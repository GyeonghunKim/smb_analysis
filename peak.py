#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 18:02:22 2018

@author: ghkim
"""
import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt


class peaks:
    def __init__(self):
        # self.__temp = {'index':0, 'x':0,'y':0,'intensity':0,'sigma':0,'kernel_intensity':0, 'isValid':0}
        self.data = DataFrame({'x':[0],'y':[0],'intensity':[0],'sigma':[0],'kernel_intensity':[0], 'isValid':[0]})
        self.__list = ('x','y','intensity','sigma','kernel_intensity','isValid')
        self.number_peak = 0

    def add_peak(self, data, parameter):
        self.__temp_nPeak = data.shape[0]
        print(self.__temp_nPeak)
        temp_rad = parameter.get_attr('sub_rad')
        temp_xsize = parameter.get_attr('movie_x_size')
        temp_ysize = parameter.get_attr('movie_y_size')
        for i in range(self.__temp_nPeak):
            self.data.loc[self.number_peak+i, ['x','y']] = data[i]
            temp_x = self.data.loc[self.number_peak+i, ['x']]
            temp_y = self.data.loc[self.number_peak+i, ['y']]
            if (int(temp_x > temp_rad) and int(temp_x < temp_xsize - temp_rad)) and (int(temp_y > temp_rad) and int(temp_y < temp_ysize - temp_rad)):
                self.data.loc[self.number_peak+i, ['isValid']] = True
            else:
                self.data.loc[self.number_peak+i, ['isValid']] = False
        
        
    def valid_test_from_crit(self,test_type, crit_type, parameter):
        if (test_type+'_crit' in parameter.param_data):
            for i in self.data.index:
                if crit_type == 'upper_limit':
                    if int(self.data.loc[i, [test_type]].isnull()):
                        self.data.loc[i, ['isValid']] = False    
                    elif not ((float(self.data.loc[i, [test_type]]) < parameter.param_data[test_type+'_crit'])):
                        self.data.loc[i, ['isValid']] = False

                elif crit_type == 'lower_limit':
                    if int(self.data.loc[i, [test_type]].isnull()):
                        self.data.loc[i, ['isValid']] = False    
                    elif not ((float(self.data.loc[i, [test_type]]) > parameter.param_data[test_type+'_crit'])):
                        self.data.loc[i, ['isValid']] = False
                else:
                    print('wrong crit. type')
        else:
            print('wrong parameter')
            
    def get_inten_from_SM(self, stacked_movie, parameter):
        sub_rad = parameter.get_attr('sub_rad')
        for i in self.data.index:
            if (int(self.data.loc[i, ['isValid']]) == True):
                x = int(self.data.loc[i,['x']])
                y = int(self.data.loc[i,['y']])
                temp_img = stacked_movie[x-sub_rad:x+sub_rad+1,y-sub_rad:y+sub_rad+1]
                self.data.loc[i, ['kernel_intensity']] = sum(sum(temp_img))
                self.data.loc[i, ['intensity']] = stacked_movie[x, y]

    
    def calc_sigma_fit(self, stacked_movie, parameter):
        sub_rad = parameter.get_attr('sub_rad')
        for i in self.data.index:
            if (int(self.data.loc[i, ['isValid']]) == True):
                x = int(self.data.loc[i,['x']])
                y = int(self.data.loc[i,['y']])
                temp_img = stacked_movie[x-sub_rad:x+sub_rad+1,y-sub_rad:y+sub_rad+1]
                fit_params = fitgaussian(temp_img)
                fit = gaussian(*fit_params)
                (height, x, y, width_x, width_y) = fit_params
                self.data.loc[i, ['sigma']] = np.sqrt(width_x*width_x + width_y*width_y)
                
    def plotPeaks(self, stacked_movie, withSM, parameter, size = ((15, 15))):
        fig, ax = plt.subplots(figsize = size)
        if withSM:
            ax.imshow(stacked_movie)
        __validData = self.data[self.data['isValid']][['x', 'y']]
        for i in __validData.index:
            x = int(__validData.loc[i,['x']])
            y = int(__validData.loc[i,['y']])
            ax.plot(y, x, 'ro')
