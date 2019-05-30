#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:21:58 2019

@author: elenalee
"""

from app import loop
from aiohttp import web
#from asyncio import get_event_loop
#from ssl import create_default_context, Purpose

async def init_app():
    app = web.Application()
    
    from app import routes, models
    routes.setup_routes(app)
    models.setup_models()
    
    return app


if __name__ == '__main__':
    try:
        app = loop.run_until_complete(init_app())
#        ssl_context = create_default_context(Purpose.CLIENT_AUTH)
#        ssl_context.load_cert_chain('localhost.crt', 'localhost.key')
#        web.run_app(app, host='127.0.0.1', port='80',
#                        ssl_context=ssl_context)
        web.run_app(app, host='127.0.0.1', port='8443')
    except Exception as e:
        print('Error create server: %r' % e)
    finally:
        pass
    loop.close()