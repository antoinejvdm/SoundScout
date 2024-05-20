import matplotlib.pyplot as plt
import random
import numpy as np

def visualization_of_angle_speakerPos(ax,angle):
    # Mic position(s)
    center_of_mic_array = [8, 3, 2]
    ### Adding the sound sources ###
    num_sources = 20  # nr. of sources
    radius = 2.0  # radius of the circle on which we put the sources
    angles = np.linspace(0, 2 * np.pi, num_sources, endpoint=False)  # Angular positions of the sound sources
    x_sources = radius * np.cos(angles)  # Cartesian x-coordinates
    y_sources = radius * np.sin(angles)  # Cartesian y-coordinates
    z_sources = 2  # Cartesian z-coordinate
    source_coordinates = np.zeros((len(x_sources), 2))  # initializing the list of coordinates

    for i in range(num_sources):
        source_coordinates[i] = (x_sources[i], y_sources[i])

    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_zlim(0, 4)
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
    ax.scatter(center_of_mic_array[0], center_of_mic_array[1], center_of_mic_array[2], color='gray', alpha=1, s=150)

    ax.quiver(center_of_mic_array[0], center_of_mic_array[1], center_of_mic_array[2], np.cos(angle), np.sin(angle), 0, length=2.0,
              color='blue')
    ax.set_title(f'Angle: {angle:.2f} deg')

    for i in range(len(source_coordinates)):
        ax.scatter(7 - source_coordinates[i][0], 3 - source_coordinates[i][1], 2, c='blue', marker='o', alpha=0)
        ax.text(7 - source_coordinates[i][0], 3 - source_coordinates[i][1], 2, str(i), color='blue', fontsize=7, ha='center', va='center')
