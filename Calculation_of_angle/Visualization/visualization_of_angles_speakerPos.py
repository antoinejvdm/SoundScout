import matplotlib.pyplot as plt
import random
import numpy as np

def visualization_of_angles_speakerPos(ax,angle, angle2,micPos, speakerPos):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_zlim(0, 4)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Mic center position
    center_of_mic_array = [8, 3, 2]
    ax.scatter(center_of_mic_array[0], center_of_mic_array[1], center_of_mic_array[2], color='gray', alpha=1, s=20)

    ax.quiver(center_of_mic_array[0], center_of_mic_array[1], center_of_mic_array[2], np.cos(angle), np.sin(angle), 0, length=2.0,color='red')
    ax.quiver(center_of_mic_array[0], center_of_mic_array[1], center_of_mic_array[2], np.cos(angle2), np.sin(angle2), 0,length=2.0,color='green')
    ax.set_title(f'Angle: {np.rad2deg(angle):.2f} deg')

    for i in range(len(speakerPos)):
        ax.scatter(7 - speakerPos[i][0], 3 - speakerPos[i][1], speakerPos[i][2], c='blue', marker='o', alpha=0)
        ax.text(7 - speakerPos[i][0], 3 - speakerPos[i][1], speakerPos[i][2], str(i), color='blue', fontsize=7, ha='center', va='center')

    for i in range(len(micPos)):
        ax.scatter(micPos[i][0], micPos[i][1], micPos[i][2], c='black', marker='+', alpha=0.8)
