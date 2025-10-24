# elliptical_rotation_live.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from pi_format import format_matrix_2x2, format_angle_degrees

# --- math helpers -------------------------------------------------------------
def R2(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s],
                     [s,  c]])

def elliptical_rotation(a, b, theta):
    S = np.array([[a, 0.0],
                  [0.0, b]])
    Sinv = np.array([[1.0/a, 0.0],
                     [0.0,   1.0/b]])
    return Sinv @ R2(theta) @ S

def ellipse_points(a, b, n=400):
    t = np.linspace(0, 2*np.pi, n)
    return np.vstack((a*np.cos(t), b*np.sin(t)))

# --- initial params -----------------------------------------------------------
a0, b0 = 2.0, 1.2
theta0_deg = 30.0
phi0_deg = 10.0

# generate random points in unit circle, then scale by (a,b)
np.random.seed(42)
num_points = 100
angles = np.random.uniform(0, 2*np.pi, num_points)
radii = np.random.uniform(0, 1, num_points) ** 0.5  # sqrt for uniform disk distribution
random_points = np.vstack([radii * np.cos(angles), radii * np.sin(angles)])  # unit circle
random_points = np.diag([a0, b0]) @ random_points  # scale to ellipse

# --- figure & axes ------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6,6))
plt.subplots_adjust(left=0.12, right=0.98, bottom=0.30)  # space for sliders and button

# ellipse outline
E = ellipse_points(a0, b0)
(ell_line,) = ax.plot(E[0], E[1], lw=1.5, alpha=0.8, label='ellipse')

# base point on ellipse chosen by φ
def base_point(a, b, phi_rad):
    return np.array([a*np.cos(phi_rad), b*np.sin(phi_rad)])

p0 = base_point(a0, b0, np.deg2rad(phi0_deg))

# point after elliptical rotation by θ
M0 = elliptical_rotation(a0, b0, np.deg2rad(theta0_deg))
pθ = M0 @ p0
(pt0_scatter,) = ax.plot([p0[0]], [p0[1]], 'o', label='base point p₀')
(ptθ_scatter,) = ax.plot([pθ[0]], [pθ[1]], 'o', label='M(θ)·p₀')

# random points and their rotations
rotated_points = M0 @ random_points
random_scatter = ax.scatter(random_points[0], random_points[1], s=15, alpha=0.4, c='blue', label='random points')
rotated_scatter = ax.scatter(rotated_points[0], rotated_points[1], s=15, alpha=0.4, c='red', label='M(θ)·points')

# trajectory: trace out M(θ)·p₀ as θ varies from 0 to 2π
def compute_trajectory(a, b, p0, n=400):
    theta_vals = np.linspace(0, 2*np.pi, n)
    points = np.zeros((2, n))
    for i, theta in enumerate(theta_vals):
        M = elliptical_rotation(a, b, theta)
        points[:, i] = M @ p0
    return points

traj = compute_trajectory(a0, b0, p0)
(traj_line,) = ax.plot(traj[0], traj[1], 'r--', lw=1.5, alpha=0.6, label='trajectory of M(θ)·p₀')

# radial guide lines
(orig_line_p0,) = ax.plot([0, p0[0]], [0, p0[1]], '--', lw=1, alpha=0.5)
(orig_line_pθ,) = ax.plot([0, pθ[0]], [0, pθ[1]], '--', lw=1, alpha=0.5)

# format the main axes
ax.set_aspect('equal', adjustable='box')
ax.grid(True, alpha=0.35)
ax.legend(loc='upper right')
ax.set_xlim(-max(a0,b0)*1.4, max(a0,b0)*1.4)
ax.set_ylim(-max(a0,b0)*1.4, max(a0,b0)*1.4)
ax.set_title("Elliptical 'Rotation'  M(θ) = S⁻¹ R(θ) S")

# matrix display text
matrix_str = "M = " + format_matrix_2x2(M0)
matrix_text = ax.text(0.02, 0.98, matrix_str, transform=ax.transAxes,
                      verticalalignment='top', fontfamily='monospace',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# --- sliders ------------------------------------------------------------------
# regions: [left, bottom, width, height] in figure fraction coords
ax_theta = plt.axes([0.12, 0.19, 0.76, 0.03])
ax_phi   = plt.axes([0.12, 0.15, 0.76, 0.03])
ax_a     = plt.axes([0.12, 0.11, 0.76, 0.03])
ax_b     = plt.axes([0.12, 0.07, 0.76, 0.03])

s_theta = Slider(ax_theta, 'θ', -180.0, 180.0, valinit=theta0_deg, valfmt='%s')
s_phi   = Slider(ax_phi,   'φ', -180.0, 180.0, valinit=phi0_deg, valfmt='%s')
s_a     = Slider(ax_a,     'a (x-axis)', 0.3, 4.0, valinit=a0)
s_b     = Slider(ax_b,     'b (y-axis)', 0.3, 4.0, valinit=b0)

# Set initial slider value displays
s_theta.valtext.set_text(format_angle_degrees(theta0_deg))
s_phi.valtext.set_text(format_angle_degrees(phi0_deg))

ax_reset = plt.axes([0.12, 0.02, 0.15, 0.03])
btn_reset = Button(ax_reset, 'Reset')

# --- update callback ----------------------------------------------------------
def update(_):
    a = s_a.val
    b = s_b.val
    theta = np.deg2rad(s_theta.val)
    phi   = np.deg2rad(s_phi.val)

    # update ellipse outline
    E = ellipse_points(a, b)
    ell_line.set_data(E[0], E[1])

    # rescale random points to match new ellipse dimensions
    scaled_random = np.diag([a, b]) @ (np.diag([1/a0, 1/b0]) @ random_points)

    # base point p0(φ) on ellipse and rotated point pθ = M(θ)p0
    p0 = base_point(a, b, phi)
    M  = elliptical_rotation(a, b, theta)
    pθ = M @ p0

    pt0_scatter.set_data([p0[0]], [p0[1]])
    ptθ_scatter.set_data([pθ[0]], [pθ[1]])

    # update random points and their rotations
    rotated = M @ scaled_random
    random_scatter.set_offsets(scaled_random.T)
    rotated_scatter.set_offsets(rotated.T)

    # update trajectory for current p0
    traj = compute_trajectory(a, b, p0)
    traj_line.set_data(traj[0], traj[1])

    # guide lines
    orig_line_p0.set_data([0, p0[0]], [0, p0[1]])
    orig_line_pθ.set_data([0, pθ[0]], [0, pθ[1]])

    # update matrix display
    matrix_str = "M = " + format_matrix_2x2(M)
    matrix_text.set_text(matrix_str)

    # update slider value displays
    s_theta.valtext.set_text(format_angle_degrees(s_theta.val))
    s_phi.valtext.set_text(format_angle_degrees(s_phi.val))

    # autoscale a bit when a/b change
    m = 1.4*max(a, b)
    ax.set_xlim(-m, m)
    ax.set_ylim(-m, m)

    fig.canvas.draw_idle()

def reset(_):
    s_theta.reset()
    s_phi.reset()
    s_a.reset()
    s_b.reset()

for slider in (s_theta, s_phi, s_a, s_b):
    slider.on_changed(update)

btn_reset.on_clicked(reset)

plt.show()
