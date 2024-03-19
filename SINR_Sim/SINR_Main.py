# Libraries
import numpy as np
import plotly.graph_objects as go
import SINR_Functions as Sinr

# Functions

    # Generates n random node positions on a circle with radius r and returns
    # a list of distances and angles for all nodes
def Gen_node_pos(n, r):
    theta = 2 * np.pi * np.random.uniform(0, 1, n)
    d = r * np.sqrt(np.random.uniform(0, 1, n))
    return d, theta


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
    
    # Runs Monte-Carlo simulation using communication parameters
def Monte_Carlo():
    
    # Simulation variables
    pr = []        # Coverage probability
    sim = 10000    # Number of simulations
    
    # Signal variables
    B = 10 ** 6             # Bandwidth (Hz)
    f = 2.4835 * 10 ** 9    # Frequency (Hz)
    P_t = 10 ** (-5)        # Transmitter power (W)
    G = 10 ** (-1)          # Antenna gain
    thr = 1                 # SINR threshold
    
    # Environment variables
    r = 10                                  # Radius of circle (m)
    T = 300                                 # temperature (K)
    n_range = range(3, 12, 2)               # range of number of interference nodes
    d_ts_range = np.linspace(0.1, r, 50)    # range of desired transmitter distances from receiver (m)
    
    # Simulation
    N = Sinr.Calc_N(B, T)
    for n in n_range:
        F = Sinr.Gen_F('F', 0, 1)
        for d_ts in d_ts_range:
            c = 0
            L_ts = Sinr.Calc_L(f, d_ts, 2)
            P_rs = Sinr.Calc_P_r(F, P_t, G, G, L_ts)
            for j in range (sim):
                d_ti, theta_ti = Gen_node_pos(n, r)
                L_ti = Sinr.Calc_L(f, d_ti, 2)
                P_ri = Sinr.Calc_P_r(F, P_t, G, G, L_ti)
                sinr = Sinr.Calc_SINR(P_rs, P_ri, N)
                if sinr > thr:
                    c += 1
            pr.append(c / sim)

    # Graph
    Plot_Data('n', n_range, ' ',
          'Desired Transmitter Distance',  d_ts_range, 'm',
          'Coverage Probability', pr, ' ')  

Monte_Carlo()       
            
            
           
           
           
            
            
         
    
    