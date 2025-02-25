# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 09:40:04 2022

@author: Fermin Mallor
"""
import numpy as np

def dudx(direction,U,DX):
    m = np.shape(U)[0]
    # manages the system case where u contains several
    # variables = columns
    ODX  = 1/DX;
    dudx = np.zeros(np.shape(U))
    if direction == 1:           # forward
       dudx[:m-1] =(U[1:]-U[:-1])*ODX
    elif direction == -1:          # rearward
       dudx[1:] = (U[1:]-U[:-1])*ODX
    else:					  # central
       dudx[1:-1] = 0.5*(U[2:]-U[:-2])*ODX
    return dudx

