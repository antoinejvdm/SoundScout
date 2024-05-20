import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
    # Select a chunk from the file (in seconds)
    frames_to_read = int(2*sample_rate)
    signal_chunk = f.read(frames_to_read)

# Calculate the duration of the sound file in seconds
duration_seconds = len(signal_chunk) / sample_rate
print('duration: ', duration_seconds, 's')

mono_signal = np.sum(signal_chunk, axis=1 )
absorbption = 0.99

room = pra.Room.from_corners(corners, fs=fs, max_order=3, materials=pra.Material(absorbption, 0.99), ray_tracing=True, air_absorption=True)
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

print('mono_signal shape: ', mono_signal.shape[0])
print('mono_signal divided shape: ', mono_signal.shape[0])

source_coordinates = np.zeros((len(x_sources), 2))
#print('source coords: ', source_coordinates)

# add sources and set the signal to WAV file content
for i in range(num_sources):
    #room.add_source([7 - x_sources[i], 3 - y_sources[i], z_sources], signal=mono_signal[i*int(mono_signal.shape[0]/num_sources):(i+1)*int(mono_signal.shape[0]/num_sources)], delay=i*(duration_seconds/num_sources)) # [5,3,2] is the coordinate of the room's center
    room.add_source([7 - x_sources[i], 3 - y_sources[i], z_sources], signal=mono_signal, delay=i*duration_seconds) # [5,3,2] is the coordinate of the room's center
    source_coordinates[i] = (x_sources[i], y_sources[i])
print('source coords: ', source_coordinates)

# for i in range(2):    
#     room.add_source([7 - x_sources[i], 3 - y_sources[i], z_sources], signal=mono_signal[i*int(mono_signal.shape[0]/num_sources):(i+1)*int(mono_signal.shape[0]/num_sources)], delay=6) # [5,3,2] is the coordinate of the room's center
#     source_coordinates[i] = (x_sources[i], y_sources[i])

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
    with open("moving_sound_audio_song/audio_output" + str(i) + ".wav", "wb") as f:
        f.write(audio_outputEcho.data)

# visualize 3D polyhedron room and image sources
fig, ax = room.plot(img_order=0)
fig.set_size_inches(18.5, 10.5)

#room.plot_rir()
fig = plt.gcf()
fig.set_size_inches(10, 50)

# Also plot the sound sources chronologically on a different plot
fig2 = plt.figure(figsize=(6, 4))  # Set the size of the figure
ax = fig2.add_subplot(111, projection='3d')

for i in range(len(source_coordinates)):
    #plt.scatter(source_coordinates[i][0], source_coordinates[i][1], marker="*", color="white")  # Scatter plot of the points
    #plt.text(source_coordinates[i][0], source_coordinates[i][1], str(i), color='blue', fontsize=12, ha='center', va='center')
    ax.scatter(7 - source_coordinates[i][0], 3 - source_coordinates[i][1], 2, c='blue', marker='o', alpha=0)
    ax.text(7 - source_coordinates[i][0], 3 - source_coordinates[i][1], 2, str(i), color='blue', fontsize=7, ha='center', va='center')
ax.scatter(mic_positions[0], mic_positions[1], mic_positions[2], color='black', marker='x')

ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.set_zlim(0, 4)

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
#plt.xlabel('X-axis')  # Label for the x-axis
#plt.ylabel('Y-axis')  # Label for the y-axis
plt.title('3D Sound Sources Plot')  # Title of the plot
plt.grid(True)  # Show grid

plt.show()

########## Merging the 4 mic recordings #############
import wave
import numpy as np

def merge_wav_files(file_paths, output_path):
    # Open all input wave files
    waves = [wave.open(file_path, 'rb') for file_path in file_paths]
    
    # Check if all files have the same parameters
    params = waves[0].getparams()
    for w in waves[1:]:
        if w.getparams() != params:
            raise ValueError("All .wav files must have the same parameters")
    
    # Read frames from all wave files
    frames = [np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) for w in waves]
    
    # Close all input wave files
    for w in waves:
        w.close()
    
    # Combine frames into a 6-channel array
    combined_frames = np.stack(frames, axis=-1).flatten()
    
    # Write to output wave file
    with wave.open(output_path, 'wb') as out_wave:
        out_wave.setnchannels(4)
        out_wave.setsampwidth(params.sampwidth)
        out_wave.setframerate(params.framerate)
        out_wave.writeframes(combined_frames.tobytes())

# Example usage
file_paths = ['moving_sound_audio_song/audio_output0.wav',
              'moving_sound_audio_song/audio_output1.wav',
              'moving_sound_audio_song/audio_output2.wav',
              'moving_sound_audio_song/audio_output3.wav']

output_path = 'moving_sound_audio_song/output_moving_sound_song_4ch.wav'
merge_wav_files(file_paths, output_path)