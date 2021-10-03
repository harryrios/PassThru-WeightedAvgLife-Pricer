# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 13:52:47 2021

@author: Harry Rios
"""

def numerate_month(key):
    table = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
    return table[key]

def month_diff(lower, upper):
    year_diff = int(upper[1]) - int(lower[1])
    month_diff = numerate_month(upper[0]) - numerate_month(lower[0])
    return month_diff + (year_diff * 12)

def yield_plotter(WAL, start_date, TRSY_mat):
    data = [(0,0)] # MONTH DIFF, RATE
    for i in range(len(TRSY_mat)):
        diff = month_diff(start_date, TRSY_mat[i][0:2])
        data.append((diff, float(TRSY_mat[i][2])))
    yield_lst = []
    for i in range(len(WAL)):
        j = 0
        while j in range(len(data)-1):
            if (data[j][0] <= WAL[i]) and (data[j+1][0] >= WAL[i]):
                time_diff = data[j+1][0] - data[j][0]
                time_from_lower = WAL[i] - data[j][0]
                yield_over_time = (data[j+1][1] - data[j][1]) / time_diff
                yield_lst.append(data[j][0] + (yield_over_time * WAL[i]))
                break
            j += 1
    return yield_lst
        

    
    
