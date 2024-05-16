import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from IPython.display import Audio
import pyroomacoustics as pra
import soundfile as sf

corners = np.array([[0,0], [10,0], [10,6], [0,6]]).T  # [x,y]
room_a = pra.Room.from_corners(corners)

# specify signal source
fs, signal = wavfile.read("Coldplay - Viva La Vida (short).wav")

with sf.SoundFile("Coldplay - Viva La Vida (short).wav", 'r') as f:
    num_frames = len(f)
    sample_rate = f.samplerate

# Calculate the duration of the sound file in seconds
duration_seconds = num_frames / sample_rate


mono_signal = np.sum(signal, axis=1 )
absorbption = 0.40

room = pra.Room.from_corners(corners, fs=fs, max_order=0, materials=pra.Material(absorbption, 0.99), ray_tracing=True, air_absorption=True)
room.extrude(4., materials=pra.Material(absorbption, 0.99))




# Set the ray tracing parameters
room.set_ray_tracing(receiver_radius=0.5, n_rays=10000, energy_thres=1e-5)

# Number of sound sources
num_sources = 20

# We take only the first second of the signal
# mono_signal = mono_signal[0:int(mono_signal.shape[0]/num_sources)]

# Radius of the source array circle
radius = 2.0

# Angular positions of the sound sources
angles = np.linspace(0, 2*np.pi, num_sources, endpoint=False)
#print('angles: ', angles)

# Calculate Cartesian coordinates for each sound source
x_sources = radius * np.cos(angles)
y_sources = radius * np.sin(angles)
z_sources = 2
#print('x_sources: ', x_sources)
#print('y_sources: ', y_sources)
print(x_sources)
print(y_sources)
print(z_sources)

print('mono_signal shape: ', mono_signal.shape[0])
print('mono_signal divided shape: ', mono_signal.shape[0])
# add sources and set the signal to WAV file content
for i in range(num_sources):
    room.add_source([7 - x_sources[i], 3 - y_sources[i], z_sources], signal=mono_signal[i*int(mono_signal.shape[0]/num_sources):(i+1)*int(mono_signal.shape[0]/num_sources)], delay=i*(duration_seconds/num_sources)) # [5,3,2] is the coordinate of the room's center

# add two-microphone array
num_mics = 4
radius = 0.21  # Radius of the circle
theta = np.linspace(0, 2 * np.pi, num_mics, endpoint=False)
x_origin = 8  # New x-origin
y_origin = 3  # New y-origin
z_origin = 2
mic_positions = np.array([radius * np.cos(theta) + x_origin, radius * np.sin(theta) + y_origin, np.ones(num_mics) * z_origin])
room.add_microphone(mic_positions)
#print('mic_positions: ', mic_positions)

# compute image sources
room.image_source_model()

room.simulate()
for i in range(4):
    audio_outputEcho = Audio(room.mic_array.signals[i, :],rate=fs)
    with open("absorbtion0p40/audio_outputEcho0p40" + str(i) + ".wav", "wb") as f:
        f.write(audio_outputEcho.data)

# visualize 3D polyhedron room and image sources
fig, ax = room.plot(img_order=0)
fig.set_size_inches(18.5, 10.5)

room.plot_rir()
fig = plt.gcf()
fig.set_size_inches(10, 50)

plt.show()