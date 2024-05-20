import numpy as np

def update_visualization(ax, angle1, angle2):
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

    ax.quiver(0, 0, 0, np.cos(angle1), np.sin(angle1), 0, length=2.0,
              color='red')
   # ax.quiver(0, 0, 0, np.cos(angle2), np.sin(angle2), 0, length=2.0,
    #          color='blue')
    ax.set_title(f'1. Angle: {angle1:.2f} deg, 2. Angle: {angle2:.2f} deg')