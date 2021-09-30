# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 18:52:33 2021

@author: Harry Rios

This file contains the main function
     for the PT_WALA_Pricer program...
     
     PT -> Pass Through
     WALA -> Weighted Average Loan Agea
    
"""

from InputManager import getInput, getBaseParameters, getTreasuryMatrix
from PSA import PSA

def main():
    # Call to getInput to init inputs
    TM_filename = "TM.txt"
    BP_filename = "BP.txt"
    tmp = getInput(BP_filename, TM_filename)
    
    BP_arr = tmp[0] # Base Parameters -> lst(str)
    start_arr = tmp[1] # Start Date -> lst(str)
    TM_mat = tmp[2] # Treasury Data -> lst(lst(str))
    
    print(len(PSA(BP_arr, float(BP_arr[5]))))
     
main()
