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

    combined_frames = np.stack(frames, axis=-1).flatten()

    # Write to output wave file
    with wave.open(output_path, 'wb') as out_wave:
        out_wave.setnchannels(4)
        out_wave.setsampwidth(params.sampwidth)
        out_wave.setframerate(params.framerate)
        out_wave.writeframes(combined_frames.tobytes())


# Example usage
file_paths = ['two_sources_audio/audio_output0.wav',
              'two_sources_audio/audio_output1.wav',
              'two_sources_audio/audio_output2.wav',
              'two_sources_audio/audio_output3.wav']

output_path = 'two_sources_audio/output_two_sources.wav'
merge_wav_files(file_paths, output_path)