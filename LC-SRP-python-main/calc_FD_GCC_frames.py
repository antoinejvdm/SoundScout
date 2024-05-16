import numpy as np

def calc_FD_GCC_frames(y_STFT):

    K = np.size(y_STFT,0);
    M = np.size(y_STFT,1);
    P = M * (M - 1) / 2;
    P = int(P);
    Psi_STFT = np.zeros([K, P]);
    Psi_STFT = np.complex64(Psi_STFT);
    for k in range (1,K+1):
        y = np.squeeze(y_STFT[k-1,:]);

        psi = np.zeros([P, 1]);
        psi = np.complex64(psi);
        p = 0;
        for mprime in range (1,M+1):
            for m in range (mprime+1,M+1):
                p = p + 1;
                psi[p-1] = y[m-1] * np.conjugate(y[mprime-1]);

        psi = psi / (abs(psi) + 1e-9);
        Psi_STFT[k-1,:] = np.transpose(psi); #psi 15 1 Psi_STFT 1025  15

    return Psi_STFT