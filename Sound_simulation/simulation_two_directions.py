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
fs, signal = wavfile.read("raw_wav_files/Asine_6s.wav")

with sf.SoundFile("raw_wav_files/Asine_6s.wav", 'r') as f:
    num_frames = len(f)
    sample_rate = f.samplerate

# Calculate the duration of the sound file in seconds
duration_seconds = num_frames / sample_rate

mono_signal = np.sum(signal, axis=1 )
absorbption = 0.99

room = pra.Room.from_corners(corners, fs=fs, max_order=3, materials=pra.Material(absorbption, 0.99), ray_tracing=True, air_absorption=True)
room.extrude(4., materials=pra.Material(absorbption, 0.99))

# Set the ray tracing parameters
room.set_ray_tracing(receiver_radius=0.5, n_rays=10000, energy_thres=1e-5)

# Add sources
source_coordinates = np.zeros((2, 3))
source_coordinates[0] = (5,3,2)
source_coordinates[1] = (9,4,2)
room.add_source([source_coordinates[0][0],source_coordinates[0][1],source_coordinates[0][2]], signal=mono_signal, delay=0)
room.add_source([source_coordinates[1][0],source_coordinates[1][1],source_coordinates[1][2]], signal=mono_signal, delay=6)
# CSV file for saving position of speakers
filename = "two_directions_audio/source_coordinates.csv"
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["X", "Y", "Z"])
    for coord in source_coordinates:
        writer.writerow(coord)

# add two-microphone array
num_mics = 4
radius = 0.21  # Radius of the circle
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
filename = "two_directions_audio/microphone_coordinates.csv"
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
    with open("two_directions_audio/audio_output" + str(i) + ".wav", "wb") as f:
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
    
    # Combine frames into a 4-channel array
    combined_frames = np.stack(frames, axis=-1).flatten()
    
    # Write to output wave file
    with wave.open(output_path, 'wb') as out_wave:
        out_wave.setnchannels(4)
        out_wave.setsampwidth(params.sampwidth)
        out_wave.setframerate(params.framerate)
        out_wave.writeframes(combined_frames.tobytes())

# Example usage
file_paths = ['two_directions_audio/audio_output0.wav',
              'two_directions_audio/audio_output1.wav',
              'two_directions_audio/audio_output2.wav',
              'two_directions_audio/audio_output3.wav']

output_path = 'two_directions_audio/output_two_directions_audio.wav'
merge_wav_files(file_paths, output_path)