"""
This file defines the database models
"""
import datetime
from .common import db, Field, auth
from pydal.validators import *
import uuid

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_user():
    return auth.current_user.get('id') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

def generate_unique_id():
    return str(uuid.uuid4())
# Complete. 

db.define_table(
    'post',
    Field('user_email', default=get_user_email()),
    Field('content', 'text', default=''),
    Field('tags', 'list:string'),
    Field('post_id', 'string', default=generate_unique_id()),
    Field('timestamp', 'datetime', default=get_time())
)

db.define_table(
    'tag',
    Field('name', 'string', default=''),
    Field('amount', 'integer', default=0),
    Field('toggle', 'boolean', default='false')
)

db.commit()
