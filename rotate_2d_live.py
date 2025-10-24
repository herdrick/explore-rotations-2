# rotate2d_live.py
import matplotlib
# matplotlib.use('TkAgg')  # uncomment if needed

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def R2(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s],[s,  c]])

P = np.array([[0,0, 1,1, 1,-1, -1,-1, -1,1, 0,0],
              [0,0, 1,-1, 1,  1, -1, 1, -1,-1, 0,0]])

fig, ax = plt.subplots(figsize=(5,5))
plt.subplots_adjust(bottom=0.22)  # space for slider
(ax_orig,) = ax.plot(P[0], P[1], '--', alpha=0.35, label='original')
(ax_rot,)  = ax.plot(P[0], P[1], '-',  label='rotated')
ax.set_aspect('equal', adjustable='box')
ax.grid(True)
ax.legend(loc='upper left')
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)

# matrix display text
R0 = R2(np.deg2rad(30.0))  # initial matrix
matrix_str = f"R = [{R0[0,0]: .3f}  {R0[0,1]: .3f}]\n    [{R0[1,0]: .3f}  {R0[1,1]: .3f}]"
matrix_text = ax.text(0.02, 0.98, matrix_str, transform=ax.transAxes,
                      verticalalignment='top', fontfamily='monospace',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

ax_theta = plt.axes([0.15, 0.08, 0.7, 0.04])
s_theta = Slider(ax_theta, 'θ (deg)', -180.0, 180.0, valinit=30.0)

def on_change(val):
    R = R2(np.deg2rad(s_theta.val))
    Q = R @ P
    ax_rot.set_data(Q[0], Q[1])

    # update matrix display
    matrix_str = f"R = [{R[0,0]: .3f}  {R[0,1]: .3f}]\n    [{R[1,0]: .3f}  {R[1,1]: .3f}]"
    matrix_text.set_text(matrix_str)

    fig.canvas.draw_idle()

s_theta.on_changed(on_change)
plt.show()
