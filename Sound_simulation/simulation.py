import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from IPython.display import Audio
import pyroomacoustics as pra

corners = np.array([[0,0], [10,0], [10,6], [0,6]]).T  # [x,y]
room_a = pra.Room.from_corners(corners)

# specify signal source
fs, signal = wavfile.read("Coldplay - Viva La Vida (short).wav")
mono_signal = np.sum(signal, axis=1 )
absorbption = 0.99

room = pra.Room.from_corners(corners, fs=fs, max_order=3, materials=pra.Material(absorbption, 0.99), ray_tracing=True, air_absorption=True)
room.extrude(4., materials=pra.Material(absorbption, 0.99))




# Set the ray tracing parameters
room.set_ray_tracing(receiver_radius=0.5, n_rays=10000, energy_thres=1e-5)


# add source and set the signal to WAV file content
room.add_source([2, 3, 2], signal=mono_signal)

# add two-microphone array
num_mics = 4
radius = 0.21  # Radius of the circle
theta = np.linspace(0, 2 * np.pi, num_mics, endpoint=False)
x_origin = 8  # New x-origin
y_origin = 3  # New y-origin
z_origin = 2
mic_positions = np.array([radius * np.cos(theta) + x_origin, radius * np.sin(theta) + y_origin, np.ones(num_mics) * z_origin])
room.add_microphone(mic_positions)
print(mic_positions)

# compute image sources
room.image_source_model()

room.simulate()
for i in range(num_mics):
    audio_outputEcho = Audio(room.mic_array.signals[i, :],rate=fs)
    with open("TestOneDirection/audio_4mic" + str(i) + ".wav", "wb") as f:
        f.write(audio_outputEcho.data)

# visualize 3D polyhedron room and image sources
fig, ax = room.plot(img_order=3)
fig.set_size_inches(18.5, 10.5)

room.plot_rir()
fig = plt.gcf()
fig.set_size_inches(10, 50)

plt.show()