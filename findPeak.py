#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 18:17:15 2018

@author: ghkim
"""

import numpy as np
from scipy.ndimage import maximum_filter

class findPeak():
    def __init__(self, image, parameter, peak):
        self.image = image
        self.param = parameter
        self.peak = peak
    
    def find_localmax(self, background = None):
        if background is None:
            background = self.param.get_attr('background')
        tmp = (self.image - background)
        self.nbimage = (1- tmp < 0) * tmp/2
        
        