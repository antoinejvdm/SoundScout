import numpy as np
import matplotlib.pyplot as plt
def calc_FD_GCC_frames(y_STFT):
    K = np.size(y_STFT, 0)  # Number of frames
    M = np.size(y_STFT, 1)  # Number of microphones
    P = int(M * (M - 1) / 2)  # Number of unique microphone pairs
    Psi_STFT = np.zeros([K, P], dtype=np.complex64)  # Initialize output array

    for k in range(1, K + 1):
        y = np.squeeze(y_STFT[k - 1, :])  # Extract STFT values for frame k
        psi = np.zeros([P, 1], dtype=np.complex64)  # Initialize cross-correlation array
        p = 0

        for mprime in range(1, M + 1):
            for m in range(mprime + 1, M + 1):
                p += 1
                # Compute cross-correlation between pairs of microphones
                psi[p - 1] = y[m - 1] * np.conjugate(y[mprime - 1])

        # Normalize the cross-correlation
        psi = psi / (abs(psi) + 1e-9)
        Psi_STFT[k - 1, :] = np.transpose(psi)

    return Psi_STFT
# Parameters
num_frames = 10
num_mics = 4
stft_size = 1024

# Generate random complex STFT data
y_STFT = np.random.randn(num_frames, num_mics) + 1j * np.random.randn(num_frames, num_mics)
Psi_STFT = calc_FD_GCC_frames(y_STFT)
# Plot the magnitude of the FD-GCC for each frame and microphone pair
plt.figure(figsize=(12, 6))
for i in range(Psi_STFT.shape[1]):
    plt.plot(np.abs(Psi_STFT[:, i]), label=f'Pair {i+1}')
plt.xlabel('Frame')
plt.ylabel('Magnitude of FD-GCC')
plt.title('Frequency Domain Generalized Cross-Correlation (FD-GCC)')
plt.legend()
plt.grid(True)
plt.show()
