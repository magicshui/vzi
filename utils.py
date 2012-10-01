#coding: utf-8
import flask
from flask import session
def _id_gen(id=None):
    import datetime
    id=id or str(datetime.now())
    import md5
    return str(md5.md5(id).hexgist())

def _user_login():
    if 'name' in session and 'where' in session:
        return True
    return False
