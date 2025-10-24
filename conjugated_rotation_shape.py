# elliptical_rotation_family.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def R2(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s],[s, c]])

def M_theta_r(theta, r):
    # S = diag(r, 1) is equivalent to a/b = r
    # M = S^{-1} R S  -> explicit closed form avoids matrix mult & keeps it stable
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -r*s],[s/r, c]])

def ellipse_points(r, n=400):
    # Ellipse with semi-axes (a,b) = (r, 1). (Scaling overall doesn't matter.)
    t = np.linspace(0, 2*np.pi, n)
    return np.vstack((r*np.cos(t), np.sin(t)))

# --- initial params
theta0_deg = 30.0
phi0_deg   = 10.0
logr0      = 0.0   # log10(r); r=10**logr, so logr=0 -> r=1 (circle)

# generate random points in unit circle
np.random.seed(42)
num_points = 100
angles = np.random.uniform(0, 2*np.pi, num_points)
radii = np.random.uniform(0, 1, num_points) ** 0.5  # sqrt for uniform disk distribution
random_points_unit = np.vstack([radii * np.cos(angles), radii * np.sin(angles)])

# --- figure
fig, ax = plt.subplots(figsize=(6,6))
plt.subplots_adjust(left=0.12, right=0.98, bottom=0.23)

# draw ellipse
r0 = 10.0**logr0
E = ellipse_points(r0)
(ell_line,) = ax.plot(E[0], E[1], lw=1.5, alpha=0.85, label='ellipse (a=r, b=1)')

def base_point(r, phi_rad):
    return np.array([r*np.cos(phi_rad), np.sin(phi_rad)])

theta0 = np.deg2rad(theta0_deg)
phi0   = np.deg2rad(phi0_deg)
p0     = base_point(r0, phi0)
pθ     = M_theta_r(theta0, r0) @ p0

(pt0_scatter,) = ax.plot([p0[0]], [p0[1]], 'o', label='p₀ on ellipse')
(ptθ_scatter,) = ax.plot([pθ[0]], [pθ[1]], 'o', label='M(θ,r)·p₀')
(l0,) = ax.plot([0, p0[0]], [0, p0[1]], '--', lw=1, alpha=0.45)
(l1,) = ax.plot([0, pθ[0]], [0, pθ[1]], '--', lw=1, alpha=0.45)

# random points and their rotations
random_points = np.diag([r0, 1]) @ random_points_unit  # scale to ellipse
rotated_points = M_theta_r(theta0, r0) @ random_points
random_scatter = ax.scatter(random_points[0], random_points[1], s=15, alpha=0.4, c='blue', label='random points')
rotated_scatter = ax.scatter(rotated_points[0], rotated_points[1], s=15, alpha=0.4, c='red', label='M(θ,r)·points')

ax.set_aspect('equal', adjustable='box')
ax.grid(True, alpha=0.35)
ax.legend(loc='upper right')

m = 1.4*max(r0, 1.0)
ax.set_xlim(-m, m); ax.set_ylim(-m, m)
ax.set_title("From circle → ellipse → line via aspect ratio r")

# matrix display text
M0 = M_theta_r(theta0, r0)
matrix_str = f"M = [{M0[0,0]: .3f}  {M0[0,1]: .3f}]\n    [{M0[1,0]: .3f}  {M0[1,1]: .3f}]"
matrix_text = ax.text(0.02, 0.98, matrix_str, transform=ax.transAxes,
                      verticalalignment='top', fontfamily='monospace',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# --- sliders
ax_theta = plt.axes([0.12, 0.16, 0.76, 0.03])
ax_phi   = plt.axes([0.12, 0.12, 0.76, 0.03])
ax_logr  = plt.axes([0.12, 0.08, 0.76, 0.03])

s_theta = Slider(ax_theta, 'θ (deg)', -180.0, 180.0, valinit=theta0_deg)
s_phi   = Slider(ax_phi,   'φ (deg)', -180.0, 180.0, valinit=phi0_deg)
# logr in [-3, +3] -> r in [1e-3, 1e+3]. Avoid exactly r=0.
s_logr  = Slider(ax_logr,  'shape: log₁₀ r', -3.0, 3.0, valinit=logr0)

def update(_):
    theta = np.deg2rad(s_theta.val)
    phi   = np.deg2rad(s_phi.val)
    logr  = s_logr.val
    r     = 10.0**logr

    # ellipse and points
    E = ellipse_points(r)
    ell_line.set_data(E[0], E[1])

    p0 = base_point(r, phi)
    M  = M_theta_r(theta, r)
    pθ = M @ p0

    pt0_scatter.set_data([p0[0]], [p0[1]])
    ptθ_scatter.set_data([pθ[0]], [pθ[1]])
    l0.set_data([0, p0[0]], [0, p0[1]])
    l1.set_data([0, pθ[0]], [0, pθ[1]])

    # update random points and their rotations
    scaled_random = np.diag([r, 1]) @ random_points_unit
    rotated = M @ scaled_random
    random_scatter.set_offsets(scaled_random.T)
    rotated_scatter.set_offsets(rotated.T)

    # autoscale with r
    m = 1.4*max(r, 1.0)
    ax.set_xlim(-m, m); ax.set_ylim(-m, m)

    # update matrix display
    matrix_str = f"M = [{M[0,0]: .3f}  {M[0,1]: .3f}]\n    [{M[1,0]: .3f}  {M[1,1]: .3f}]"
    matrix_text.set_text(matrix_str)

    fig.canvas.draw_idle()

for s in (s_theta, s_phi, s_logr):
    s.on_changed(update)

plt.show()
