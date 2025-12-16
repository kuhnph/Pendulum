'''
This program takes the number of pendulum links and the acceleration due to gravity as inputs
and produces the equations of motion as binary files to be used by main.
'''

import sympy as sp
from sympy import cos, sin
from sympy.physics.mechanics import dynamicsymbols
import dill
import time
import os
dill.settings['recurse'] = True

#INPUTS
links = 5
g = 9.81

#Pre-allocate arrays for use in equations of motion
ms = [sp.symbols(f"m{i}") for i in range(links)]
Ls = [sp.symbols(f"L{i}") for i in range(links)]
thetas = [dynamicsymbols(f"theta{i}") for i in range(links)]
thetaDots = [dynamicsymbols(f"theta{i}", 1) for i in range(links)]
thetaDDots = [dynamicsymbols(f"theta{i}", 2) for i in range(links)]
thetas_2 = [sp.symbols(f"theta_{i}") for i in range(links)]
thetaDots_2 = [sp.symbols(f"thetaDot_{i}") for i in range(links)]
thetaDDots_2 = [sp.symbols(f"thetaDDot_{i}") for i in range(links)]


#loop to generate the equations for pendulum position
for i, L in enumerate(Ls):
    theta = thetas[i]

    if i == 0:
        x = L*sin(theta)
        y = -L*cos(theta)
        pos = [x,y]
    else:
        pos.append(x+L*sin(theta))
        pos.append(y-L*cos(theta))
vel = [sp.diff(pos[i], "t") for i in range(len(pos))]

#loop to solve for the kinetic and potential energy of the pendulums
j=0
for i in range(0, len(vel)-1, 2):
    if i == 0:
        KE = ms[j]*(vel[i]**2+vel[i+1]**2)/2
        PE = ms[j]*g*pos[i+1]
    else:
        KE = KE + ms[j]*(vel[i]**2+vel[i+1]**2)/2
        PE = PE+ms[j]*g*pos[i+1]
    j+=1

#The Lagrangian
L = KE-PE
LEs = [(sp.diff(sp.diff(L,thetaDots[i]), 't')-sp.diff(L,thetas[i])).simplify() for i in range(len(Ls))]

for i in range(len(LEs)):
    for ii in range(len(thetaDDots_2)):
        LEs[i] = LEs[i].subs([(thetaDDots[ii], thetaDDots_2[ii]), (thetaDots[ii], thetaDots_2[ii]),  (thetas[ii], thetas_2[ii])])


print('solving')
T_start = time.time()
sol = sp.solve(LEs, thetaDDots_2)
print(f"solve time = {format(time.time()-T_start, '2f')}")

print('simplifying')
for i in range(len(Ls)):
    sol[thetaDDots_2[i]] = sol[thetaDDots_2[i]].simplify()

print("lambdifying")
thetaDDots_F = [sp.lambdify(thetas_2+thetaDots_2+ms+Ls, sol[thetaDDots_2[i]]) for i in range(len(Ls))]


CD = os.getcwd()
for file in os.listdir(CD):
    if 'theta' in file:
        os.remove(file)

#Remove and add new dills
toRemove = os.listdir("assets")
for asset in toRemove:
    os.remove(os.path.join("assets",asset))
for i in range(len(Ls)):
    dill.dump(thetaDDots_F[i], open(os.path.join("assets",f"thetaddot{i}_F"), "wb"))

#Generate main to reflect the number of coupled pendulums
with open('main.py','w') as f:
    f.write("\
from src.pendulum_animation import create_figure, update\n\
import numpy as np\n\
fig,ax,bg = create_figure()\n")
    
    for i in range(links):
        f.write(f'pendulumAngle{i} = np.radians(0)\n')
    f.write('\n')

    for i in range(links):
        f.write(f'initialVelocity{i} = np.radians(0)\n')
    f.write('\n')

    f.write('angles = [')
    for i in range(links):
        f.write(f'pendulumAngle{i},') if i != links-1 else f.write(f'pendulumAngle{i}]')
    f.write('\n')
    f.write('velocities = [')
    for i in range(links):
        f.write(f'initialVelocity{i},') if i != links-1 else f.write(f'initialVelocity{i}]')
    f.write(f'\nstate = np.array([angles+velocities]).T\n\n')


    for i in range(links):
        f.write(f'pendulumLength{i} = .25\n')
    f.write('lengths = [')
    for i in range(links):
        f.write(f'pendulumLength{i},') if i != links-1 else f.write(f'pendulumLength{i}]')
    f.write('\n\n')

    for i in range(links):
        f.write(f'pendulumMass{i} = .25\n')
    f.write('masses = [')
    for i in range(links):
        f.write(f'pendulumMass{i},') if i != links-1 else f.write(f'pendulumMass{i}]')
    f.write('\nplay = update([state],[lengths],[masses],.01,20,fig,ax,bg)')