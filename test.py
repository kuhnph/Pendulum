from pendulum_animation import create_figure, update
import numpy as np
fig,ax,bg = create_figure()
pend1 = np.array([[1.5],[1.5],[1.5],[0],[0],[0]])
pend2 = np.array([[1.6],[1.5],[1.5],[0],[0],[0]])
Lss = [[.5,.5,.5],
       [.5,.5,.5]]
mss = [[1,1,1],
       [1,1,1]]
play = update([pend1, pend2],Lss,mss,.01,20,fig,ax,bg)