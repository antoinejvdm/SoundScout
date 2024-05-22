import numpy as np
import matplotlib.pyplot as plt
import math
def calc_SRPconv_frames(Psi_STFT, omega, Delta_t_i):
    J = np.size(Delta_t_i, 0)  # Number of candidate locations
    K = np.size(Psi_STFT, 0)   # Number of STFT frames

    SRP_FD = np.zeros([K, J], dtype=np.complex64)  # Initialize SRP matrix

    for k in range(1, K):
        psi = np.squeeze(Psi_STFT[k, :])  # Extract FD-GCC values for the k-th frame
        i = np.arange(len(SRP_FD[k])) + 1
        SRP_FD[k - 1, :] = np.dot(np.exp(1j * Delta_t_i[i - 1, :] * omega[k]), psi)

    SRP_stack = 2 * np.sum(np.real(SRP_FD), axis=0)  # Sum real parts
    return SRP_stack
# Parameters
num_frames = 10
num_mics = 4
num_candidates = 8
freqs = np.linspace(0, np.pi, num_frames)

# Generate random complex FD-GCC values
Psi_STFT = np.random.randn(num_frames, num_mics * (num_mics - 1) // 2) + 1j * np.random.randn(num_frames, num_mics * (num_mics - 1) // 2)

# Generate random Delta_t_i (time differences of arrival)
Delta_t_i = np.random.randn(num_candidates, num_mics * (num_mics - 1) // 2)
SRP_stack = calc_SRPconv_frames(Psi_STFT, freqs, Delta_t_i)
# Plot the SRP values for each candidate location
plt.figure(figsize=(10, 6))
plt.bar(range(len(SRP_stack)), SRP_stack, color='blue')
plt.xlabel('Candidate Location')
plt.ylabel('SRP Value')
plt.title('Steered Response Power (SRP) for Candidate Locations')
plt.grid(True)
plt.show()
