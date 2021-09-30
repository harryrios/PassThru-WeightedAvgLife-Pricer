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
    
    inFile = open(filename, 'r')
    input_arr = inFile.read().split(',')
    inFile.close()

    return input_arr
    
def getTreasuryMatrix(filename):
    # This fucntion returns a tuple containing
    # the treasury data, including a start date
    # for which there is no treasury rate.
    
    # SD: lst(str) -> [month, year]
    # TM: lst(str) -> [month, year, rate]
    
    TM_mat = []
    inFile = open(filename, 'r')
    isFirst = True
    for line in inFile:
        if isFirst:
            SD = line.strip('\n').split(',')
            isFirst = False
        else:
            TM_vect = line.strip('\n').split(',')
            TM_mat.append(TM_vect)
    inFile.close()
    
    return (SD, TM_mat)

def getInput(BP_filename, TM_filename):
    BP_arr = getBaseParameters(BP_filename) #Basic Parameters
    tmp = getTreasuryMatrix(TM_filename)
    TM_mat = tmp[1] #Treasury Data
    SD = tmp[0] #Start Date

    return (BP_arr, SD, TM_mat)


