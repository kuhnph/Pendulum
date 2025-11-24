import matplotlib.pyplot as plt
import dill
import numpy as np
import os
import sys
import matplotlib.animation as animation
# get project root (one directory up from /src)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# path to the assets folder
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
sys.path.append(ASSETS_DIR)

def create_figure(xmin=-3, xmax=3, ymin=-3, ymax=3, height=5, width=5):
    fig, ax = plt.subplots()
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    fig.set_size_inches(height,width)
    return fig, ax

class pendAnimation():
    def __init__(self, Ls):
            self.Ls = Ls
            self.init = False
            self.lines = []
            self.trace = 1
            self.x_history = []
            self.y_history = []

    def pendAnimate(self, state, T, fig, ax):
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
            return [*self.lines, self.trace, self.text]
        else:
            for i in range(1, len(self.Ls)+1, 1): self.lines[i-1].set_data((xs[i-1],xs[i]), (ys[i-1],ys[i]))
            self.trace.set_data(self.x_history, self.y_history)
            tx = f"T={format(T,'2f')}"
            self.text.set_text(tx)
            
        return [*self.lines, self.trace, self.text]
    
class pendulum():
    def __init__(self, ms, Ls):
        self.state = []
        self.ms = ms
        self.Ls = Ls
        self.thetaddots_F = [dill.load(open(os.path.join(ASSETS_DIR,f"thetaddot{i}_F"), 'rb')) for i in range((len(ms)))]
    def f(self, state):
        states = [state[i][0] for i in range(len(state))]
        states_vars = states+self.ms+self.Ls
        thetaddots = [self.thetaddots_F[i](*states_vars) for i in range(len(self.Ls))]
        xdot = np.array(states[int(len(states)/2):len(states)]+thetaddots).reshape(-1,1)
        return xdot

    def rk4_step(self, state, Ts):
        F1 = self.f(state)
        F2 = self.f(state + Ts / 2 * F1)
        F3 = self.f(state + Ts / 2 * F2)
        F4 = self.f(state + Ts * F3)
        state += Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)
        return state

class update():
    def __init__(self, state0s, Lss, mss, T_total, fig, ax, fps=30):
        self.Lss = Lss
        self.mss = mss
        self.Ts = 1/fps
        self.T_total = T_total
        self.fig = fig
        self.ax = ax
        self.states = [i for i in state0s]
        self.anis = [pendAnimation(Lss[i]) for i in range(len(self.states))]
        self.pens = [pendulum(mss[i], Lss[i]) for i in range(len(self.states))]
        self.T = 0
        self.fps = fps
    def update(self, i):
        self.T = self.Ts+self.T
        for i in range(len(self.states)): self.states[i] = self.pens[i].rk4_step(self.states[i], self.Ts)
        artists = [self.anis[i].pendAnimate(self.states[i], self.T, self.fig, self.ax) for i in range(len(self.states))]
        return np.hstack(artists)
    def funk(self, playback_speed=1.0, save=True):
        frameCount = int(self.T_total/self.Ts)
        interval_ms = (1000 / self.fps) / playback_speed

        print(f'saving\ntotal frames: {frameCount}')
        anim = animation.FuncAnimation(self.fig, self.update,
                        frames=frameCount, interval=interval_ms, blit=True)
        anim.save('pendulum.gif', writer='imagemagick', fps=60)