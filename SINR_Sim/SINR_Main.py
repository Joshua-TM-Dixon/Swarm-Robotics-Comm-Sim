# Libraries
import numpy as np
import plotly.graph_objects as go
import SINR_Functions as Sinr

#  Global Constants
pi = np.pi
c = 3 * 10 ** 8
k_B = 1.38 * 10 ** (-23)

# Simulation variables
pr = []        # Coverage probability
sim = 10000    # Number of simulations

# Environment variables
r = 10                                  # Radius of circle (m)
T = 300                                 # temperature (K)
n_range = range(3, 4, 2)               # range of number of interference nodes
d_ts_range = np.linspace(0.1, r, 50)    # range of desired transmitter distances from receiver (m)


# Signal variables
B = 10 ** 6             # Bandwidth (Hz)
f = 2.4835 * 10 ** 9    # Frequency (Hz)
P_t = 10 ** (-5)        # Transmitter power (W)
G = 10 ** (-1)          # Antenna gain
thr = 1                 # SINR threshold

# Functions

    # Generates n random node positions on a circle with radius r and returns
    # a list of distances and angles for all nodes
def Gen_node_pos(n, r):
    theta = 2 * np.pi * np.random.uniform(0, 1, n)
    d = r * np.sqrt(np.random.uniform(0, 1, n))
    return d, theta

    # Generates fading or scattering variable using different distributions
    # with a mean mu and standard deviation sigma where required
def Gen_F(FS, mu, sigma):
    if FS == 'F' or FS == 'f' or FS == 0:
        return np.random.exponential(sigma)  
    elif FS == 'S' or FS == 's' or FS == 1:
        return np.random.lognormal(mu, sigma)

    # Calculates Noise Power
def Calc_N(k_B, B, T):
    return k_B * B  * T

    # Calculates Path-Loss
def Calc_L(f, d):
    return (c / (4 * pi * f * d)) ** 2

    # Calculates signal power at receiver
def Calc_P_r(F, P_t, G, L):
    return F * P_t * G * G * L

    # Calculates SINR
def Calc_SINR(P_rs, P_ri, N):
    S = P_rs
    I = np.sum(np.array(P_ri))
    return S / (I + N)

    # Plots generic figure containing 1 or more scatter graphs
def Plot_Data(t_name, t_data, t_dim, x_name, x_data, x_dim, y_name, y_data, y_dim):
    fig = go.Figure()
    
    for i in range(len(t_data)):
        fig.add_trace(go.Scatter(x = list(x_data),
                                 y = [y_data[j + i * len(x_data)] for j in range(len(x_data))], 
                                 mode = 'lines+markers',
                                 name = f'{t_name} = {t_data[i]} {t_dim}'))
        
    fig.update_layout(
        title = dict(
            text = f'Graph of {y_name} Against {x_name}',
            font = dict(family = 'Arial', size = 26, color = 'black')),
        xaxis = dict(
            title = dict(
                text = f'{x_name} ({x_dim})',
                font = dict(family = 'Arial', size = 22, color = 'black')),
            tickfont = dict(family = 'Arial', size = 18, color = 'black')),
        yaxis = dict(
            title = dict(
                text = f'{y_name} ({y_dim})',
                font = dict(family = 'Arial', size = 22, color = 'black')),
            tickfont = dict(family = 'Arial', size = 18, color = 'black')),
        legend = dict(
            font = dict(family = 'Arial', size = 18, color = 'black'),
            x = 0, 
            y = -0.1, 
            orientation = 'h'),
        autosize = False,
        width = 1100,
        height = 750)
    
    fig.show()
    
#Monte-Carlo simulation using communication parameters
N = Calc_N(k_B, B, T)
for n in n_range:
    F = Gen_F('F', 0, 1)
    for d_ts in d_ts_range:
        c = 0
        L_ts = Calc_L(f, d_ts)
        P_rs = Calc_P_r(F, P_t, G, L_ts)
        for j in range (sim):
            d_ti, theta_ti = Gen_node_pos(n, r)
            L_ti = Calc_L(f, d_ti)
            P_ri = Calc_P_r(F, P_t, G, L_ti)
            sinr = Calc_SINR(P_rs, P_ri, N)
            if sinr > thr:
                c += 1
        pr.append(c / sim)

# Graph
Plot_Data('n', n_range, ' ',
        'Desired Transmitter Distance',  d_ts_range, 'm',
        'Coverage Probability', pr, ' ')  
     
            
            
            
           
           
           
            
            
         
    
    