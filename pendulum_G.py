import matplotlib.pyplot as plt
import dill
import numpy as np
from numpy import pi
import time
import matplotlib.animation as animate

def create_figure():
    fig, ax = plt.subplots()
    ax.set_xlim(-3,3)
    ax.set_ylim(-3,3)
    fig.canvas.draw()
    # fig.set_size_inches(12,6)

    # cache the background
    plt.pause(.0001)
    bg = fig.canvas.copy_from_bbox(ax.bbox)
    plt.show(block=False)
    return fig, ax, bg

class animation():
    def __init__(self, Ls):
            self.Ls = Ls
            self.init = False
            self.lines = []
            self.trace = 1
            self.x_history = []
            self.y_history = []

    def animate(self, state, T, fig, ax, bg):
        thetas = [state[i][0] for i in range(len(self.Ls))]
        
        for i in range(len(self.Ls)):
            if i == 0: 
                xs = [0, self.Ls[0]*np.sin(thetas[0])]
                ys = [0, -self.Ls[0]*np.cos(thetas[0])]
            else     : 
                xs.append(xs[i]+self.Ls[i]*np.sin(thetas[i]))
                ys.append(ys[i]-self.Ls[i]*np.cos(thetas[i]))

        self.x_history.append(xs[-1])
        self.y_history.append(ys[-1])

        if len(self.x_history) > 50:
            self.x_history.pop(0)
            self.y_history.pop(0)

        if not self.init:
            for i in range(1, len(self.Ls)+1, 1):
                if i == 1: self.lines = [ax.plot((xs[i-1],xs[i]), (ys[i-1],ys[i]))[0]]
                else     :self.lines.append(ax.plot((xs[i-1],xs[i]), (ys[i-1],ys[i]))[0])

            self.trace, = ax.plot(self.x_history, self.y_history, alpha=.45)
            self.text = ax.text(0.8,0.5, '')
            self.init = True
        else:
            for i in range(1, len(self.Ls)+1, 1): self.lines[i-1].set_data((xs[i-1],xs[i]), (ys[i-1],ys[i]))
            self.trace.set_data(self.x_history, self.y_history)
            tx = f"T={format(T,'2f')}"
            self.text.set_text(tx)

            artists = [*self.lines, self.trace, self.text]
            return artists
   
    def make(self, artists, fig, ax, bg):
        fig.canvas.restore_region(bg)
        for artists2 in artists: 
            for i in artists2: ax.draw_artist(i)
        fig.canvas.blit(ax.bbox)
        fig.canvas.flush_events()

class pendulum():
    def __init__(self, ms, Ls):
        self.state = []
        self.ms = ms
        self.Ls = Ls
    def f(self, state):
        states = [state[i][0] for i in range(len(state))]
        states_vars = states+self.ms+self.Ls
        thetaddots = [thetaddots_F[i](*states_vars) for i in range(len(self.Ls))]
        xdot = np.array(states[int(len(states)/2):len(states)]+thetaddots).reshape(-1,1)
        return xdot

    def rk4_step(self, state, Ts):
        F1 = self.f(state)
        F2 = self.f(state + Ts / 2 * F1)
        F3 = self.f(state + Ts / 2 * F2)
        F4 = self.f(state + Ts * F3)
        state += Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)
        return state


n = 4
thetaddots_F = [dill.load(open(f"thetaddot{i}_F", 'rb')) for i in range(n)]
state0_1 = np.array([[159.999*pi/180], 
                     [159.999*pi/180], 
                     [159.999*pi/180],
                     [159.999*pi/188], 
                     [0], 
                     [0],
                     [0], 
                     [0]]).astype("float64")
state0_2 = np.array([[159.998*pi/180], 
                     [159.998*pi/180], 
                     [159.998*pi/180],
                     [159.998*pi/188], 
                     [0], 
                     [0],
                     [0], 
                     [0]]).astype("float64")
state0_3 = np.array([[159.997*pi/180], 
                     [159.997*pi/180], 
                     [159.997*pi/180],
                     [159.997*pi/188], 
                     [0], 
                     [0],
                     [0], 
                     [0]]).astype("float64")
state0_4 = np.array([[159.996*pi/180], 
                     [159.996*pi/180], 
                     [159.996*pi/180],
                     [159.996*pi/188], 
                     [0], 
                     [0],
                     [0], 
                     [0]]).astype("float64")
fig, ax, bg = create_figure()
Ls = [.5,.5,.5,.5]
ms = [1,1,1,1]

ani = animation(Ls)
ani2 = animation(Ls)
ani3 =animation(Ls)
ani4 = animation(Ls)

pen1 = pendulum(ms, Ls)
pen2 = pendulum(ms, Ls)
pen3 = pendulum(ms, Ls)
pen4 = pendulum(ms, Ls)
Ts = .03
T_0 = 0
T_total = 20

T_start = time.time()
frames = int(T_total/Ts)

def update():
    for i in range(frames):
        if i == 0: T = T_0
        T = T+Ts
        state1=state0_1
        state2=state0_2
        state3=state0_3
        state4=state0_4
        state1 = pen1.rk4_step(state1,Ts)
        state2 = pen2.rk4_step(state2,Ts)
        state3 = pen3.rk4_step(state3,Ts)
        state4 = pen4.rk4_step(state4,Ts)

        artists1 = ani.animate(state1, T, fig, ax, bg)
        artists2 = ani2.animate(state2, T, fig, ax, bg)
        artists3 = ani3.animate(state3, T, fig, ax, bg)
        artists4 = ani4.animate(state4, T, fig, ax, bg)

        if i > 1: ani.make([artists1, artists2, artists3, artists4], fig, ax, bg)
        #time.sleep(.5)
    print(f"run time = {format(time.time()-T_start, '2f')}")
update()