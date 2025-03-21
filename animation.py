#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 14:50:12 2022

@author: rachelodwyer
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
 
# Total population, N.
N = int(input("Type your inital population, N"))
# Initial number of infected and recovered individuals, I0 and R0.
I0 = int(input("How many people initally infected?"))
R0 = 0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
#beta, gamma = 0.2, 1./10
contact_rate = 0.2
recovery_rate = 1./10
# A grid of time points (in days)
t_span = np.linspace(0, 160, 160)
h = t_span[1]-t_span[0]
 
 
# The SIR model differential equations.
def deriv(y, N, contact_rate, recovery_rate):
    S, I, R = y
    dSdt = -contact_rate * S * I / N
    dIdt = contact_rate * S * I / N - recovery_rate * I
    dRdt = recovery_rate * I
    return np.array([dSdt, dIdt, dRdt])
 
 
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
line = [ax.plot([], [], 'b', alpha=0.5, lw=2, label='Susceptible')[0]]
line.append(ax.plot([], [], 'r', alpha=0.5, lw=2, label='Infected')[0])
line.append(ax.plot([], [], 'g', alpha=0.5, lw=2, label='Recovered with immunity')[0])
ax.set_xlabel('Time /days')
ax.set_ylabel('Number (1000s)')
ax.set_ylim(0,1.2)
ax.set_xlim(0,len(t_span))
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(visible=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
    
X = np.empty((3,len(t_span)))*np.nan
X[:,0] = (S0,I0,R0)
 
# initialization function: plot the background of each frame
def init():
    [line[i].set_data([], []) for i in range(3)]
    return line
 
# animation function.  This is called sequentially
def animate(i):
    dX = deriv(X[:,i],N,contact_rate,recovery_rate)
    X[:,i+1] = X[:,i] + h*dX
   
    line[0].set_data(t_span, X[0,:]/1000)
    line[1].set_data(t_span, X[1,:]/1000)
    line[2].set_data(t_span, X[2,:]/1000)
    return line
 
anim =FuncAnimation(fig, animate, init_func=init,
                               frames=len(t_span)-1, interval=20, blit=True)
plt.show()



## 