import numpy as np

    # Generates fading or scattering variable using different distributions
    # with a mean mu and standard deviation sigma where required
def Gen_F(FS, mu, sigma):
    if FS == 'F' or FS == 'f' or FS == 0:
        return np.random.exponential(sigma)  
    elif FS == 'S' or FS == 's' or FS == 1:
        return np.random.lognormal(mu, sigma)

    # Calculates Noise Power
def Calc_N(B, T):
    return (1.38 * 10 ** (-23)) * B  * T

    # Calculates Path-Loss
def Calc_L(f, d, a):
    return ((3 * 10 ** 8) / (4 * np.pi * f * d)) ** a

    # Calculates signal power at receiver
def Calc_P_r(F, P_t, G_t, G_r, L):
    return F * P_t * G_t * G_r * L

    # Calculates SINR
def Calc_SINR(P_rs, P_ri, N):
    S = P_rs
    I = np.sum(np.array(P_ri))
    return S / (I + N)