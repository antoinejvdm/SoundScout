import numpy as np
import math

def calc_SRPconv_2D(Psi_STFT, omega, Delta_t_i_az):

    J = Delta_t_i_az.shape[0]
    L = Psi_STFT.shape[1]
    SRP_stack = np.zeros((L, J))

    for l in range(L):
        SRP_FD = np.zeros((omega.shape[0], J), dtype=np.complex64)
        for k in range(1, omega.shape[0]):
            psi = np.squeeze(Psi_STFT[k, l, :])
            for j in range(J):
                SRP_FD[k, j] = np.dot(np.exp(1j * Delta_t_i_az[j] * omega[k]), psi)

        SRP_stack[l, :] = 2 * np.sum(np.real(SRP_FD), axis=0)

    return SRP_stack
