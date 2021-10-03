# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 18:22:16 2021

@author: Harry Rios

This file contains the following functions:
Yield to Price,Price to Yield,front_and_back_price
Yield to Price has multiple subfunctions are requires
the appropriete data plus a key to run the right subfunction

# """

def helper0(data_arr):
    # ALL Values are base
    
    Int = data_arr[0] # base Interest
    TPrinc = data_arr[1] # base Total Principal
    BY = data_arr[2] # Back Yield
    CI = data_arr[3] # base Cut Indice
    WAM = data_arr[4] 
    

    tdv = 0  # total discount value
    tbs = 0  # total bond size?
    disc = 1+(BY/1200)
    
    for i in range(CI):
        tdv += TPrinc[CI]/disc
        disc *= 1+(BY/1200)
    while CI in range(WAM):
        tdv += (TPrinc[CI]+bInt[CI])/disc
        tbs += TPrinc[CI]
        CI += 1
        disc *= 1+(BY/1200)
        
    return tdv / tbs
    
def helper1(data_arr): 
    # ALL VALUES ARE +300
    
    Princ = data_arr[0]
    Prpy = data_arr[1]
    SPrinc = data_arr[2]
    Int = data_arr[3]
    Yld = data_arr[4]
    i = data_arr[5] # start month
    
    monthly_disc = 1 + (Yld/1200)
    sum_pres_val = 0
    
    while i in range(WAM):
        cashflow_sum = SPrinc[i] + Prpy[i] + Int[i]
        if (i==0):
            prev = 1/monthly_disc
        else:
            prev = prev/monthly_disc
        sum_pres_val += prev*cashflow_sum
        i+=1
    
    return sum_pres_val / (sum(Prpy)+sum(SPrinc))
    
def helper2(data_arr):
    # ALL Values are base
    
    TPrinc = data_arr[0]
    Int = data_arr[1]
    CI = data_arr[2]
    i = data_arr[3] # start_month
    guess_yield = data_arr[4]
    
    tdv = 0
    tbs = 0
    multiplier = 1 + guess+_yield/1200
    disc = multiplier
    
    while i in range(CI):
        tdv += (TPrinc[i]+Int[i])/disc
        tbs += TPrinc[i]
        disc *= multiplier
        i += 1
    
    return tdv/tbs

def helper3(data_arr):
    # ALL data are base
    
    Princ = data_arr[0]
    TPrinc = data_arr[1]
    cut_percent = data_arr[2]
    WAM = data_arr[3]
    CPN = data_arr[4]
    front_yield = data_arr[5]
    back_yield = data_arr[6]
    i = data_arr[7] # start month
    
    fPrinc = [] # front princ
    fInt = [] # front int
    fSUM = 0 # front sum
    bPrinc = [] # back princ
    bInt = [] # back int
    bSUM = 0 # back sum
    
    while i in range(WAM):
        
        if (i==0):
            fPrinc.append(cut_percent*Princ[i])
            bPrinc.append((1-cut_percent)*Princ[i])
        else:
            curr_fPrinc = max(fPrinc[i-1] - TPrinc[i], 0)
            fPrinc.append(curr_fPrinc)
            bPrinc.append(bPrinc[i-1] - TPrinc[i] + fPrinc[i-1] - curr_fPrinc)
            
        fInt.append((CPN/1200) * fPrinc[i])
        bInt.append((CPN/1200) * bPrinc[i])
        
        if (i!=0):
            L = (1+(front_yield/1200))**(i)
            M = (1+(back_yield/1200))**(i)
            
            fSUM += (fInt[i] + fPrinc[i-1] - fPrinc[i]) / L
            bSUM += (bInt[i] + bPrinc[i-1] - bPrinc[i]) / M
            
        i += 1
            
    front_price = fSUM / fPrinc[0]
    back_price = bSUM / bPrinc[0]
    
    return (front_price, back_price)      
    
def YieldToPrice(data_arr, key):
    if (key == 0):
        # formally: yield_to_price_BACK
        return helper0(data_arr)
    
    elif (key == 1):
        # formally: yield_to_price
        return helper1(data_arr)
    
    elif (key == 2):
        # formally:  yield_to_price_FRONT_TWO
        return helper2(data_arr)
        
    elif (key == 3):
        # formally: new_thing
        return helper3(data_arr)
          
def PriceToYield(data_for_YTP2, tgt_price, guess_yield): # im not sure how well this function works
                                            # should be 1.9318
    diff = 100
    mod = 5.0
    curr_data = data_for_YTP2.append(guess_yield)
    
    while not ((diff > -0.001) and (diff < 0.001)):
        
        guess_price = YieldToPrice(data_for_YTP2, 2)
        diff = guess_price - tgt_price
        if (guess_price > tgt_price):
            guess_yield += mod
        else:
            guess_yield -= mod
        mod /= 2
        curr_data[4] = guess_yield
        
    return guess_yield
    
def front_and_back_price(start_month, WAM, CPN, plus300_cut_percent,
                         front_yield, back_yield, Princ, TPrinc):
    # ALL cashflows should be BASE
    
    front_Princ = []
    back_Princ = []
    front_Int = []
    back_Int = []
    front_TDS = []
    back_TDS = []
    front_sum = 0
    back_sum = 0
    
    i = start_month
    j = 0
    
    while i in range(WAM):
        if (i == start_month):
            front_Princ.append(plus300_cut_percent * Princ[i])
            back_Princ.append((1-plus300_cut_percent) * Princ[i])
            curr_FI = (CPN/1200) * front_Princ[j] # front interest
            curr_BI = (CPN/1200) * back_Princ[j] # back interest
        else:
            prev_FP = front_Princ[j-1] # front princ
            prev_BP = back_Princ[j-1] # back princ
            curr_FP = max(prev_FP - TPrinc[i], 0)
            front_Princ.append(curr_FP)
            curr_BP = (prev_BP - TPrinc[i] + prev_FP - curr_FP)
            curr_FI = (CPN/1200) * front_Princ[j] # front interest
            curr_BI = (CPN/1200) * back_Princ[j] # back interest
            L = (1+(front_yield/1200)) ** (j+1)
            M = (1+(back_yield/1200)) ** (j+1)
            front_sum += (curr_FI+prev_FP-curr_FP)/L
            back_sum += (curr_BI+prev_BP-curr_BP)/M
        front_Int.append(curr_FI)
        back_Int.append(curr_BI)            
        i += 1
        j += 1
        
    front_price = front_sum / front_Princ[0]
    back_price = back_sum / back_Princ[0]

    return (front_price, back_price)
