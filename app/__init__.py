#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 08:22:55 2019

@author: elenalee
"""
#from aiohttp import web
from asyncio import get_event_loop
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

loop = get_event_loop()
db = create_engine('sqlite:///red.db')
session = sessionmaker(db)

