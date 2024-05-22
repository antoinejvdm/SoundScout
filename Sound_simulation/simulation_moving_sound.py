import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from IPython.display import Audio
import pyroomacoustics as pra
import soundfile as sf
import csv

corners = np.array([[0,0], [10,0], [10,6], [0,6]]).T  # [x,y]
room_a = pra.Room.from_corners(corners)

# specify signal source
fs, signal = wavfile.read("raw_wav_files/Coldplay - Viva La Vida (short).wav")

with sf.SoundFile("raw_wav_files/Coldplay - Viva La Vida (short).wav", 'r') as f:
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
# Radius of the source array circle
radius = 2.0
# Angular positions of the sound sources
angles = np.linspace(0, 2*np.pi, num_sources, endpoint=False)
# Center of the Source Array
sources_center = [7,3,2]
# Calculate Cartesian coordinates for each sound source
x_sources = sources_center[0] - (radius * np.cos(angles))
y_sources = sources_center[1] - (radius * np.sin(angles))
z_sources = 2

source_coordinates = np.zeros((len(x_sources), 3))
# add sources and set the signal to WAV file content
for i in range(num_sources):
    room.add_source([x_sources[i], y_sources[i], z_sources], signal=mono_signal, delay=i*duration_seconds) # [5,3,2] is the coordinate of the room's center
    source_coordinates[i] = (x_sources[i], y_sources[i], z_sources)

# CSV file for saving position of speakers
filename = "moving_sound_audio_song/source_coordinates.csv"
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["X", "Y", "Z"])
    for coord in source_coordinates:
        writer.writerow(coord)

# add two-microphone array
num_mics = 4
radius = 0.21
theta = np.linspace(0, 2 * np.pi, num_mics, endpoint=False)
x_origin = 8
y_origin = 3
z_origin = 2
mic_positions = np.array([radius * np.cos(theta) + x_origin, radius * np.sin(theta) + y_origin, np.ones(num_mics) * z_origin])
room.add_microphone(mic_positions)

mic_coordinates = np.zeros((num_mics, 3))
for i in range(num_mics):
    mic_coordinates[i] = (mic_positions[0][i], mic_positions[1][i], mic_positions[2][i])
# CSV file for saving position of microphones
filename = "moving_sound_audio_song/microphone_coordinates.csv"
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["X", "Y", "Z"])
    for coord in mic_coordinates:
        writer.writerow(coord)

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
    ax.scatter(source_coordinates[i][0], source_coordinates[i][1], 2, c='blue', marker='o', alpha=0)
    ax.text(source_coordinates[i][0], source_coordinates[i][1], 2, str(i), color='blue', fontsize=7, ha='center', va='center')
ax.scatter(mic_positions[0], mic_positions[1], mic_positions[2], color='black', marker='x')

ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.set_zlim(0, 4)

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.title('3D Sound Sources Plot')
plt.grid(True)

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
    
    # Combine frames into a 5-channel array
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