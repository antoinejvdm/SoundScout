
import numpy as np
import math

def calc_SRPconv_frames(Psi_STFT, omega, Delta_t_i):

    J = np.size(Delta_t_i, 0);
    K = np.size(Psi_STFT, 0);

    SRP_FD = np.zeros([K, J])
    SRP_FD = np.complex64(SRP_FD)
    for k in range(1, K):
        psi = np.squeeze(Psi_STFT[k, :]);
        i = np.arange(len(SRP_FD[k])) + 1;
        SRP_FD[k - 1, :] = np.dot((np.exp(1j * Delta_t_i[i - 1, :] * omega[k])), psi);

    SRP_stack = 2 * np.sum(np.real(SRP_FD), axis=0);
    return SRP_stack
