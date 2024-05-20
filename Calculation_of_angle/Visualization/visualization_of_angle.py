
import numpy as np

def visualization_of_angle(ax,angle):
    ax.clear()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # microphone
    r = 0.06
    h = 0.35
    resolution = 1000
    theta = np.linspace(0, 2 * np.pi, resolution)
    z = np.linspace(-0.5, h - 0.5, resolution)
    theta, z = np.meshgrid(theta, z)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    ax.plot_surface(x, y, z, color='black', alpha=0.5)
    ax.scatter(0, 0, 0, color='gray', alpha=1, s=150)

    ax.quiver(0, 0, 0, np.cos(angle), np.sin(angle), 0, length=2.0,
              color='red')
    ax.set_title(f'Angle: {angle:.2f} deg')
