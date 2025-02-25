# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 09:40:04 2022

@author: Fermin Mallor
"""
import numpy as np

def boundary_cond(U):
    # In this function, boundary conditions for the shock tube
    # should be implemented
    # The boundary conditions are: 
    # u(0,t)=u(L,t) = 0  => rho*u = 0 at both ends
    # rho should be extrapolated at both ends
     
    #### Here you have to implement the boudary conditions !!!
    U[0,0] = U[1,0]
    U[-1,0] = U[-2,0]
    U[0,1] = 0
    U[-1,1] = 0
    return U