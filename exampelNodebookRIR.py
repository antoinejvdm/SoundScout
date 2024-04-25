import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import fftconvolve
import IPython
from IPython.display import Audio
import pyroomacoustics as pra

corners = np.array([[0,0], [0,6], [5,6], [0,5]]).T  # [x,y]
room = pra.Room.from_corners(corners)

fs, signal = wavfile.read("Coldplay - Viva La Vida (short).wav")


# set max_order to a low value for a quick (but less accurate) RIR
room = pra.Room.from_corners(corners, fs=fs, max_order=3, absorption=0.2, ray_tracing=True, air_absorption=True)
room.extrude(2., materials=pra.Material(0.2, 0.15))

# Set the ray tracing parameters
room.set_ray_tracing(receiver_radius=0.5, n_rays=10000, energy_thres=1e-5)

# add source and set the signal to WAV file content
room.add_source([1., 1., 0.5], signal=signal)

# add two-microphone array
R = np.array([[3.5, 3.6], [2., 2.], [0.5,  0.5]])  # [[x], [y], [z]]
room.add_microphone(R)

# compute image sources
room.image_source_model()

# visualize 3D polyhedron room and image sources
fig, ax = room.plot(img_order=3)
fig.set_size_inches(18.5, 10.5)

room.plot_rir()
fig = plt.gcf()
fig.set_size_inches(15, 5)
plt.show()

t60 = pra.experimental.measure_rt60(room.rir[0][0], fs=room.fs, plot=True)
print(f"The RT60 is {t60 * 1000:.0f} ms")

room.simulate()
print(room.mic_array.signals.shape)

audio_outputOriginal = Audio(signal, rate=fs)

print("Simulated propagation to first mic:")
audio_outputEcho = Audio(room.mic_array.signals[0,:], rate=fs)

# Save the audio to a file
with open("audio_outputEcho.wav", "wb") as f:
    f.write(audio_outputEcho.data)