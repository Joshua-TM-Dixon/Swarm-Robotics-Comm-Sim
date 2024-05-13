import numpy as np
import scipy.stats as ss

def gen_fading_var(m, omega):
    """
    Generate fading factor.

    Parameters:
        m (float): Shape parameter.
        omega (float): Scale parameter.

    Returns:
        float: Fading factor.
    """
    A_fading = ss.nakagami.rvs(m, scale = omega)
    F = A_fading**2
    return F

def calc_noise_power(B, T):
    """
    Calculate noise power.

    Parameters:
        B (int): Bandwidth.
        T (float): Temperature.

    Returns:
        float: Noise power.
    """
    N =  (1.38 * 10**(-23)) * B  * T
    return N

def calc_path_loss(f, d, d_0, a):
    """
    Calculate path loss.

    Parameters:
        f (float): Frequency.
        d (float): Distance.
        d_0 (float): Reference distance.
        a (float): Path loss exponent.

    Returns:
        float: Path loss.
    """
    if d < d_0:
        L_dB = 20 * np.log10((4 * np.pi * f * d) / (3 * 10**8))
    else:
        X = np.random.lognormal(0, 1)
        L_d_0_dB = 20 * np.log10((4 * np.pi * f * d_0) / (3 * 10**8))
        L_dB = L_d_0_dB + 10 * a * np.log10(d / d_0) + X
    L = 10**(L_dB / 10)
    return L

def calc_rx_power(F, P_tx, G_tx, G_rx, L):
    """
    Calculate received power.

    Parameters:
        F (float): Fading factor.
        P_tx (float): Transmit power.
        G_tx (float): Transmitter antenna gain.
        G_rx (float): Receiver antenna gain.
        L (float): Path loss.

    Returns:
        float: Received power.
    """
    P_r = (F * P_tx * G_tx * G_rx) / L
    return P_r

def calc_sinr(P_rx_tgt, P_rx_intf, N):
    """
    Calculate Signal-to-Interference-plus-Noise Ratio (SINR).

    Parameters:
        P_rx_tgt (float): Received power from the target transmitter.
        P_rx_intf (list): List of received powers from interfering transmitters.
        N (float): Noise power.

    Returns:
        float: SINR.
    """
    S = P_rx_tgt
    I = np.sum(np.array(P_rx_intf))
    return S / (I + N)