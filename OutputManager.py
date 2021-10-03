# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 13:45:14 2021

@author: Harry Rios
"""


def outputResults(OF_filename, data_arr):
    OF = open(OF_filename, 'w')
    month = 1
    for data in data_arr:
        print( month, ' : ', data, file = OF)
        month += 1
