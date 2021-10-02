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

def WAL_months(sched_princ_arr, prepay_arr, princ_arr, WAM):
    sumprod_SchedPrinc = 0
    sumprod_Prepay = 0
    
    for i in range(WAM):
        sumprod_SchedPrinc += (i+1)*sched_princ_arr[i] 
        sumprod_Prepay += (i+1)*prepay_arr[i]
        
    WAL_months = []
    
    for i in range(WAM):
        WM = (sumprod_SchedPrinc+sumprod_Prepay)/princ_arr[i] - (i+1)
        WAL_months.append(WM)
        sumprod_SchedPrinc -= (i+1)*sched_princ_arr[i] 
        sumprod_Prepay -= (i+1)*prepay_arr[i]
        
    return WAL_months
    
def cutting():
    
    
    
    # def step_one(self):
    #     curr_size = 0
    #     dividend = 0
    #     avg_life = 0
    #     i = 0
        
    #     while (avg_life < 6.99) and (i+self.SM < len(self.pTLPR)):
    #         curr_month = i + self.SM
    #         curr_size += self.pTLPR[curr_month-1]
    #         dividend += self.pTLPR[curr_month-1] * (i+1)
    #         avg_life = ((dividend / curr_size)) / 12
    #       #  print(curr_month, self.pSCPR[curr_month-1]+self.pTLPR[curr_month-1])
    #         i+=1
            
    #     # ---- output ---- #
    #     cut_percent = (curr_size- self.pTLPR[curr_month]) / self.pPRNC[self.SM-1]
    #     #print('CP ', cut_percent)
    #     cut_ind = i + self.SM - 2
        
    #     return (cut_percent, cut_ind)
    
