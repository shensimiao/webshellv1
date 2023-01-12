from __future__ import absolute_import, division, with_statement

import functools
from lib.db.engine import Base, SQLENGINE
from lib.log import logger
from sqlalchemy.exc import InvalidRequestError, IntegrityError, OperationalError, StatementError
from sqlalchemy.orm import sessionmaker, scoped_session, query
from pymysql.err import OperationalError as PymysqlOperationError
from typing import (
    Any,
    NoReturn,
    Callable,
    Type,
    TypeVar,
    Tuple,
    List,
    Optional,
    Union,
    Mapping,
)

__all__ = [
    'SQLSESSION',
    'SessionOrm',
    'flush_cache_from_sqlalchemy',
    'SQLSession',
    '_SessionClassType',
    '_ScopedSession',
    'Session'
]

Protocol = object
_SessionType = TypeVar("_SessionType")


class _SessionClass(Protocol):

    def __enter__(self) -> Type[_SessionType]:
        pass

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def destroy(self) -> None:
        pass


_SessionClassType = TypeVar("_SessionClassType", bound=_SessionClass)

# Session工厂， 通过这个生产的session对象对于线程是不安全的
_SessionFactory = sessionmaker(bind=SQLENGINE)

# 通过scoped_session获取的session是安全的，同个线程获取相同session,不同线程获取不同的session，
# 线程间不会获取到相同的session
_ScopedSession = scoped_session(_SessionFactory)


class Session(_SessionClass):

    def __init__(self, session: _SessionType):
        self.session = session
        self.closed = False
    """
    def __enter__(self) -> _SessionType:
        if self.closed:
            raise RuntimeError('{} session has closed')
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()
    """

    def destroy(self):
        if not self.closed:
            self.session.close()
            self.session = None
            self.closed = True

    def __getattr__(self, item) -> Callable[..., None]:
        return getattr(self.session, item)


class SQLSession(object):
    @classmethod
    def create(cls) -> _SessionClassType:
        return Session(_ScopedSession())

    def __call__(self) -> _SessionClassType:
        return self.create()


SQLSESSION = SQLSession()


def recoverySqlalchemy(func):
    @functools.wraps(func)
    def wrapper(cls, *args, **kwargs):
        try:
            result = func(cls, *args, **kwargs)
        except (InvalidRequestError, StatementError):
            # 连接断开后， 事务没有回滚，残留的锁导致后续的查询报错
            cls.rollback()
            result = func(cls, *args, **kwargs)
        except (OperationalError, PymysqlOperationError):
            cls.reload_session()
            cls.rollback()
            result = func(cls, *args, **kwargs)
        return result

    return wrapper


class SessionOrm(object):

    def __init__(self):
        self.session = None
        self.reload_session()
        self.DBsession = _ScopedSession

    def reload_session(self):
        if self.session:
            del self.session
            logger.debug('clear old session.')
        self.session: _SessionClassType = SQLSESSION()
        logger.debug('create a session.')

    @recoverySqlalchemy
    def add(self, orm: Type[Base]) -> NoReturn:
        self.session.add(orm)

    @recoverySqlalchemy
    def add_all(self, orms: List[Type[Base]]) -> NoReturn:
        self.session.add_all(orms)

    # @recoverySqlalchemy
    # def add_qucik_all(self, Quick) -> NoReturn:
    #     self.DBsession.bulk_save_objects(Quick)
    #     self.DBsession.commit()

    @recoverySqlalchemy
    def query(self, orm: Type[Base]):
        queryset = self.session.query(orm)
        return queryset

    @recoverySqlalchemy
    def filter(
            self, orm: Type[Base], *filter_condition: Tuple
    ) -> List:
        # print(orm, *filter_condition)
        # e.g.::
        # filter_condition using SQL expressions:
        # MyClass.name == 'some name'
        return self.query(orm).filter(*filter_condition).all()

    @recoverySqlalchemy
    def filter_by(
            self, orm: Type[Base], **filter_by_condition: Mapping
    ) -> List:
        return self.query(orm).filter_by(**filter_by_condition).all()

    @recoverySqlalchemy
    def exist(
            self, orm: Type[Base], **filter_by_condition: Mapping
    ) -> bool:
        if self.get(orm, **filter_by_condition) is None:
            return False
        return True

    @recoverySqlalchemy
    def all(self, orm: Type[Base]) -> List:
        return self.query(orm).all()

    @recoverySqlalchemy
    def get(self, orm: Type[Base], **filter_by_condition) -> List:
        queryset = self.filter_by(orm, **filter_by_condition)
        if queryset:
            return queryset[0]
        return None

    @recoverySqlalchemy
    def update(
            self, db_query_obj: Type[Base], **parameter: Mapping
    ) -> None:
        with self.session as s:
            for k, v in parameter.items():
                if hasattr(db_query_obj, k):
                    setattr(db_query_obj, k, v)

    @recoverySqlalchemy
    def delete(self, db_query_obj: Type[Base]) -> None:
        if isinstance(db_query_obj, query.Query):
            db_query_obj = db_query_obj.first()
        try:
            self.session.delete(db_query_obj)
        except InvalidRequestError:
            self.rollback()
            self.session.delete(db_query_obj)

    def commit(self) -> bool:
        logger.debug('commit transaction.')
        try:
            self.session.commit()
        except InvalidRequestError as e:
            logger.error('出错回滚' % e)
            self.rollback()
            self.session.commit()
            return True
        except Exception as e:
            logger.error('An exception is committed to the database. '
                         'the transaction will be rollback: %s' % e)
            self.rollback()
            return False
        else:
            return True

    def flush_cache(self) -> bool:
        # 只要没有操作commit， sqlalchemy默认是从缓存读取第一次查询的数据
        # 这里要刷新数据只能commit
        logger.debug('flush cache from sqlalchemy.')
        return self.commit()

    def rollback(self) -> NoReturn:
        logger.debug('rollback transaction.')
        self.session.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_trace):
        if exc_type or exc_val or exc_trace:
            import traceback
            self.rollback()
            logger.error(
                'An exception occurred during the execution of the orm operation.'
                ' the transaction will be rollback'
            )
            logger.error(
                'exc_type : {} , exc_value: {},'.format(exc_type, exc_val)
            )
            for trace in traceback.extract_tb(exc_trace):
                logger.error("{}".format(trace))
            return
        self.commit()


def flush_cache_from_sqlalchemy():
    SessionOrm().flush_cache()


class ModelOrm:

    def __init__(self):
        self.session = SessionOrm()
        self.config_model()

    def config_model(self):
        self.model = None

    def reload_session(self):
        self.session = SessionOrm()

    def all(self):
        return self.session.query(self.model).all()

    def get(self, **kwargs):
        queryset = self.session.filter_by(self.model, **kwargs)
        return queryset

    def create(self, obj):
        with self.session as s:
            s.add(obj)

    def delete(self, **kwargs):
        queryset = self.get(**kwargs)
        if not queryset:
            return False
        with self.session as s:
            for obj in queryset:
                s.delete(obj)
        return True
