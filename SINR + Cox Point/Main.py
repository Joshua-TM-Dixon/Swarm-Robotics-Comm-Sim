import numpy as np
import plotly.graph_objects as go
import Circle as cr
import Path as pa
import Node as nd
import Link as lk
import Sinr

r = 10
T = 300
x_0 = 0
y_0 = 0

B = 10 ** 6
f = 2.4835 * 10 ** 9
P_t = 10 ** (-5)
G = 10 ** (-1)
thr = 0.1

lambda_0 = 0.2
mu_0 = 0.3

circle = cr.Circle('Area', r, x_0, y_0)

paths = []
Tx = []
Rx = []
links = [] 

n_paths = np.random.poisson(2 * np.pi * r * lambda_0)
for i in range(n_paths):
    path = pa.Path(i, r, x_0, y_0)
    
    n_tx = 0 
    n_rx = 0
    path_Tx = []
    path_Rx = []
    n_nodes = np.random.poisson(2 * path.q * mu_0)
    for j in range(n_nodes):
        node = nd.Node(j, path, B, f, P_t, G, thr, x_0, y_0)
        
        if node.state == 0:
           node.node_n = n_tx
           n_tx += 1
           path_Tx.append(node)
        else:
            node.node_n = n_rx
            n_rx += 1
            path_Rx.append(node)
    
    path_links = []     
    for k, tx in enumerate(path_Tx):
        d_min = float('inf')
        opt_rx = None
        for rx in path_Rx:
            d = np.sqrt((tx.x - rx.x) ** 2 + (tx.y - rx.y) ** 2)
            if d > 0 and d < d_min:
                d_min = d
                opt_rx = rx
        
        if opt_rx is not None:       
            tx.active = 1
            opt_rx.active = 1
            link = lk.Link(i, k, tx, opt_rx, 2)
            path_links.append(link)
    
    links.append(path_links)   
    Tx.append(path_Tx)
    Rx.append(path_Rx)
    paths.append(path)
 

N = Sinr.Calc_N(B, T)
for path_links in links:
    for link in path_links:
        
        c = 0
        P_ri = []
        for path_Tx in Tx:
            for tx in path_Tx:
                if tx.active == 1:
                    F = Sinr.Gen_F('F', 0, 1)
                    d = np.sqrt((link.rx.x - tx.x) ** 2 + (link.rx.y - tx.y) ** 2)
                    L = Sinr.Calc_L(tx.f, d, 2)
                    P_r = Sinr.Calc_P_r(F, tx.P_t, tx.G, link.rx.G, L)
                    P_ri.append(P_r)
        
        link.sinr = Sinr.Calc_SINR(link.P_r, P_ri, N)
   
        
fig = go.Figure()

fig.add_trace(circle.Draw())

for path in paths:
    fig.add_trace(path.Draw())

for path_links in links:
    for link in path_links:
        fig.add_trace(link.Draw())
    
for path_Tx in Tx:
    for tx in path_Tx:
        fig.add_trace(tx.Draw())
    
for path_Rx in Rx:
    for rx in path_Rx:
        fig.add_trace(rx.Draw())

fig.show()     
               
                    
        