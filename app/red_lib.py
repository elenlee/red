#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Библиотека:
  get_image_from_request(request) - функция считывания и декодирования
    бинарного файла с изображением (используется OpenCV)
    input: post запрос бинарным файлом
    return: numpy массив изображения
        
  get_red_percent(np_image) - функция расчета процента пикселей на изображении,
    в которых преобладает красный цвет;
    input: mp_image - numpy массив - результат декодирования бинарного файла
                      с помощью OpenCV;
    return: процент пикселей на изображении, в которых преобладает красный цвет
    
  add_to_db(account_id, tag, im_red) - функция добавления в базу данных
    данных об изображении
      input: account_id - идентификатор аккаунта пользователя,
             tag - строка информации об изображении,
             im_red - процент пикселей на изображении, в которых преобладает
                красный цвет
      return: im_id - уникальный идентификатор изображения
  
  get_image_info(im_id) - функция извлечения из базы данных информации
    об изображении
    input: идентификатор изображения
    return: im_info = {'image_id': .., 'red': .., 'account_id': .., 'tag': ..}
  
  get_count(account_id, tag, red_gt) - функция подсчета количества записей
    в базе данных, удовтелетворяющих условиям запроса
    input: account_id - идентификатор аккаунта пользователя,
             tag - строка информации об изображении,
             red_gt - минимальный процент пикселей на изображении, в которых
                преобладает красный цвет
    return: количество записей, удовлетворяющих условиям запроса
  
  del_from_db(im_id) - функция удаления из базы данных изображения
    input: идентификатор изображения, запись о котором необходимо удалить
    return: 1 в случае успеха, иначе 0 (если изображения нет в базе)

    
Created on Fri May 17 07:37:44 2019

@author: elenalee
"""
import numpy as np
import cv2
from app import session
from app.models import Image, Account, Tag
from sqlalchemy import func

async def get_image_from_request(request):
    # Считывание по частям
#    np_image_bytes = np.array([])
#    while True:
#        chunk = await request.content.read(8192)  # 8192 bytes by default.
#        if not chunk:
#            break
#        np_image_bytes = np.append(np_image_bytes,
#                                   np.frombuffer(chunk, np.uint8))
    # Считывание целиком
    np_image_bytes = np.frombuffer(await request.content.read(), np.uint8)
    # Декодирование (OpenCV)
    np_image = cv2.imdecode(np_image_bytes, -1)
    return np_image

def get_red_percent(np_image):
    np_image = np_image.reshape(-1,3)
    # Выделение отдельного канала: im_array[:,С]
    # С = 0: BLUE, 1: GREEN, 2: RED
    # Преобладание красного цвета пиксела i:
    # RED(i) > GREEN(i) и RED(i) > BLUE(i) = True
    temp = (np_image[:,2]>np_image[:,0]) & (np_image[:,2]>np_image[:,1])
    return np.count_nonzero(temp) / len(temp) * 100

def add_to_db(account_id, tag, im_red):
    ses = session()
    # Используем аккаунт из базы или создаем новый
    cur_ac = ses.query(Account).get(account_id)
    if not cur_ac:
        cur_ac = Account(account_id)
        ses.add(cur_ac)
    # Используем тэг из базы, если он уже использовался этим аккаунтом,
    # или создаем новый
    cur_tag = ses.query(Tag).get(tag)
    if not cur_tag:
        cur_tag = Tag(tag)
        ses.add(cur_tag)
    cur_ac.tags.append(cur_tag)
    # Создаем новый объект изображения в базе и связываем с ним аккаунт и тэг
    im = Image(red=im_red)
    im.account = cur_ac
    im.tag = cur_tag
    ses.add(im)
    # Внесение изменений в базу
    ses.commit()
    # Для получения im.id необходимо обновить атрибуты
    ses.refresh(im)
    ses.close()
    return im.id
    
def get_image_info_from_db(im_id):
    ses = session()
    im = ses.query(Image).get(im_id)
    if im:
        im_info = {'image_id': im.id, 'red': im.red, \
                'account_id': im.account.id, 'tag': im.tag.tag}
        ses.close()
        return im_info
    else:
        ses.close()
        return 0

def get_count_from_db(account_id, tag, red_gt):
    ses = session()
    count = ses.query(func.count(Image.id)).\
        filter(Image.red>red_gt).\
        join('tag').\
        filter_by(tag=tag).\
        join('account').\
        filter_by(id=account_id).\
        all()
    ses.close()
    return count[0][0]

def get_accounts_from_db():
    ses = session()
    accounts = ses.query(Account).all()
    ses.close()
    return accounts

def get_account_info_from_db(account_id):
    ses = session()
    account_info = {}
    if ses.query(Account).get(account_id):
        tags = [value for value, in ses.query(Tag.tag).\
                   join('accounts').\
                   filter_by(id=account_id).all()]
        account_info['account_{}_tags'.format(account_id)] = tags
        for tag in tags:
            images = ses.query(Image.id).\
                      join('account').\
                      filter_by(id=account_id).\
                      join('tag').\
                      filter_by(tag=tag).\
                      all()
            account_info[tag] = [value for value, in images]
        ses.close()
        return account_info
    else:
        ses.close()
        return 0
    
def del_from_db(im_id):
    ses = session()
    im_to_del = ses.query(Image).get(im_id)
    if im_to_del:
        ses.delete(im_to_del)
        ses.commit()
        ses.close()
        return 1
    else:
        ses.close()
        return 0