import numpy as np
import plotly.graph_objects as go
import Sinr_Functions as Sinr

# Global Variables
B = 10 ** 6   
f = 2.4835 * 10 ** 9   
P_tx = 10 ** (-5)    
G = 10 ** (-1)    
sinr_threshold = 1                 

r = 100                            
T_range = np.linspace(250, 350, 5)
n_sims = 5000
m = np.random.choice([1, 4])
omega = 0.75
d_0 = 0.01 * r
a_range = np.linspace(2, 2, 1)
n_tx_intf_range = range(2, 3, 1)
d_tx_tgt_range = np.linspace(0.1, 60, 30)


def gen_rand_point_on_circle(r_circle):
    """
    Generate a random point on a circle.

    Parameters:
        r_circle (float): Radius of the circle.

    Returns:
        tuple: Distance from (0,0) and angle from the x-axis of the point.
    """
    theta = 2 * np.pi * np.random.uniform(0, 1)
    d = r_circle * np.sqrt(np.random.uniform(0, 1))
    return d, theta

def plot_data(t_name, t_data, t_units, x_axis_name, x_data, x_units, y_axis_name, y_data, y_units):
    """
    Plot data using Plotly.

    Parameters:
        t_name (str): Name of the variable for which data is plotted.
        t_data (list): List of values for the variable.
        t_units (str): Units of the variable.
        x_axis_name (str): Name of the x-axis.
        x_data (list): List of values for the x-axis.
        x_units (str): Units of the x-axis.
        y_axis_name (str): Name of the y-axis.
        y_data (list): List of values for the y-axis.
        y_units (str): Units of the y-axis.
    """
    fig = go.Figure()
    
    for i in range(len(t_data)):
        fig.add_trace(go.Scatter(x = list(x_data),
                                 y = [y_data[j + i * len(x_data)] for j in range(len(x_data))], 
                                 mode = 'lines+markers',
                                 name = f'{t_name} = {t_data[i]} {t_units}'))
       
    fig.update_layout(
        title = dict(
            text = f'Graph of {y_axis_name} Against {x_axis_name}',
            font = dict(family = 'Arial', size = 26, color = 'black')),
        xaxis = dict(
            title = dict(
                text = f'{x_axis_name} {x_units}',
                font = dict(family = 'Arial', size = 22, color = 'black')),
            tickfont = dict(family = 'Arial', size = 18, color = 'black')),
        yaxis = dict(
            title = dict(
                text = f'{y_axis_name} {y_units}',
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

# Simulation
coverage_Prob = []
for T in T_range:  
    N = Sinr.calc_noise_power(B, T)
    for n_tx_intf in n_tx_intf_range:
        for d_tx_tgt in d_tx_tgt_range:
            for a in a_range:
                count = 0
                # Monte-Carlo Process
                for i in range (n_sims):
                    L_tx_tgt = Sinr.calc_path_loss(f, d_tx_tgt, d_0, a)
                    F_tx_tgt = Sinr.gen_fading_var(m, omega)
                    P_rx_tgt = Sinr.calc_rx_power(F_tx_tgt, P_tx, G, G, L_tx_tgt)
                    P_rx_intf = []
                    for j in range(n_tx_intf):
                        d_tx_intf, theta_tx_intf = gen_rand_point_on_circle(r)
                        L_tx_inft = Sinr.calc_path_loss(f, d_tx_intf, d_0, a)
                        F_tx_intf = Sinr.gen_fading_var(m, omega)
                        P_rx_intf.append(Sinr.calc_rx_power(F_tx_intf, P_tx, G, G, L_tx_inft))
                    sinr = Sinr.calc_sinr(P_rx_tgt, P_rx_intf, N)
                    if sinr > sinr_threshold:
                        count += 1
                coverage_Prob.append(count / n_sims)

plot_data('T', T_range, '(K)',
        'Desired Transmitter Distance',  d_tx_tgt_range, '(m)',
        'Coverage Probability', coverage_Prob, ' ')     
            
            
           
           
           
            
            
         
    
    