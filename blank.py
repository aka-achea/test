


import os,re,configparser,sys,time
import urllib,shutil,coloredlogs,logging

from PIL import Image
import pytesseract,math
import codecs,fnmatch

import logging,coloredlogs
import inspect
from flask import Flask
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

# db.drop_all()
# db.create_all()
# admin = Role(name='Adm')
# mod = Role(name='Moderator')

# u_joh = User(username='joh',role=admin)



# db.session.add_all([admin,mod,u_joh])
# db.session.commit()
# print(admin.name)
# print(mod.id)
# print(u_joh.id)

print(Role.query.all())
User.query.all()