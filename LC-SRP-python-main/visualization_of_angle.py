
import numpy as np

def visualization_of_angle(axis,angle):
    axis.clear()
    axis.set_xlim(-2, 2)
    axis.set_ylim(-2, 2)
    axis.set_zlim(-2, 2)
    axis.set_xlabel('X')
    axis.set_ylabel('Y')
    axis.set_zlabel('Z')

    # microphone
    r = 0.06
    h = 0.35
    resolution = 1000
    theta = np.linspace(0, 2 * np.pi, resolution)
    z = np.linspace(-0.5, h - 0.5, resolution)
    theta, z = np.meshgrid(theta, z)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    axis.plot_surface(x, y, z, color='black', alpha=0.5)
    axis.scatter(0, 0, 0, color='gray', alpha=1, s=150)

    axis.quiver(0, 0, 0, np.cos(angle), np.sin(angle), 0, length=2.0,
              color='blue')
    axis.set_title(f'Angle: {np.rad2deg(angle):.2f} deg')