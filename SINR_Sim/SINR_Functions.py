import numpy as np


def gen_fading_var(distribution, mu, sigma, n_vals):
    if distribution == 'F' or distribution == 'f' or distribution == 0:
        return np.random.exponential(sigma, n_vals)  
    elif distribution == 'S' or distribution == 's' or distribution == 1:
        return np.random.lognormal(mu, sigma, n_vals)
    else:
        print("""Error : gen_fading_var : Fading Distribution can be 
              \n F, f or 0 for exponential distribution
              \n S, s or 1 for lognormal distribution""")


def calc_noise_power(B, T):
    for param in [B, T]:
        if isinstance(param, (int, float)) == False or param < 0:
            print("Error: calc_path_loss: All parameters must be real numbers greater than 0")
            return None
    else:
        return (1.38 * 10 ** (-23)) * B  * T


def calc_path_loss(f, d, a):
    if all(isinstance(param, (int, float)) for param in [f, d, a]) == False:
        print("Error: calc_path_loss: All parameters must be real numbers")
    if  f < 0 or d <0:
        print("Error: calc_path_loss: frequency and distance must be a real numbers greater than 0")
    else:
        return ((3 * 10 ** 8) / (4 * np.pi * f * d)) ** a


def calc_rx_power(F, P_tx, G_tx, G_rx, L):
    if not all(isinstance(param, (int, float)) for param in [F, P_tx, G_tx, G_rx, L]):
        print("Error: calc_rx_power: All parameters must be real numbers")
    elif F < 0 or F > 1:
        print("Error: calc_rx_power: Fading variable must be a real number between 0 and 1")
    elif P_tx < 0:
        print("Error: calc_rx_power: Transmitter power must be a real number greater than 0")
    elif G_tx < 0 or G_rx < 0:
        print("Error: calc_rx_power: Gain values must be real numbers greater than 0")
    elif L <= 0:
        print("Error: calc_rx_power: Path-loss must be a real number greater than 0")
    else:
        return F * P_tx * G_tx * G_rx * L


def calc_sinr(P_rx_tgt, P_rx_intf, N):
    for param in [P_rx_tgt, P_rx_intf, N]:
        if isinstance(param, (int, float)) == False or param < 0:
            print("Error: calc_path_loss: All parameters must be real numbers greater than 0")
            return None
    S = P_rx_tgt
    I = np.sum(np.array(P_rx_intf))
    return S / (I + N)