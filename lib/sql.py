from __future__ import absolute_import, division, with_statement

import datetime
from typing import (
    Optional,
)
from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from lib import exceptions, logger
from lib.db.engine import TableModel
from lib.db.session import SessionOrm, _ScopedSession as Dbsession
from sqlalchemy.dialects.mysql import \
    BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
    DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
    LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
    NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
    TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR


def NotFoundSetting(param):
    pass


class Drvice(TableModel):
    __tablename__ = 'drvice_tables'
    __table_args__ = {'comment': '存放路由器配置'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    drvice_name = Column(VARCHAR(100))
    _drvice_passwd = Column(VARCHAR(100))
    drvice_host = Column(VARCHAR(100))
    drvice_port = Column(INTEGER)
    drvice_type = Column(VARCHAR(100))
    last_updated = Column(DateTime)

    # 加密存储
    # @property
    # def password(self):
    #     raise Exception('密码不能被读取')  # 为了保持使用习惯，还是设置一个password字段用来设置密码，当然也不能被读取。
    #
    # # 赋值password，则自动加密存储。
    # @password.setter
    # def password(self, value):
    #     self._drvice_passwd = generate_password_hash(value)
    #
    # # 使用check_password,进行密码校验，返回True False。
    # def check_password(self, pasword):
    #     return check_password_hash(self._drvice_passwd, pasword)

    def __repr__(self):
        return "<Drvice(id={}, drvice_name={}, _drvice_passwd={}," \
               " drvice_host={}, drvice_port={}, drvice_type={}, last_updated={})>".format(
            self.id, self.drvice_name, self._drvice_passwd, self.drvice_host,
            self.drvice_port, self.drvice_type, self.last_updated
        )

    def all(self):
        return {'id': self.id, 'drvice_name': self.drvice_name,
                '_drvice_passwd': self._drvice_passwd,
                'drvice_host': self.drvice_host,
                'drvice_port': self.drvice_port,
                'drvice_type': self.drvice_type,
                'last_updated': self.last_updated}


class DrviceOrm:
    orm = SessionOrm()

    @classmethod
    def update_setting(cls, drvice_name, _drvice_passwd):
        query = cls.get(drvice_name)
        if not query:
            raise NotFoundSetting(
                "'drvice_name' {} not found from table".format(
                    drvice_name)
            )
        with cls.orm as s:
            query._drvice_passwd = _drvice_passwd

    @classmethod
    def get(cls, drvice_name):
        return cls.orm.get(Drvice, drvice_name=drvice_name)

    @classmethod
    def all(cls):
        return cls.orm.all(Drvice)


class Script(TableModel):
    __tablename__ = 'drvice_script'
    __table_args__ = {'comment': '存放路由器脚本'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    drvice_type = Column(VARCHAR(100))
    script_name = Column(VARCHAR(100))
    script_reson = Column(LONGTEXT)
    last_updated = Column(DateTime)

    def __repr__(self):
        return "<Script(id={}, drvice_type={}, script_name={}," \
               " script_reson={}, last_updated={})>".format(
            self.id, self.drvice_type, self.script_name, self.script_reson,
            self.last_updated
        )

    def all(self):
        return {'id': self.id, 'drvice_type': self.drvice_type,
                'script_name': self.script_name,
                'script_reson': self.script_reson,
                'last_updated': self.last_updated}


class ScriptOrm:
    orm = SessionOrm()

    @classmethod
    def update_script(cls, script_name, script_reson):
        query = cls.get(script_name)
        if not query:
            raise NotFoundSetting(
                "'drvice_name' {} not found from table".format(
                    script_reson)
            )
        with cls.orm as s:
            query.script_reson = script_reson

    @classmethod
    def get(cls, script_name):
        return cls.orm.get(Script, script_name=script_name)

    @classmethod
    def get_type(cls, drvice_type):
        return cls.orm.get(Script, drvice_type=drvice_type)

    @classmethod
    def all(cls):
        return cls.orm.all(Script)


def DropAllTable():
    from lib.db.engine import DropAllTable
    return DropAllTable()


def CreateAllTable():
    from lib.db.engine import CreateAllTable
    return CreateAllTable()


def ReInitTableEntry():
    DropAllTable()
    CreateAllTable()
