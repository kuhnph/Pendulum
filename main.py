from src.pendulum_animation import create_figure, update
import numpy as np
fig,ax,bg = create_figure()
pendulumAngle0 = np.radians(0)
pendulumAngle1 = np.radians(0)

initialVelocity0 = np.radians(0)
initialVelocity1 = np.radians(0)

angles = [pendulumAngle0,pendulumAngle1]
velocities = [initialVelocity0,initialVelocity1]
state = np.array([angles+velocities]).T

pendulumLength0 = .25
pendulumLength1 = .25
lengths = [pendulumLength0,pendulumLength1]

pendulumMass0 = .25
pendulumMass1 = .25
masses = [pendulumMass0,pendulumMass1]
play = update([state],[lengths],[masses],.01,20,fig,ax,bg)