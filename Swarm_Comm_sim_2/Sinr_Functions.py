import numpy as np
import scipy.stats as ss

# Produces a random variable to represent fading or shadowing in a channel
def gen_fading_var(m, omega):
    A_fading = ss.nakagami.rvs(m, scale = omega)
    F = A_fading ** 2
    return F

# Calculates noise power
def calc_noise_power(B, T):
    N =  (1.38 * 10 ** (-23)) * B  * T
    return N

# Calculates path-loss
def calc_path_loss(f, d, a):
    L =  ((3 * 10 ** 8) / (4 * np.pi * f * d)) ** a
    return L

# Calculates power at the receiver
def calc_rx_power(F, P_tx, G_tx, G_rx, L):
    return F * P_tx * G_tx * G_rx * L

# Calculates the sinr between target transmitters and receivers
def calc_sinr(P_rx_tgt, P_rx_intf, N):
    S = P_rx_tgt
    I = np.sum(np.array(P_rx_intf))
    return S / (I + N)