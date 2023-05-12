import matplotlib.pyplot as plt
import dill
import numpy as np
from numpy import pi
Ls = [1.2, 1, .5, .6]
state0 = np.array([[45*pi/180], 
                   [0*pi/180], 
                   [0*pi/180],
                   [0*pi/188], 
                   [0], 
                   [0],
                   [0], 
                   [0]]).astype("float64")

thetaddots_F = [dill.load(open(f"thetaddot{i}_F", 'rb')) for i in range(len(Ls))]


class animation():
    def __init__(self):
            self.fig, self.ax = plt.subplots()
            self.ax.set_xlim(-4,4)
            self.ax.set_ylim(-4,4)
            self.init = False
            self.lines = []
            self.trace = 1
            self.ax.set_title("T = ")
            self.x_history = []
            self.y_history = []
    def animate(self, state, T):
        thetas = [state[i][0] for i in range(len(Ls))]
        for i in range(len(Ls)):
            if i == 0: 
                xs = [0, Ls[0]*np.sin(thetas[0])]
                ys = [0, -Ls[0]*np.cos(thetas[0])]
            else     : 
                xs.append(xs[i]+Ls[i]*np.sin(thetas[i]))
                ys.append(ys[i]-Ls[i]*np.cos(thetas[i]))
        self.x_history.append(xs[-1])
        self.y_history.append(ys[-1])
        if len(self.x_history) > 50:
            self.x_history.pop(0)
            self.y_history.pop(0)

        if not self.init:
            for i in range(1, len(Ls)+1, 1):
                if i == 1:
                    self.lines = [self.ax.plot((xs[i-1],xs[i]), (ys[i-1],ys[i]))[0]]
                else:
                    self.lines.append(self.ax.plot((xs[i-1],xs[i]), (ys[i-1],ys[i]))[0])
            self.trace, = self.ax.plot(self.x_history, self.y_history, color='cyan', alpha=.45)
            self.init = True
        else:
            for i in range(1, len(Ls)+1, 1): self.lines[i-1].set_data((xs[i-1],xs[i]), (ys[i-1],ys[i]))
            self.trace.set_data(self.x_history, self.y_history)
            self.ax.set_title(f"T={format(T,'2f')}")
            plt.pause(0.05)

def f(state, force):
    states = [state[i][0] for i in range(len(state))]
    thetaddots = [thetaddots_F[i](*states) for i in range(len(Ls))]
    xdot = np.array(states[int(len(states)/2):len(states)]+thetaddots).reshape(-1,1)
    return xdot

def rk4_step(state, force, Ts):
    F1 = f(state, force)
    F2 = f(state + Ts / 2 * F1, force)
    F3 = f(state + Ts / 2 * F2, force)
    F4 = f(state + Ts * F3, force)
    state += Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)
    return state

def update():
    ani = animation()
    Ts = .05
    T = 0
    state=state0
    for i in range(int(30/Ts)):
        T = T+Ts
        state = rk4_step(state,0,Ts)
        ani.animate(state, T)
update()