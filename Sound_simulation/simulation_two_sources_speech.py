import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.io import wavfile
from IPython.display import Audio
import pyroomacoustics as pra
import soundfile as sf
import csv
import os 

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
print('current dir: ', current_dir)
# Move up one directory
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
print('parrent dir: ', parent_dir)
audio_Antoine_dir = 'Sound_simulation/two_sources_sound/AntoineRecording20sec.wav' 
audio_Antoine_path = os.path.join(parent_dir, audio_Antoine_dir)
audio_Dries_dir = 'Sound_simulation/two_sources_sound/DriesRecording.wav' 
audio_Dries_path = os.path.join(parent_dir, audio_Dries_dir)
csv_source_coordinates_dir = 'Sound_simulation/two_sources_sound/source_coordinates.csv'
csv_source_coordinates_path = os.path.join(parent_dir, csv_source_coordinates_dir)
csv_mic_coordinates_dir = 'Sound_simulation/two_sources_sound/microphone_coordinates.csv'
csv_mic_coordinates_path = os.path.join(parent_dir, csv_mic_coordinates_dir)

##################### CHANGE THIS PARAMETER #####################

# If two_sources_simultaneous = 0, then we only play one source.
# If two_sources_simultaneous = 1, then we play two sources simultaneously.

two_sources_simultaneous = 1

##################### END #####################

corners = np.array([[0,0], [10,0], [10,6], [0,6]]).T
room_a = pra.Room.from_corners(corners)

# specify signal source
fs, signal = wavfile.read(audio_Antoine_path)
print(signal.shape)

with sf.SoundFile(audio_Antoine_path, 'r') as f:
    num_frames = len(f)
    sample_rate = f.samplerate

# Calculate the duration of the sound file in seconds
duration_seconds = num_frames / sample_rate

# Convert to mono signal by averaging the channels if it's stereo
if signal.ndim > 1:
    mono_signal = np.mean(signal, axis=1)
else:
    mono_signal = signal

absorbption = 0.99

# Second signal:
fs2, signal2 = wavfile.read(audio_Dries_path)

with sf.SoundFile(audio_Dries_path, 'r') as f2:
    num_frames2 = len(f2)
    sample_rate2 = f2.samplerate

# Calculate the duration of the sound file in seconds
duration_seconds2 = num_frames2 / sample_rate2

# Convert to mono signal by averaging the channels if it's stereo
if signal2.ndim > 1:
    mono_signal2 = np.mean(signal2, axis=1)
else:
    mono_signal2 = signal2

mono_signal2 = mono_signal2*0.5

room = pra.Room.from_corners(corners, fs=fs, max_order=3, materials=pra.Material(absorbption, 0.99), ray_tracing=True, air_absorption=True)
room.extrude(4., materials=pra.Material(absorbption, 0.99))

# Set the ray tracing parameters
room.set_ray_tracing(receiver_radius=0.5, n_rays=10000, energy_thres=1e-5)

# Add sources
if (two_sources_simultaneous == 0):
    source_coordinates = (5, 3, 2)
    room.add_source([source_coordinates[0],source_coordinates[1],source_coordinates[2]], signal=mono_signal, delay=0)
else:
    source_coordinates = np.zeros((2, 3))
    source_coordinates[0] = (5, 3, 2)
    source_coordinates[1] = (9, 4, 2)
    room.add_source([source_coordinates[0][0],source_coordinates[0][1],source_coordinates[0][2]], signal=mono_signal, delay=0)
    room.add_source([source_coordinates[1][0],source_coordinates[1][1],source_coordinates[1][2]], signal=mono_signal2, delay=0)
# CSV file for saving position of speakers
filename = csv_source_coordinates_path
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["X", "Y", "Z"])
    for coord in source_coordinates:
        writer.writerow(coord)

# add two-microphone array
num_mics = 4
radius = 0.21  # Radius of the circle
theta = np.linspace(0, 2 * np.pi, num_mics, endpoint=False)
x_origin = 8  # New x-origin
y_origin = 3  # New y-origin
z_origin = 2
mic_positions = np.array([radius * np.cos(theta) + x_origin, radius * np.sin(theta) + y_origin, np.ones(num_mics) * z_origin])
room.add_microphone(mic_positions)
# CSV file for saving position of microphones
mic_coordinates = np.zeros((num_mics, 3))
for i in range(num_mics):
    mic_coordinates[i] = (mic_positions[0][i], mic_positions[1][i], mic_positions[2][i])
filename = csv_mic_coordinates_path
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
    with open(current_dir + "/two_sources_sound/audio_output" + str(i) + ".wav", "wb") as f:
        f.write(audio_outputEcho.data)

# visualize 3D polyhedron room and image sources
fig, ax = room.plot(img_order=0)
fig.set_size_inches(18.5, 10.5)

#room.plot_rir()
fig = plt.gcf()
fig.set_size_inches(10, 50)

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
file_paths = ['two_sources_sound/audio_output0.wav',
              'two_sources_sound/audio_output1.wav',
              'two_sources_sound/audio_output2.wav',
              'two_sources_sound/audio_output3.wav']

output_path = 'two_sources_sound/output_our_speech_audio.wav'
merge_wav_files(file_paths, output_path)