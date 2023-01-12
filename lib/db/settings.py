from __future__ import absolute_import, division, with_statement

from lib.config import DbConfiguration

__all__ = [
    'MYSQL_URI',
    'SQLENCODING',
    'SQLECHO',
    'SQLECHOPOOL',
    'SQLConnPoolSize',
    'SQLConnPoolRecycle',
]
config = DbConfiguration

SQLENCODING = "utf-8"
SQLECHO = False
SQLECHOPOOL = True

SQLConnPoolSize = int(config.pool_size or 5)
SQLConnPoolRecycle = int(config.pool_recycle or 7200)
SQLAutoCommit = config.autocommit

# Mysql Connection
MYSQL_HOST = config.host
MYSQL_PORT = str(config.port or 3306)
MYSQL_USER = config.username
MYSQL_PASSWD = config.password
MYSQL_DB = config.db
MYSQL_CHARSET = 'charset={}'.format(config.charset)
MYSQL_URI = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?{charset}'.format(
    user=MYSQL_USER, password=MYSQL_PASSWD, host=MYSQL_HOST, port=MYSQL_PORT,
    db=MYSQL_DB, charset=MYSQL_CHARSET
)
if SQLAutoCommit:
    MYSQL_URI += '&autocommit=true'


