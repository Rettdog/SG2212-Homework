# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 09:42:43 2022

@author: Fermin Mallor
"""
import numpy as np
from boundary_cond import boundary_cond
from flux_function import flux_function
from artificial_visc import artificial_visc
from dx import dudx

def mac_cormack(U,dt,Kentr,GAMMA,DX,C2,C0):
    # McCormack's scheme for system of 1D conservation laws
    #
    # du/dt + d/dx(F + F_A) = 0
    # F    = convective flux             
    # F_A  = artificial viscous flux    
    # 
    # The artificial viscosity function has a flag to tell which
    # one-sided difference to use.
    U = boundary_cond(U)            # Set boundary conditions:
    print(f'U:{U}')
    F = flux_function(U,Kentr,GAMMA)            # Compute flux function:          
    print(f'F:{F}')
    F = F - artificial_visc(-1,U,Kentr,GAMMA,DX,C2,C0)   # Add artificial viscosity
    print(f'F:{F}')
    tmp = dudx(+1, F, DX)
    print(f'tmp:{tmp}')                       # Take a forward difference of the
                                    # flux (predictor step)
                                    # The 'dx' function can take the derivatives
                                    # in three directions,(forward, backward,
                                    # and central)    			       
                                    
    Up = U - dt * tmp                   # Update solution according to 
                                    # predictor step equation (7)   
    print(f'Up:{Up}')             
    Up = boundary_cond(Up)          # Set boundary conditions on
                                    # predictor, Up                          
                                    
    F = flux_function(Up,Kentr,GAMMA)           # Compute flux function using Up            
    # print(F.shape,U.shape)
    F = F - artificial_visc(+1,Up,Kentr,GAMMA,DX,C2,C0)  # Add artificial viscosity   
    
    tmp = dudx(-1,F,DX)                # Take a backward difference of the
                                    # flux (corrector step)   
                                    
    Unew = 0.5*(U + Up - dt*tmp)    # Update solution     

    return Unew