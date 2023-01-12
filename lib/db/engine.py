from __future__ import absolute_import, division, with_statement

from sqlalchemy import create_engine, Table, MetaData

from sqlalchemy.ext.declarative import declarative_base

from .settings import (
    MYSQL_URI, SQLECHO, SQLENCODING, SQLConnPoolRecycle,
    SQLConnPoolSize, SQLECHOPOOL,
)
from lib import logger

__all__ = [
    'SQLENGINE',
    'Base',
    'TableModel',
    'CreateAllTable',
    'DropAllTable',
]

SQLENGINE = create_engine(
    MYSQL_URI,
    echo=SQLECHO,
    encoding=SQLENCODING,
    pool_pre_ping=True,
    pool_size=SQLConnPoolSize,  # 连接池大小
    echo_pool=SQLECHOPOOL,
    pool_recycle=SQLConnPoolRecycle,  # 池回收时
)

Base = declarative_base()
metadata = MetaData(bind=SQLENGINE)


class TableModel(Base):
    __abstract__ = True
    extend_existing = True


def CreateAllTable():
    try:
        Base.metadata.create_all(SQLENGINE)
    except Exception as e:
        logger.error('create metadata to db error: %s' % e)
        return False
    else:
        return True


def DropAllTable():
    try:
        Base.metadata.drop_all(SQLENGINE)
    except Exception as e:
        logger.error('drop all table from db error: %s' % e)
        return False
    else:
        return True
