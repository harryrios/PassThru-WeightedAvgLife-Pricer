# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 18:52:33 2021

@author: Harry Rios

This file contains everything needed for taking in 
    inputs for the PT_WALA_Pricer program...
    
This file contains the following functions:
    getInput -> calls remaining functions and returns inputs
    getTreasuryMatrix -> opens one file, takes in matrix of Treasury Data
    getBaseParameters -> opens one file, takes in basic CMO parameters
    
    
Details on BP_filename (Base Parameters) and TM_filename (Treasury Matrix)
    can be found in the README file under the INPUTS banner.
    
"""

def getBaseParameters(filename):
    # This function returns a list of string
    # representations of the base parameters of 
    # a cmo.
    # lst(str) -> [WAC, CPN, WAM, WALA, OLS, pPSA,
    #               bPSA, price, back_spread]
    
    # If the correct number of inputs are not 
    # counted, 0 is returned.
    
    inFile = open(filename, 'r')
    input_arr = read(inFile).split(',')
    inFile.close()
    
    if (len(input_arr) != 9):
        return 0
    return input_arr
    
#def getTreasuryMatrix(filename):
    

def getInput(BP_filename, TM_filename):
    BP_arr = getBaseParameters(BP_filename)
    #TM_mat = getTreasuryMatrix(TM_filename)
    
    if (BP_arr != 0):
        return (BP_arr, TM_mat)
    else:
        return 0



