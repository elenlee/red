#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 08:22:55 2019

@author: elenalee
"""
from aiohttp import web
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = web.Application()

db = create_engine('sqlite:///red.db')
session = sessionmaker(db)

from app import routes, models
routes.setup_routes(app)
models.setup_models()

#app.on_startup.append()
#app.on_cleanup.append()
