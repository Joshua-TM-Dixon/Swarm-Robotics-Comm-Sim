# Libraries
import numpy as np
import plotly.graph_objects as go
import Sinr_Functions as Sinr

# Global variables
coverage_Prob = []
n_sims = 1000

B = 10 ** 6  # Bandwidth in Hertz (Hz)     
f = 2.4835 * 10 ** 9  # Frequency in Hertz (Hz)   
P_tx = 10 ** (-5)  # Transmit power in Watts (W)      
G = 10 ** (-1)  # Antenna gain        
sinr_threshold = 1                 

r_env = 100  # Environment radius Meters (m)                               
T_env = 300  # Environment temperature in Kelvin (K)
n_tx_intf_range = range(0, 10, 2)  # Range in the number of interference transmitters
d_tx_tgt_range = np.linspace(0.1, 100, 50)  # Range of target transmitter distances


# Provides polar coordinates of a point in a circle
def gen_rand_point_on_circle(r_circle):
    theta = 2 * np.pi * np.random.uniform(0, 1)
    d = r_circle * np.sqrt(np.random.uniform(0, 1))
    return d, theta


# Plots generic figure containing 1 or more scatter graphs
def plot_data(t_name, t_data, t_units, x_axis_name, x_data, x_units, y_axis_name, y_data, y_units):
    fig = go.Figure()
    
    # Add scatter graphs
    for i in range(len(t_data)):
        fig.add_trace(go.Scatter(x = list(x_data),
                                 y = [y_data[j + i * len(x_data)] for j in range(len(x_data))], 
                                 mode = 'lines+markers',
                                 name = f'{t_name} = {t_data[i]} {t_units}'))
    
    # Modify graph appearance    
    fig.update_layout(
        title = dict(
            text = f'Graph of {y_axis_name} Against {x_axis_name}',
            font = dict(family = 'Arial', size = 26, color = 'black')),
        xaxis = dict(
            title = dict(
                text = f'{x_axis_name} ({x_units})',
                font = dict(family = 'Arial', size = 22, color = 'black')),
            tickfont = dict(family = 'Arial', size = 18, color = 'black')),
        yaxis = dict(
            title = dict(
                text = f'{y_axis_name} ({y_units})',
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
  
  
# Run Monte-Carlo simulation using communication parameters
N = Sinr.calc_noise_power(B, T_env)
for n_tx_intf in n_tx_intf_range:
    for d_tx_tgt in d_tx_tgt_range:
        count = 0
        for i in range (n_sims):
            L_tx_tgt = Sinr.calc_path_loss(f, d_tx_tgt, 2)
            F_tx_tgt = Sinr.gen_fading_var('F', 0, 1)
            P_rx_tgt = Sinr.calc_rx_power(F_tx_tgt, P_tx, G, G, L_tx_tgt)
            P_rx_intf = []
            for j in range(n_tx_intf):
                d_tx_intf, theta_tx_intf = gen_rand_point_on_circle(r_env)
                L_tx_inft = Sinr.calc_path_loss(f, d_tx_intf, 2)
                F_tx_intf = Sinr.gen_fading_var('F', 0, 1)
                P_rx_intf.append(Sinr.calc_rx_power(F_tx_intf, P_tx, G, G, L_tx_inft))
            sinr = Sinr.calc_sinr(P_rx_tgt, P_rx_intf, N)
            if sinr > sinr_threshold:
                count += 1
        coverage_Prob.append(count / n_sims)

plot_data('n', n_tx_intf_range, ' ',
        'Desired Transmitter Distance',  d_tx_tgt_range, 'm',
        'Coverage Probability', coverage_Prob, ' ')     
            
            
           
           
           
            
            
         
    
    