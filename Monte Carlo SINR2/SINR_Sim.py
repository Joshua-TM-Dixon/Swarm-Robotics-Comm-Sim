import numpy as np
import plotly.graph_objects as pgo

def l(d, k, B):
    return (k * d) ** B

def Gen_F(FS, mu, sigma):
    if FS == 'F' or FS == 'f' or FS == 0:
        return np.random.exponential(sigma)  
    elif FS == 'S' or FS == 's' or FS == 1:
        return np.random.lognormal(mu, sigma)
    
def Gen_node_pos(n, r, Tx_pos):
    theta = 2 * np.pi * np.random.uniform(0, 1, n)
    d = r * np.sqrt(np.random.uniform(0, 1, n))
    for i in range(n):
        Tx_pos.append([d[i], theta[i]])
    return Tx_pos

def  Pr(F, d, k, B, Pt):
    return F * l(d, k, B) * Pt

def Calc_SINR(F, Tx_pos, k, B, N, Pt):
    S = Pr(F, Tx_pos[0][0], k, B, Pt)
    I = np.sum(Pr(F, np.array(Tx_pos[1:][0]), k, B, 100))
    return S / (N + I)

def Monte_Carlo(s, n_range, S_Tx_d_range, k, B, N, Pt, T, r):
    C = []
    for n in n_range:
        for S_Tx_d in S_Tx_d_range:
            i = 0
            for j in range(s):
                Tx_pos = []
                Tx_pos.append([S_Tx_d, 0])
                Tx_pos = Gen_node_pos(n, r, Tx_pos)
                F = Gen_F('F', 0, 1)
                sinr = Calc_SINR(F, Tx_pos, k, B, N, Pt)
                if sinr > T:
                    i += 1
            C.append(i / s)
    return C
                
def Plot_Data(t_name, t_data, t_dim, x_name, x_data, x_dim, y_name, y_data, y_dim):
    fig = pgo.Figure()
    
    for i in range(len(t_data)):
        fig.add_trace(pgo.Scatter(x = list(x_data),
                                 y = [y_data[j + i * len(x_data)] for j in range(len(x_data))], 
                                 mode = 'lines+markers',
                                 name = f'{t_name} = {t_data[i]} {t_dim}'))
        
    fig.update_layout(title = f'{y_name} Against {x_name} For Each {t_name}',
                      xaxis_title = f"{x_name} ({x_dim})",
                      yaxis_title = f'{y_name} ({y_dim})',
                      legend = dict(x = 0, y = -0.1, orientation = 'h'))
    
    fig.show()

r = 20       
s = 1000
n_range = range(1, 11, 2)
S_Tx_d_range = np.linspace(0.1, 10, 50)
f = 2.4 * 10 ** 9
k = (4 * np.pi * f) / (3 * 10 ** 8)
B = -2
N = 0.0001
Pt = 100
T = 1
C = Monte_Carlo(s, n_range, S_Tx_d_range, k, B, N, Pt, T, r)
Plot_Data('n', n_range, ' ',
          'Desired Transmitter distance',  S_Tx_d_range, 'm',
          'Coverage Probability', C, ' ')