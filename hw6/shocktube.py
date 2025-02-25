# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 09:38:56 2022

@author: Fermin Mallor
"""

import numpy as np
import matplotlib.pyplot as plt
from mac_cormack import mac_cormack

#        Barotropic shock tube solved by McCormack scheme
#        ------------------------------------------------
# At t = 0:
#  	Rho |
#       +---------
#       |         |
#       |         |
#       |          --------
#       +---------+--------+--> X
#       0        L/2       L
# Solve the Riemann problem. At both ends, the tube is closed
# so u = 0. Equations:
#     d(rho)/dt + d(rho*u)dx = 0
#     d(rho*u)/dt + d(rho*u*u + p)/dx = 0
# 
# ==============================================================
# !!!!!!!!!!  READ THIS BEFORE YOU START !!!!!!!!!!!!!!!!!!!!!!!
#  
# 
# U in the program is the matrix of conservative varibles: rho and
# rho*u stored as columns in the matrix U
#     
#       rho_1     (rho*u)_1
#       rho_2     (rho*u)_2
# U =    .           .
#        .           .
#       rho_n     (rho*u)_n 
# 
# 
# rho = U(:,1)  and  u=U(:,2)./rho
#
# rho: Density
# uu  : Velocity
# p  : Pressure
# Kentr = K (in the homework)

# Constants
GAMMA  = 1.4  
R      = 288.7   # 8.314 J/K.mol = 8.314 *1000/(0.8*28 + 0.2*32) =
                  # 288.7 J/kg/K

# Compute initial state:
# Left conditions:
P0      = 1e5                   # Pa
T0      = 300                   # K
RHO0    = P0/T0/R               # kg/m^3
Kentr   = P0/RHO0**GAMMA         # isentropic relation
print(Kentr)

# Right conditions:
P1      = 1e4                   # Pa, atmosphere 
RHO1    = (P1/Kentr)**(1/GAMMA)  # kg/m^3, isentropic relation

# Tube geometry:
L  = 3                          # m

# Grid:
n  = 81 
X  = np.linspace(0,L,n)
DX = X[1]-X[0]

# Initial conditions:
U      = np.zeros((n,2))             # allocate U, uu zero 
U[:,0] = RHO0*np.ones(n)         # density left
I      = (X > L/2)          # right half of tube
U[I,0] = RHO1*np.ones(np.sum(I)) # density right

# Artificial viscosity, try other parameter values
C0 = 0.05
C2 = 0.25

#  Courant number, try with different
CN = 0.9

nstp   = 50                     # number of timesteps
rho  = U[:,0]
uu    = U[:,1]/rho
p    = Kentr*rho**GAMMA # added here so that p exists as a vector in first time step as well

fig2, ax2 = plt.subplots(3)

for k in range(nstp):
  ### !!!Here you have to add something to determine the timestep!!!! 
  
  # 1) Find the speed of sound
  c = np.sqrt(GAMMA * p/rho) # Currently just getting values for one side and assuming it is constant which it isn't
  
  # 2) Compute vmax, maximal, absolute value of the characteristic speeds
  umax = max(np.max(np.abs(uu+c)), np.max(np.abs(uu-c))) # lambda = u+-c
   
  # 3) Determine the time step using the CFL condition 
  #    and the Courant number, CN
  dt = CN * np.min(DX) / umax 
  print(f'dt: {dt}')

  U = mac_cormack(U,dt,Kentr,GAMMA,DX,C2,C0);      # Use MacCormack to update the solution
  
  # Decode the variables:
  rho  = U[:,0]
  uu   = U[:,1]/rho; 
  p    = Kentr*rho**GAMMA

  
  # Plot 
  if k == 1:          # plot initial condition
    fig1, ax1 = plt.subplots(3)
    ax1[0].plot(X,rho,'r'), 
    ax1[0].set_title('Density')
    ax1[1].plot(X,uu,'b')
    ax1[1].set_title('Velocity')
    ax1[2].plot(X,p,'m') 
    ax1[2].set_title('Pressure')
    fig1.suptitle('Initial condition')
    fig1.tight_layout()
  # Look at the density, 
  # pressure and velocity
  if k%4 == 0:          # plot every fourth time step 
    ax2[0].plot(X,rho,'r'), 
    ax2[0].set_title('Density')
    ax2[1].plot(X,uu,'b')
    ax2[1].set_title('Velocity')
    ax2[2].plot(X,p,'m') 
    ax2[2].set_title('Pressure') 
    # fig2.canvas.draw()
# plot the solution at the end time
fig3, ax3 = plt.subplots(3)
ax3[0].plot(X,rho,'-+')
ax3[0].grid()
ax3[0].set_title('Density')
ax3[1].plot(X,uu,'-+')
ax3[0].grid()
ax3[0].set_title('Velocity')
ax3[2].plot(X,p,'-+')
ax3[2].grid()
ax3[2].set_title('Pressure')
fig3.tight_layout()

plt.show()
