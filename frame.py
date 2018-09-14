#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 16:50:36 2018

@author: ghkim
"""
import os
import numpy as np

class frame():
    def __init__(self, datapath, filename):
        self.filename = filename
        os.chdir(datapath)
        self.__fID = open(filename, 'rb')
        self.shape = np.fromfile(self.__fID, np.uint16, count=2).astype(int)
        self.cur_frame = 0
        self.length = int((os.path.getsize(filename) - 4)/(self.shape[0] * self.shape[1]))
    def __del__(self):
        self.__fID.close()
        
    def get_next_frame(self):
        self.cur_frame += 1
        return np.fromfile(self.__fID, np.uint8, count=self.shape[0]*self.shape[1]).reshape(self.shape)
    
    def get_frame(self, frame_number):
        self.__fID.seek(2 + self.shape[0]*self.shape[1] * (frame_number - 1))
        one_frame = np.fromfile(self.__fID, np.uint8, count=self.shape[0]*self.shape[1]).reshape(self.shape)
        self.__fID.seek(2 + self.shape[0]*self.shape[1] * (self.cur_frame))
        return  one_frame
    
    def stack_image(self, start = 1, end = None):
        if end is None:
            end = self.length
        self.__nst = (end - start + 1)
        self.fortest = 1
        self.__fID.seek(2 + self.shape[0]*self.shape[1] * (start-1))
        self.stacked_image = np.zeros(self.shape)
        for i in np.linspace(start, end, end - start + 1):
            self.stacked_image += self.get_next_frame()/self.__nst
            self.fortest += 1
        self.__fID.seek(2 + self.shape[0]*self.shape[1] * (self.cur_frame))
        return self.stacked_image