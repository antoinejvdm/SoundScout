import numpy as np
from scipy.io import wavfile

fs, signal = wavfile.read("raw_wav_files/Coldplay - Viva La Vida.wav")
fromTo = [180,220] #in sec
shortSignal = signal[int(fs * fromTo[0]): int(fs * fromTo[1])]

print(signal.shape)
print(shortSignal.shape)
wavfile.write('raw_wav_files/Coldplay - Viva La Vida(40sec).wav', fs, shortSignal)