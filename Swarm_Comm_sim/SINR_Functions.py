import numpy as np

# Produces a random variable to represent fading or shadowing in a channel
def gen_fading_var(distribution, mu, sigma):
    if distribution == 'F' or distribution == 'f' or distribution == 0:
        return np.random.exponential(sigma)  
    elif distribution == 'S' or distribution == 's' or distribution == 1:
        return np.random.lognormal(mu, sigma)

# Calculates noise power
def calc_noise_power(B, T):
    return (1.38 * 10 ** (-23)) * B  * T

# Calculates path-loss
def calc_path_loss(f, d, a):
    return ((3 * 10 ** 8) / (4 * np.pi * f * d)) ** a

# Calculates power at the receiver
def calc_rx_power(F, P_tx, G_tx, G_rx, L):
    return F * P_tx * G_tx * G_rx * L

# Calculates the sinr between target transmitters and receivers
def calc_sinr(P_rx_tgt, P_rx_intf, N):
    S = P_rx_tgt
    I = np.sum(np.array(P_rx_intf))
    return S / (I + N)