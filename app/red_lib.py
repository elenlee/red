#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Библиотека:
  get_red_percent(path) - функция расчета процента пикселей на изображении,
    в которых преобладает красный цвет;
    input: path - полный путь файла;
    return ...
    
Created on Fri May 17 07:37:44 2019

@author: elenalee
"""

from matplotlib.image import imread
from numpy import count_nonzero

def get_red_percent(path):
    im_array = imread(path).reshape(-1,3)
    # Выделение отдельного канала: im_array[:,С]
    # С = 0: RED, 1: GREEN, 2: BLUE
    # Преобладание красного цвета пиксела i:
    # RED(i) > GREEN(i) и RED(i) > BLUE(i) = True
    temp = (im_array[:,0]>im_array[:,1]) & (im_array[:,0]>im_array[:,2])
    return count_nonzero(temp) / len(temp) * 100
