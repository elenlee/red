#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 15:53:07 2019

@author: elenalee
"""
from sqlalchemy import Table, MetaData
from sqlalchemy.orm import mapper, relation
from app import db

class Image(object):
    def __init__(self, id=None, red=None):
        self.id = id
        self.red = red
    def __repr__(self):
        return '<Image {}, red = {}>'.format(self.id, self.red)
    
class Account(object):
    def __init__(self, id=None):
        self.id = id
    def __repr__(self):
        return '<Account {}>'.format(self.id)
    
class Tag(object):
    def __init__(self, tag=None):
        self.tag = tag
    def __repr__(self):
        return '<Tag {}>'.format(self.tag)

def setup_models():
    metadata = MetaData(db)
    images = Table('images', metadata, autoload=True)
    accounts = Table('accounts', metadata, autoload=True)
    association = Table('accounts_tags', metadata, autoload=True)
    tags = Table('tags', metadata, autoload=True)
    
    mapper(Account, accounts)
    mapper(Tag, tags, properties={
        'accounts': relation(Account, secondary=association, backref='tags')})
    mapper(Image, images, properties={
        'tag': relation(Tag, backref='images'),
        'account': relation(Account, backref='images')})