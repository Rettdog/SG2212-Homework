# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 09:03:46 2022

@author: Fermin Mallor
"""

import numpy as np
from dx import dudx

def artificial_visc(direction,U,Kentr,GAMMA,DX,C2,C0):
    m,n = np.shape(U)
    # Artificial dissipative flux
    # DX (abs(u) + c)*(C2*sw  + C0) dx(u)
    # sw density switch
    # (abs(u) + c) velocity scaling
    # decode
    rho = U[:,0]
    uu = U[:,1]/rho
    # density switch
    sw      = np.abs(np.diff(np.diff(rho)))
    sw = np.concatenate(([sw[0]],sw,[sw[-1]]))
    den     = np.copy(rho)
    den[1:-1] = den[0:-2] + 2*den[1:-1] + den[2:]
    sw           = 2*sw/den
    
    # add the speed of sound
    c = np.sqrt(GAMMA * Kentr * rho ** (GAMMA-1))

    # add Vs (velocity scaling)
    Vs = max(np.max(np.abs(uu+c)), np.max(np.abs(uu-c)))
    Q = DX*Vs*(C2*np.matmul(np.expand_dims(sw,1),np.ones((1,2))) + C0)* dudx(direction,U,DX)
    return Q