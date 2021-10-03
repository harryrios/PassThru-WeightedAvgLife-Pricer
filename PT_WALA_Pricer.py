# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 18:52:33 2021

@author: Harry Rios

This file contains the main function
     for the PT_WALA_Pricer program...
     
     PT -> Pass Through
     WALA -> Weighted Average Loan Age
"""
from InputManager import getInput, getBaseParameters, getTreasuryMatrix
from PSA import PSA, WAL_months, cutting, front_and_back_WAL
from YieldPlotter import yield_plotter, numerate_month, month_diff
from Yield_To_Price import helper0,helper1,helper2,helper3,YieldToPrice,PriceToYield,front_and_back_price
from OutputManager import outputResults

def front_spread_calc(data_arr):
    back_spread = data_arr[0]
    back_WAL = data_arr[1]
    front_WAL = data_arr[2]
    plus300_cut_percent = data_arr[3]
    WAM = data_arr[4]
    price = data_arr[5]
    base_cut_ind = data_arr[6]
    start_month = data_arr[7]
    base_cashflows = data_arr[8]
    start_date = data_arr[9]
    TRSY_mat = data_arr[10]
    
    back_yield = yield_plotter([back_WAL*12], start_date, TRSY_mat)
    back_yield = back_yield[0]
    back_price = YieldToPrice([base_cashflows[1],base_cashflows[4], back_yield,
                                  base_cut_ind, WAM],0)
    front_price = price - ((1-plus300_cut_percent)*back_price)/plus300_cut_percent
    
    front_yield = PriceToYield([base_cashflows[4], base_cashflows[1], base_cut_ind, start_month], front_price, 1.9318)
    front_yield_two = yield_plotter([front_WAL], start_date, TRSY_mat)
    front_yield_two = front_yield_two[0]
    front_spread = front_yield - front_yield_two
    
    return (front_spread, front_price, back_price)

def zero_to_thirty(BP_arr, start_arr, TRSY_mat):
    
    TOTAL_PRICE_arr = []
    front_spread = None
    
        #### GENERATE +300 CASHFLOWS ####
    plus300_cashflows = PSA(BP_arr, float(BP_arr[5]))
    # principal, interest, scheduled principal, prepayment, total principal
    
        #### GENERATE BASE CASHFLOWS ####
    base_cashflows = PSA(BP_arr, float(BP_arr[6]))
    
    for start_month in range(30): ### SHOULD BE 30
        
            #### GENERATE WEIGHTED AVG LIFE BY MONTHS ####
        WAL = WAL_months(plus300_cashflows[2],plus300_cashflows[3]
                ,plus300_cashflows[0], int(BP_arr[2]), start_month)
        
            #### CUTTING +300 ####
        tmp = cutting(plus300_cashflows[4],plus300_cashflows[2],
                  plus300_cashflows[0][0], int(BP_arr[2]), start_month)
        
        plus300_cut_percent = tmp[0]
        plus300_cut_ind = tmp[1]
        
            #### FRONT AND BACK WAL ####
        tmp = front_and_back_WAL(plus300_cashflows[4],plus300_cashflows[0]
                              ,int(BP_arr[2]), plus300_cut_percent, start_month)
        front_WAL = tmp[0]
        back_WAL = tmp[1]
        base_cut_ind = tmp[2]    
            
        #### if/else part (depending on front spread) #####
        if (start_month == 0):
            tmp = front_spread_calc([float(BP_arr[8]), back_WAL,front_WAL, plus300_cut_ind, int(BP_arr[2]),
                              float(BP_arr[7]), base_cut_ind, start_month,base_cashflows, start_arr, TRSY_mat])
            front_spread = tmp[0]
            total_price = tmp[1]*plus300_cut_percent + tmp[2]*(1-plus300_cut_percent)
            TOTAL_PRICE_arr.append(total_price)
        else:
            tmp = yield_plotter([front_WAL], start_arr, TRSY_mat)
            front_yield = tmp[0] + front_spread
            tmp = yield_plotter([back_WAL], start_arr, TRSY_mat)
            back_yield = tmp[0] + float(BP_arr[8])
            tmp = YieldToPrice([base_cashflows[0],base_cashflows[4],base_cut_ind,int(BP_arr[2]),
                                  float(BP_arr[1]),front_yield,back_yield, start_month],3)
            total_price = tmp[0]*plus300_cut_percent + tmp[1]*(1-plus300_cut_percent)
            TOTAL_PRICE_arr.append(total_price)
            
    return TOTAL_PRICE_arr

def main():
    #### TAKE INPUTS ####
    TM_filename = "TM.txt"
    BP_filename = "BP.txt"
    tmp = getInput(BP_filename, TM_filename)
    
    BP_arr = tmp[0] # Base Parameters -> lst(str)
    #[WAC, CPN, WAM, WALA, OLS, pPSA, bPSA, price, back_spread]
    
    start_arr = tmp[1] # Start Date -> lst(str)
    TRSY_mat = tmp[2] # Treasury Data -> lst(lst(str))
    
    PRICER_arr = zero_to_thirty(BP_arr, start_arr, TRSY_mat)
    
    #### OUTPUT RESULTS ####
    OF_filename = 'OF.txt.'
    outputResults(OF_filename, PRICER_arr)
     
main()
