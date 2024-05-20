import numpy as np
import math
from scipy.fft import fft, ifft
def calc_STFT_frames(x, fs, win, N_STFT, sides):
    N_STFT_half = N_STFT/2 + 1;

    #get frequency vector
    f = np.linspace(0,fs/2,int(N_STFT_half));
    if (sides=='twosided'):
        f = [f, np.take(-f,(range(len(f)-2,0,-1)))];

    #init
    M = len(np.transpose(x));
    if (sides == 'onesided'):
        X = np.zeros((int(N_STFT_half), len(np.transpose(x))))
    if (sides == 'twosided'):
        X = np.zeros((N_STFT, M))

    X = np.complex128(X)

    for m in range (1,M+1):
        x_frame = x[:,m-1]
        X_frame = fft(np.multiply(win,x_frame))
        if (sides == 'onesided'):
            X[:,m-1] = X_frame[0:int(N_STFT_half)]
        if (sides == 'twosided'):
            X[:,m-1] = X_frame
    return X, f