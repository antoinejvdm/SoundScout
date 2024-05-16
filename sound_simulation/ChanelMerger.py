import wave
import numpy as np

def merge_wav_files(files, output_filename):
    # Open the WAV files
    wavs = [wave.open(file, 'r') for file in files]

    # Check if all files have the same framerate and number of frames
    framerates = {wav.getframerate() for wav in wavs}
    nframes = {wav.getnframes() for wav in wavs}

    if len(framerates) != 1 or len(nframes) != 1:
        raise ValueError("All files must have the same number of frames and framerate.")

    # Read frames and convert to numpy arrays
    datas = [np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16) for wav in wavs]

    # Stack arrays along a new axis (resulting array has shape [4, n])
    combined_data = np.stack(datas)

    # Ensure the combined data has shape [n, 4] (n samples, 4 channels)
    combined_data = combined_data.T

    # Create a new 4-channel WAV file
    output_wav = wave.open('moving.wav', 'w')
    output_wav.setnchannels(4)
    output_wav.setsampwidth(wavs[0].getsampwidth())
    output_wav.setframerate(wavs[0].getframerate())
    output_wav.writeframes(combined_data.tobytes())
    output_wav.close()

    # Close all opened files
    for wav in wavs:
        wav.close()

# Define the list of files to merge
files_to_merge = [
    'moving_source_mic_0.wav',
    'moving_source_mic_1.wav',
    'moving_source_mic_2.wav',
    'moving_source_mic_3.wav'
]
# Call the function to merge files
merge_wav_files(files_to_merge, 'moving.wav')