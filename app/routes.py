#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 18:43:35 2019

@author: elenalee
"""
import aiohttp
from app.red_lib import get_red_percent, get_image_from_request
from app.red_lib import add_to_db, del_from_db
from app.red_lib import get_count_from_db, get_image_info_from_db
from app.red_lib import get_accounts_from_db, get_account_info_from_db

async def index(request):
    data = await request.json()
    return aiohttp.web.Response(text='Hello {}!'.format(data.get('name','Aiohttp')))

async def set_image_info(request):
    # Чтение параметров запроса
    account_id = request.rel_url.query.get('account_id')
    if not account_id:
        return aiohttp.web.HTTPBadRequest()
    tag = request.rel_url.query.get('tag','')
    # Считывание по частям и сохранение в файл
    np_image = await get_image_from_request(request)
    # Расчет количества красного на изображении
    im_red = get_red_percent(np_image)
    # Запись в БД
    im_id = add_to_db(account_id, tag, im_red)
    
    return aiohttp.web.json_response({'image_id': im_id, 'red': im_red})

async def get_count(request):
    # Подсчет количества записей, удовлетворяющих запросу
    params = request.rel_url.query
    account_id = params['account_id']
    tag = params['tag']
    red_gt = params['red_gt']
    count = get_count_from_db(account_id, tag, red_gt)
    return aiohttp.web.Response(text=str(count))

async def get_image_info(request):
    # Формирование словаря информации об изображении
    # {'image_id": ..., "red": ..., "account_id": ..., "tag": ...}
    im_id = request.match_info['image_id']
    im_info = get_image_info_from_db(im_id)
    if im_info:
        return aiohttp.web.json_response(im_info)
    else:
        return aiohttp.web.Response(text=
        'There is no Image {} in DB'.format(im_id))

async def del_image(request):
    # Удаление записи об изображении
    im_id = request.match_info['image_id']
    if del_from_db(im_id):
        return aiohttp.web.Response(text=
        'Image {} succesfully deleted'.format(im_id))
    else:
        return aiohttp.web.Response(text=
        'There is no Image {} in DB. Nothing to delete'.format(im_id))
        
async def get_accounts_list(request):
    # Формирование списка аккаунтов
    return aiohttp.web.Response(text=
        str(get_accounts_from_db()))

async def get_account_info(request):
    # Формирование словаря информации об аккаунте
    account_id = request.match_info['account']
    account_info = get_account_info_from_db(account_id)
    if account_info:
        return aiohttp.web.json_response(account_info)
    else:
        return aiohttp.web.Response(text=
        'There is no Account {} in DB'.format(account_id))

def setup_routes(new_app):
    new_app.router.add_get('/', index)
    new_app.router.add_post('/images',set_image_info)
    new_app.router.add_get('/images/count',get_count)
    # Динамический маршрут
    new_app.router.add_get('/images/{image_id:\d+}', get_image_info)
    new_app.router.add_delete('/images/{image_id:\d+}', del_image)
    # Дополнительные маршруты
    new_app.router.add_get('/accounts', get_accounts_list)
    new_app.router.add_get('/accounts/{account:\d+}', get_account_info)