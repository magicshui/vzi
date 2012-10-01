#coding: utf-8
import os
#from bs4 import BeautifulSoup

import datetime
from datetime import *
import urllib2
#from bs4 import BeautifulSoup
import urllib2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy import Column, Integer, String
from flask import *
from flask import request,render_template,session,redirect
from flask.views import MethodView
from sqlalchemy.orm import sessionmaker
import md5
import json
#from bs4 import BeautifulSoup
from sqlalchemy import Column, Integer, String
from datetime import *
from datetime import timedelta
#import requests as httprequest

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy import Column, Integer, String
from flask import *
from flask import request,render_template,session,redirect,flash
from flask.views import MethodView
from sqlalchemy.orm import sessionmaker
import re
import string

from sqlalchemy.sql.expression import *
import datetime

import urllib2
import json
from functools import wraps

from sqlalchemy import Column, Integer, String
from datetime import *
from weibo import *
import logging
from logging.handlers import SMTPHandler
import string
import sys
from sqlalchemy.pool import NullPool
import douban_client
import oauth2
from oauth2 import *

from douban_client import *

reload(sys)
sys.setdefaultencoding('utf8')

THE_ENV = 'aws'

if THE_ENV=='sys':

    Weibo_APP_KEY = '570026225'
    Weibo_APP_SECRET = '45ea1cae01eecda0e07a2b88a256d7a2'
    Weibo_CALLBACK_URL = 'http://movie.shui.us/oauth/back/weibo'
    Douban_APP_KEY='03a5da64a44660190af18f2decd3204b'
    Douban_APP_SECRET ='cbc5c5e36886894f'
    Douban_CALLBACK_URL='http://movie.shui.us/oauth/back/douban'
    DATABASE_USER = 'ubuntu'
    DATABASE_PWD ='shuishui123'
    DATABASE_NAME= 'vzi'
    DATABASE_HOST='http://aws-db-vzi.ctspojliopg8.us-west-2.rds.amazonaws.com'
    DATABASE_PORT='3306'
    UPLOAD_FOLDER='/home/ubuntu/pro/vzi/vzi/static/movie/'
    UPLOAD_FOLDER_BACK='/home/ubuntu/pro/vzi/vzi/static/back/'
    DB = create_engine('mysql://%s:%s@%s:%s/%s'% (DATABASE_USER,DATABASE_PWD,DATABASE_HOST,DATABASE_PORT,DATABASE_NAME),connect_args={'charset':'utf8'},echo=True,poolclass=NullPool)

else:
    Weibo_APP_KEY = '1298147116'
    Weibo_APP_SECRET = '54beadf29b1798fc7bebb2e7a9d6fa74'
    Weibo_CALLBACK_URL = 'http://127.0.0.1:5000/oauth/back/weibo'
    Douban_APP_KEY='03a5da64a44660190af18f2decd3204b'
    Douban_APP_SECRET ='cbc5c5e36886894f'
    Douban_CALLBACK_URL='http://127.0.0.1:5000/oauth/back/douban'
    DATABASE_USER = 'root'
    DATABASE_PWD =''
    DATABASE_NAME= 'vzi'
    DATABASE_HOST='127.0.0.1'
    DATABASE_PORT='3306'
    UPLOAD_FOLDER='/Users/Arthur/PycharmProjects/vzius/static/movie/'
    DB = create_engine('mysql://%s:%s@%s:%s/%s'% (DATABASE_USER,DATABASE_PWD,DATABASE_HOST,DATABASE_PORT,DATABASE_NAME),connect_args={'charset':'utf8'},echo=True,poolclass=NullPool)

Base = declarative_base()
class SysInfo(Base):
    __tablename__='sys_list'
    crt_time=Column(DateTime,primary_key=True)
    douban=Column(String(40))
    def __init__(self,douban):
        self.douban=douban
        self.crt_time=datetime.now()
        
class Lines(Base):
    __tablename__="lines_list"
    id=Column(String(20),primary_key=True)
    name=Column(String(30))
    avatar=Column(String(100))
    crt_time=Column(DateTime)
    content=Column(Text)
    movie_id=Column(String(20))
    cut=Column(String(200))

    def __init__(self,content,movie_id,cut=''):
        self.id=_id_gen()
        self.name=session['name']
        self.avatar=session['avatar']
        self.crt_time=datetime.now()
        self.content=content
        self.movie_id=movie_id
        if  'SERVER_SOFTWARE' in os.environ:
            self.cut=cut
        elif cut!='':
            self.cut="/static/movie/"+self.id+'.'+cut
class Movie(Base):
    __tablename__='movie_list'
    id=Column(String(20),primary_key=True)
    title=Column(String(30))
    alt_title=Column(String(30))
    image=Column(String(200))
    alt=Column(String(200))
    summary=Column(Text)
    source_data=Column(Text)
    back=Column(String(200))

    def __init__(self,id,title,alt_title,image,alt,summary,source_data=''):
        self.id=id
        self.title=title
        self.alt_title=alt_title
        self.image=image.replace('sp','mp')
        self.alt=alt
        self.summary=summary
        self.source_data=source_data


class User(Base):
    __tablename__='user_list'

    name = Column(String(30))
    come = Column(String(30))
    id = Column(String(30),primary_key=True)
    crt_time = Column(DateTime)
    avatar = Column(String(200))


    def __init__(self,name,come,avatar):
        self.name = name
        self.come=come
        self.id = _id_gen()
        self.crt_time = datetime.now()

# the helper functions
def _if_user_exists(name):
    r=dbSession.query(User).filter(User.name==name).all()
    if r:
        return True
    else:
        return False

def _id_gen(id=None):
    if not id:
        id=str(datetime.now())
    import md5
    return str(md5.md5(id).hexdigest())

def _user_login():
    if 'name' in session and 'come' in session:
        return True
    return False



Base.metadata.create_all(DB)
db_session=sessionmaker(bind=DB)

