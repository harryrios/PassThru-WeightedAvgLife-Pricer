# # -*- coding: utf-8 -*-
# """
# Created on Fri Oct  1 18:22:16 2021

# @author: Harry Rios

# This file contains the following functions:
# Yield to Price and Price to Yield
# Yield to Price has multiple subfunctions are requires
# the appropriete data plus a key to run the right subfunction

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
    
    monthly_disc = 1 + (Yld/1200)
    sum_pres_val = 0
    
    for i in range(WAM):
        cashflow_sum = SPrinc[i] + Prpy[i] + Int[i]
        
        if (i==0):
            prev = 1/monthly_disc
        else:
            prev = prev/monthly_disc
        sum_pres_val += prev*cashflow_sum
    
    return sum_pres_val / (sum(Prpy)+sum(SPrinc))
    
def helper2(data_arr):
    # ALL Values are base
    
    TPrinc = data_arr[0]
    Int = data_arr[1]
    guess_yield = data_arr[2]
    CI = data_arr[3]
    
    tdv = 0
    tbs = 0
    multiplier = 1 + guess+_yield/1200
    disc = multiplier
    
    for i in range(CI):
        tdv += (TPrinc[i]+Int[i])/disc
        tbs += TPrinc[i]
        disc *= multiplier
    
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
    
    fPrinc = [] # front princ
    fInt = [] # front int
    fSUM = 0 # front sum
    bPrinc = [] # back princ
    bInt = [] # back int
    bSUM = 0 # back sum
    
    for i in range(WAM):
        
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
          
def PriceToYield(data_arr): # im not sure how well this function works
    
    data_for_YTP2 = data_arr[0]
    tgt_price = data_arr[1]
    guess_yield = data_arr[2] # should be 1.9318
    
    diff = 100
    mod = 5.0
    
    while not ((diff > -0.001) and (diff < 0.001)):
        guess_price = YieldToPrice(data_for_YTP2, 2)
        diff = guess_price - tgt_price
        
        if (guess_price > tgt_price):
            guess_yield += mod
        else:
            guess_yield -= mod
            
        mod /= 2
    return guess_yield
    
