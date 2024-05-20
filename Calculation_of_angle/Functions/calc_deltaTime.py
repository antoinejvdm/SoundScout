import numpy as np
from numpy import linalg as LA
def calc_deltaTime(micPos, dim1, dim2, mode, c):
    # number of microphones
    M = len(micPos)
    # number of microphone pairs
    P = M * (M - 1) / 2

    N_dim1 = len(dim1)
    N_dim2 = len(dim2)

    rows = N_dim1 * N_dim2
    Delta_t_i = np.zeros((rows, int(P)))

    loc = np.zeros((rows, 3))

    i = 0
    for n_dim1 in range(1, N_dim1 + 1):
        for n_dim2 in range(1, N_dim2 + 1):
            i += 1
            if mode == 'cartesian':
                x = dim1[n_dim1 - 1]
                y = dim2[n_dim2 - 1]
                # location in cartesian coordinates
                loc[i - 1, :] = x, y, 0
                # TDOA
                Delta_t_i[i - 1, :] = loc2TDOA(micPos, [x, y, 0], c)
            elif mode == 'polar':
                r = dim1[n_dim1 - 1]
                theta = dim2[n_dim2 - 1]
                x = r * np.cos(np.deg2rad(theta))
                y = r * np.sin(np.deg2rad(theta))
                # location in cartesian coordinates
                loc[i - 1, :] = x, y, 0
                # TDOA
                Delta_t_i[i - 1, :] = loc2TDOA(micPos, [x, y, 0], c)
            elif mode == 'spherical':
                ang_pol = dim1[n_dim1 - 1]
                ang_az = dim2[n_dim2 - 1]
                # location in far field spherical coordinates
                Delta_t_i[i - 1, :], loc[i - 1, :] = spher2TDOA(micPos, ang_pol, ang_az, c)
                if ang_pol == 0 or ang_pol == 180:
                    break

    Delta_t_i = Delta_t_i[:i, :]
    loc = loc[:i, :]
    return loc, Delta_t_i

def loc2TDOA(micPos, loc, c):
    M = len(micPos)
    P = M * (M - 1) / 2
    # propagation time
    Z = micPos - np.tile(loc, (M, 1))
    dist = np.sqrt(np.sum(np.power(Z, 2), axis=1))
    propTime = dist / c

    delta_t = np.zeros((int(P),))
    p = 0
    for mprime in range(1, M + 1):
        for m in range(mprime + 1, M + 1):
            delta_t[p] = propTime[m - 1] - propTime[mprime - 1]
            p += 1

    return delta_t

def spher2TDOA(micPos, ang_pol, ang_az, c):
    M = len(micPos)
    P = M * (M - 1) / 2

    DOA_vec = [np.sin(np.deg2rad(ang_pol)) * np.cos(np.deg2rad(ang_az)),
               np.sin(np.deg2rad(ang_pol)) * np.sin(np.deg2rad(ang_az)),
               np.cos(np.deg2rad(ang_pol))]
    DOA_vec = np.matrix(DOA_vec)

    b = -np.transpose(DOA_vec)
    b = np.matrix(b)
    micPos = np.matrix(micPos)

    delta_t = np.zeros((int(P), 1))
    p = 0
    for mprime in range(1, M + 1):
        for m in range(mprime + 1, M + 1):
            p += 1

            a = np.transpose(micPos[m - 1, :]) - np.transpose(micPos[mprime - 1, :])
            a = np.matrix(a)
            norms = (LA.norm(a) * LA.norm(b))
            delta_t[p - 1] = (LA.norm(a) / c) * (np.transpose(a) * b / norms)
    return np.transpose(delta_t), DOA_vec