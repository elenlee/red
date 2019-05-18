#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 18:43:35 2019

@author: elenalee
"""
#from app import app
import aiohttp
import os
from config import IMAGES_SAVE_PATH
from app.red_lib import get_red_percent

async def index(request):
    data = await request.json()
    return aiohttp.web.Response(text='Hello {}!'.format(data['name']))

async def image(request):
    # чтение параметров запроса
    account_id = request.rel_url.query['account_id']
    try:
        tag = request.rel_url.query['tag']
    except KeyError:
        tag = ''
    # Формирование уникального идентификатора изображения
    im_id = 0
    filename = 'im{}.jpg'.format(im_id)
    # Считывание по частям и сохранение в файл
    size = 0
    with open(os.path.join(IMAGES_SAVE_PATH, filename), 'wb') as f:
        while True:
            chunk = await request.content.read(8192)  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)
    # Расчет количества красного на изображении
    im_red = get_red_percent(os.path.join(IMAGES_SAVE_PATH, filename))
    
    return aiohttp.web.json_response({'image_id': im_id, 'red': im_red})

async def count(request):
    # Подсчет количества записей, удовлетворяющих запросу
    params = request.rel_url.query
    account_id = params['account_id']
    tag = params['red']
    red_gt = params['red_gt']
    count = 0
    return aiohttp.web.Response(count)

async def get_image_info(request):
    im_id = request.match_info['image_id']
    im_info = {'image_id': im_id, 'red': 0, 'account_id': 0, 'tag': ''}
    return aiohttp.web.json_response(im_info)

async def del_image(request):
    return aiohttp.web.Response(text=
        'Image {} succesfully deleted'.format(request.match_info['image_id']))

def setup_routes(new_app):
    new_app.router.add_get('/', index)
    new_app.router.add_post('/image',image)
    new_app.router.add_get('/image/count',count)
    # динамический маршрут
    new_app.router.add_get('/image/{image_id:\d+}', get_image_info)
    new_app.router.add_delete('/image/{image_id:\d+}', del_image)