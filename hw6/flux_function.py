# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 09:42:07 2022

@author: Fermin Mallor
"""

import numpy as np

def flux_function(U,Kentr,GAMMA):
    # This function should be completed by computing the flux:
    #        rho*u
    # F(U) = 
    #        rho*u^2 + p
    
    # F(U) should be stored in the same way as the conservative
    # variables
    # 
    # F[:,0] = rho*u
    # F[:,1] = rho*u^2 + p
    # 
    #### Here you have to define the flux function!!!!
    F = np.zeros(np.shape(U))

    if np.any(U[:,0] <= 0): print(f'U[:,0]: {U[:,0]}')
    
    F[:,0] = U[:,1] # rho*u
    F[:,1] = U[:,1] * U[:,1] / U[:,0] + Kentr * U[:,0] ** GAMMA # rho*u^2 + p
    return F
