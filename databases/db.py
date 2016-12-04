# -*- coding: utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import config



DB_HOST = config.mysql_host
DB_USER = config.mysql_user
DB_PWD = config.mysql_password
DB_NAME = config.mysql_database 


Base = declarative_base()
engine = create_engine('mysql+pymysql://%s:%s@%s/%s?charset=utf8' %
                       (DB_USER, DB_PWD, DB_HOST, DB_NAME),
                       encoding='utf-8', echo=False,
                       pool_size=100, pool_recycle=10)
