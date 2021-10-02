def PSA(BP_arr, PSA):
    # BP_arr -> lst(str)
    #   [WAC, CPN, WAM, WALA, OLS, pPSA, bPSA, price, back_spread]
    # PSA -> float, can be +300 or BASE    OLS = float(BP_arr[4])
    WAC = float(BP_arr[0])
    WAM = float(BP_arr[2]) 
    OLS = float(BP_arr[4])
    
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
    
    sumCPR = 0
    
    Princ_arr = []
    Int_arr = [] 
    SPrinc_arr = []
    Prpy_arr = []
    TPrinc_arr = []
    
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
        
        Princ_arr.append(cPrinc)
        Int_arr.append(cInt)
        SPrinc_arr.append(cSPrinc)
        Prpy_arr.append(cPrpy)
        TPrinc_arr.append(cTPrinc)
        
        pPrinc  = cPrinc
        pPrpy = cPrpy
        pSPrinc = cSPrinc
        pScdBal = ScdBal
        i+=1
            
    PSA_mat = [Princ_arr, Int_arr, SPrinc_arr, Prpy_arr, TPrinc_arr]
    return PSA_mat

# OUTPUTS -> PSA_MATRIX
    # ROWS : principal, interest, scheduled principal, prepayment, total principal
    # COlS : months 1 thru 360

def WAL_months(SPrinc_arr, Prpy_arr, Princ_arr, WAM, start):
    # ALL cashflows are +300
    
    sumprod_SPrinc = 0
    sumprod_Prpy = 0
    i = start
    
    while i in range(WAM):
        sumprod_SPrinc += (i+1)*SPrinc_arr[i] 
        sumprod_Prpy += (i+1)*Prpy_arr[i]
        i += 1
        
    WAL_months = []
    i = start
    
    while i in range(WAM):
        WM = (sumprod_SPrinc+sumprod_Prpy)/Princ_arr[i] - (i+1)
        WAL_months.append(WM)
        sumprod_SPrinc -= (i+1)*SPrinc_arr[i] 
        sumprod_Prpy -= (i+1)*Prpy_arr[i]
        i += 1
        
    return WAL_months
    
def cutting(TPrinc_arr, SPrinc_arr, Princ_init, WAM, start): # double check this works with appropreite data
    # ALL cashflows are +300
    
    curr_size = 0
    dividend = 0
    avg_life = 0
    i = start
    
    while (avg_life < 6.99) and (i < int(WAM)):
        curr_size += TPrinc_arr[i]
        dividend += TPrinc_arr[i] * (i+1)
        avg_life = (dividend/curr_size)/12
        i+=1
    i -= 1
    cut_percent = (curr_size - TPrinc_arr[i])/Princ_init
    return (cut_percent, i)
    
def front_and_back_WAL(TPrinc_arr, Princ_arr, WAM, cut_percent, start):
    # ALL cashflows are BASE
    
    sumprod = 0
    div = 0
    i = start
    
    while (div/Princ_arr[i]) <= cut_percent:
        sumprod += (i+1) * TPrinc_arr[i]
        div += TPrinc_arr[i]
        i += 1
    i -= 1
    cut_ind = i
    
    sumprod -= (i+1) * TPrinc_arr[i]
    div -= TPrinc_arr[i]
    front_WAL = (sumprod / div) / 12
    
    sumprod = 0
    div = 0
    
    while i in range(WAM):
        sumprod += (i+1) * TPrinc_arr[i]
        div += TPrinc_arr[i]
        i+=1
    i-=1
    sumprod -= (i+1) * TPrinc_arr[i]
    div -= TPrinc_arr[i]
    back_WAL = (sumprod / div) / 12
    
    return (front_WAL, back_WAL, cut_ind)
    
    
