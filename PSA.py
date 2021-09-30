def PSA(BP_arr, PSA):
    # BP_arr -> lst(str)
    #   [WAC, CPN, WAM, WALA, OLS, pPSA, bPSA, price, back_spread]
    # PSA -> float, can be +300 or BASE
    
    OLS = float(BP_arr[4])
    WAC = float(BP_arr[0])
    WAM = float(BP_arr[2]) 
    
    i = 0 # current month
    
    cPrinc = OLS # current principal, init at OLS
    cInt = 0 # current interest
    cSPrinc = 0 # current scheduled principal
    cPrpy = 0 # current prepayment
    cTPrinc = 0 # curent total principal
    
    pPrinc = 0 # previous principal
    pPrpy = 0 # previous prepayment
    pSPrinc = 0 # previous scheduled principal
    pScdBal = 0 # previous scheduled balance
    
    PSA_mat = []
    # ROWS : principal, interest, scheduled principal, prepayment, total principal
    # COlS : months 1 thru 360
    
    sumCPR = 0
    
    while (i<WAM):
        top = 1 - (1 + (WAC / 1200)) ** (-1 * (WAM - i-1))
        bot = 1 - (1 + (WAC / 1200)) ** (-1 * WAM)
        ScdBal = 1 - (top/bot) # Scheduled Balance
        
        cprPSA = min(i+1, 30) * .2 * PSA / 100
        smmPSA = 1-((1-(cprPSA/100))**(1/12))
        
        cInt = (float(BP_arr[1]) / 1200) * cPrinc
        
        if (i == 0): # it is the first month
            cSPrinc = ScdBal * cPrinc
        else:
            cPrinc = max(pPrinc - pPrpy  - pSPrinc, 0)
            cSPrinc = (ScdBal - pScdBal) * (OLS - sumCPR)
        
        cPrpy = (cPrinc - cSPrinc) * smmPSA
        cTPrinc = min(cPrpy + cSPrinc, cPrinc)
            
        try:
            sumCPR += cPrpy / (1-ScdBal)
        except:
            pass
        
        PSA_mat.append([cPrinc, cInt, cSPrinc, cPrpy, cTPrinc])
        
        pPrinc  = cPrinc
        pPrpy = cPrpy
        pSPrinc = cSPrinc
        pScdBal = ScdBal
        i+=1
            
    return PSA_mat

