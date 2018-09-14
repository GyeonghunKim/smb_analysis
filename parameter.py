#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 17:50:42 2018

@author: ghkim
"""
import numpy as np
from pandas import DataFrame, Series

class parameter:
    def __init__(self):
        self.__param_data = {'input_type': 'tif'}
        self.__param_data['movie_x_size'] = 512
        self.__param_data['movie_y_size'] = 512
        self.__param_data['pixel_size'] = 104
        self.__param_data['kernel_rad'] = 5
        self.__param_data['movie_length'] = 0
    def add_attr(self, param_name, param_value):
        if param_name in self.__param_data.keys():
            print('parameter ',param_name,'already exist')    
        else:
             self.__param_data[param_name] = param_value
    def delete_attr(self, param_name):
        if param_name in self.__param_data.keys():
            del self.__param_data[param_name]
        else:
            print('parameter ',param_name,'does not exist')     
    def set_attr(self, param_name, param_value):
        if param_name in self.__param_data.keys():
            self.__param_data[param_name] = param_value
        else:
            print('parameter ',param_name,'does not exist')     
    def get_attr(self, param_name):
        if param_name in self.__param_data.keys():
            return self.__param_data[param_name]
        else:
            return np.nan
    def print_value(self, param_name):
        if param_name in self.__param_data.keys():
            print(param_name, ':', self.__param_data[param_name])
        else:
            print('parameter ',param_name,'does not exist')
    def print_parameters(self):
        for key, value in self.__param_data.items():
            print(key,':', value)
