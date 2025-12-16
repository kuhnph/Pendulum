from src.pendulum_animation import create_figure, update
import numpy as np
fig,ax,bg = create_figure()
pendulumAngle0 = np.radians(90)
pendulumAngle1 = np.radians(60)
pendulumAngle2 = np.radians(40)
pendulumAngle3 = np.radians(90)
pendulumAngle4 = np.radians(90)

initialVelocity0 = np.radians(0)
initialVelocity1 = np.radians(0)
initialVelocity2 = np.radians(0)
initialVelocity3 = np.radians(0)
initialVelocity4 = np.radians(200)

angles = [pendulumAngle0,pendulumAngle1,pendulumAngle2,pendulumAngle3,pendulumAngle4]
velocities = [initialVelocity0,initialVelocity1,initialVelocity2,initialVelocity3,initialVelocity4]
state = np.array([angles+velocities]).T

pendulumLength0 = .25
pendulumLength1 = .25
pendulumLength2 = .25
pendulumLength3 = .25
pendulumLength4 = .25
lengths = [pendulumLength0,pendulumLength1,pendulumLength2,pendulumLength3,pendulumLength4]

pendulumMass0 = .25
pendulumMass1 = .25
pendulumMass2 = .25
pendulumMass3 = .25
pendulumMass4 = .25
masses = [pendulumMass0,pendulumMass1,pendulumMass2,pendulumMass3,pendulumMass4]
play = update([state],[lengths],[masses],.005,20,fig,ax,bg)