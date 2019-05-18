#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 08:22:55 2019

@author: elenalee
"""

from aiohttp import web
from app import routes

app = web.Application()
routes.setup_routes(app)
