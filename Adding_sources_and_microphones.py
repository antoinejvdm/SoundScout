import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import fftconvolve
import IPython
from IPython.display import Audio
import pyroomacoustics as pra

## Adding sources and microphones ##

# specify signal source
fs, signal = wavfile.read("audio_outputEcho.wav")

# add source to 2D room
corners = np.array([[0,0], [0,3], [5,3], [5,1], [3,1], [3,0]]).T  # [x,y]
room = pra.Room.from_corners(corners, fs=fs, ray_tracing=True, air_absorption=True)
room.add_source([1.,1.], signal=signal)

# add microphone array #
R = pra.circular_2D_array(center=[2.,2.], M=6, phi0=0, radius=0.1)
room.add_microphone_array(pra.MicrophoneArray(R, room.fs))


fig, ax = room.plot()
ax.set_xlim([-0.5, 5.5])
ax.set_ylim([-0.5, 3.5])

plt.show()

