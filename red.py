#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:21:58 2019

@author: elenalee
"""

from app import app
import aiohttp
#import asyncio

aiohttp.web.run_app(app, host='127.0.0.1', port='8080')