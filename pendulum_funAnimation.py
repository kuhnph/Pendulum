import matplotlib.pyplot as plt
import dill
import numpy as np
from matplotlib.animation import FuncAnimation

def create_figure(xmin=-3, xmax=3, ymin=-3, ymax=3, height=4, width=4):
    fig, ax = plt.subplots()
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    fig.set_size_inches(height,width)

    return fig, ax

class animation():
    def __init__(self, Ls):
            self.Ls = Ls
            self.init = False
            self.lines = []
            self.trace = 1
            self.x_history = []
            self.y_history = []

    def animate(self, state, T, fig, ax):
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
        self.thetaddots_F = [dill.load(open(f"thetaddot{i}_F", 'rb')) for i in range((len(ms)))]
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
    def __init__(self, state0s, Lss, mss, T_total, fig, ax, fps=24):
        self.Lss = Lss
        self.mss = mss
        self.Ts = T_total/(fps*T_total)
        self.T_total = T_total
        self.fig = fig
        self.ax = ax
        self.states = [i for i in state0s]
        self.anis = [animation(Lss[i]) for i in range(len(self.states))]
        self.pens = [pendulum(mss[i], Lss[i]) for i in range(len(self.states))]
        self.T = 0
        self.fps = fps
    def update(self, i):
        self.T = self.Ts+self.T
        for i in range(len(self.states)): self.states[i] = self.pens[i].rk4_step(self.states[i], self.Ts)
        artists = [self.anis[i].animate(self.states[i], self.T, self.fig, self.ax) for i in range(len(self.states))]
        return np.hstack(artists)
    def funk(self, save=True):
        anim = FuncAnimation(self.fig, self.update,
                        frames=int(self.T_total/self.Ts), interval=self.Ts, blit=True)
        anim.save('pendulum.gif', "Pillow", self.fps)