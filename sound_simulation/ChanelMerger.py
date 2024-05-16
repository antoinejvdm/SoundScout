# import wave
# import numpy as np

# def merge_wav_files(files, output_filename):
#     # Open the WAV files
#     wavs = [wave.open(file, 'r') for file in files]

#     # Check if all files have the same framerate and number of frames
#     framerates = {wav.getframerate() for wav in wavs}
#     nframes = {wav.getnframes() for wav in wavs}

#     if len(framerates) != 1 or len(nframes) != 1:
#         raise ValueError("All files must have the same number of frames and framerate.")

#     # Read frames and convert to numpy arrays
#     datas = [np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16) for wav in wavs]

#     # Stack arrays along a new axis (resulting array has shape [4, n])
#     combined_data = np.stack(datas)

#     # Ensure the combined data has shape [n, 4] (n samples, 4 channels)
#     combined_data = combined_data.T

#     # Create a new 4-channel WAV file
#     output_wav = wave.open('simulation_20sources.wav', 'w')
#     output_wav.setnchannels(4)
#     output_wav.setsampwidth(wavs[0].getsampwidth())
#     output_wav.setframerate(wavs[0].getframerate())
#     output_wav.writeframes(combined_data.tobytes())
#     output_wav.close()

#     # Close all opened files
#     for wav in wavs:
#         wav.close()

# # Define the list of files to merge
# files_to_merge = [
#     'absorbtion0p40/audio_outputEcho0p400.wav',
#     'absorbtion0p40/audio_outputEcho0p401.wav',
#     'absorbtion0p40/audio_outputEcho0p402.wav',
#     'absorbtion0p40/audio_outputEcho0p403.wav'
# ]
# # Call the function to merge files
# merge_wav_files(files_to_merge, 'simulation_20sources.wav')

import soundfile as sf
import numpy as np

# Read the four separate WAV files
wav1, samplerate = sf.read('absorbtion0p40/audio_outputEcho0p400.wav')
wav2, samplerate = sf.read('absorbtion0p40/audio_outputEcho0p401.wav',)
wav3, samplerate = sf.read('absorbtion0p40/audio_outputEcho0p402.wav')
wav4, samplerate = sf.read('absorbtion0p40/audio_outputEcho0p403.wav')

# Combine the four channels into one multi-channel array
merged_channels = [wav1, wav2, wav3, wav4]

# Merge the channels along the second axis (channels axis)
merged_audio = np.column_stack(merged_channels)

# Save the merged audio to a new WAV file
sf.write('simulation_20sources.wav', merged_audio, samplerate)