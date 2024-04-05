import numpy as np
import networkx as nx
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
import Cox_Point as cp
import Graph_Functions as gph
import Sinr_Functions as Sinr
import Robot as rb


r = 10
T = 300
x_0 = 0
y_0 = 0
thr = 0.1
lambda_0 = 0.1
mu_0 = 0.1


m_los = 4
m_nlos = 1
omega = 0.75
a = 2
n_sims = 100
n_robots = 15
sinr_threshold = 0.5


def check_point_on_line(point_l1, point_l2, point_p):
    cross_product = (point_p[1] - point_l1[1]) * (point_l2[0] - point_l1[0]) - (point_p[0] - point_l1[0]) * (point_l2[1] - point_l1[1])
    dot_product = (point_p[0] - point_l1[0]) * (point_l2[0] - point_l1[0]) + (point_p[1] - point_l1[1])*(point_l2[1] - point_l1[1])
    length_sqrd = (point_l2[0] - point_l1[0])**2 + (point_l2[1] - point_l1[1])**2
    if abs(cross_product) < 0.01 and dot_product > 0 and dot_product < length_sqrd:
        return 1
    else:
        return 0

def calc_link_par(robots,tx, rx, m_los, m_nlos, omega, a):
    common_path_n = None
    m = m_nlos
    for path_n_tx in tx.path_n:
        if path_n_tx in rx.path_n:
            common_path = path_n_tx
            break
        
    if common_path_n:
        for robot in robots:
            if common_path_n in robot.path_n:
                if check_point_on_line([tx.x, tx.y], [rx.x, rx.y], [robot.x, robot.y]) == False:
                    m = m_los

    d = np.sqrt((tx.x - rx.x)** 2 + (tx.y - rx.y)** 2)
    L = Sinr.calc_path_loss(tx.f, d, a)
    F = Sinr.gen_fading_var(m, omega)
    
    return d, L, F


x_c, y_c = cp.gen_circle(r, x_0, y_0)


phys_nwk = nx.Graph()
paths, nodes = cp.cox_point_process(r, x_0, y_0, lambda_0, mu_0, n_robots)   
path_gdf = gph.create_path_gdf(paths)
node_gdf = gph.create_node_gdf(nodes)
intersection_gdf = gph.create_intersection_gdf(path_gdf) 
gph.populate_graph(phys_nwk, 'black', path_gdf, 'lightgrey', intersection_gdf, 'grey', node_gdf, 'darkgrey')


comm_nwk = nx.Graph()
robots = []
for i in range(n_robots):
    robots.append(rb.Robot(i, 10 ** 6, 2.4835 * 10 ** 9, 10 ** (-5), 10 ** (-1)))    


phys_nodes = list(phys_nwk.nodes())
np.random.shuffle(phys_nodes)
for i, phys_node in enumerate(phys_nodes[:n_robots]):
    node_x, node_y = phys_nwk.nodes[phys_node]['pos']
    path_n = phys_nwk.nodes[phys_node]['path_n']
    robots[i].update(path_n, node_x, node_y)
        

for robot in robots:
    phys_nwk.add_node(robot.name, pos = (robot.x, robot.y), color = robot.col, type = robot.state, path_n = robot.path_n)
    comm_nwk.add_node(robot.name, pos = (robot.x, robot.y), color = robot.col, type = robot.state, path_n = robot.path_n)


coverage_probs = []
N = Sinr.calc_noise_power(robots[0].B, T)
for tx_tgt in filter(lambda robot: robot.state == 'Tx', robots):
    for rx_tgt in filter(lambda robot: robot.state == 'Rx', robots):
        
        count = 0
        for i in range(n_sims):
            d_tx_tgt, L_tx_tgt, F_tx_tgt = calc_link_par(robots, tx_tgt, rx_tgt, m_los, m_nlos, omega, a)
            P_rx_tgt = Sinr.calc_rx_power(F_tx_tgt, tx_tgt.P_t, tx_tgt.G, rx_tgt.G, L_tx_tgt)  
            P_rx_intf = []
            for tx_intf in filter(lambda robot: robot.state == 'Tx' and robot.name != tx_tgt.name, robots):
                d_tx_intf, L_tx_intf, F_tx_intf = calc_link_par(robots, tx_intf, rx_tgt, m_los, m_nlos, omega, a)
                P_rx_intf.append(Sinr.calc_rx_power(F_tx_intf, tx_intf.P_t, tx_intf.G, rx_tgt.G, L_tx_intf))
            
            sinr = Sinr.calc_sinr(P_rx_tgt, P_rx_intf, N)
            if sinr > sinr_threshold:
                count += 1
        coverage_prob = count / n_sims
        print(tx_tgt.name, rx_tgt.name, count / n_sims)
        if coverage_prob > 0.1:
            coverage_probs.append(count / n_sims)
            if coverage_prob > 0.5:
                link_col = 'green'
            else:
                link_col = 'orange'
            comm_nwk.add_edge(tx_tgt.name, rx_tgt.name, color = link_col)
            phys_nwk.add_edge(tx_tgt.name, rx_tgt.name, color = link_col)
            
                   
fig = plt.figure(figsize = (60, 60))
phys_ax = fig.add_subplot(121)
phys_ax.plot(x_0 + x_c, y_0 + y_c, color = 'black')
phys_point_pos = nx.get_node_attributes(phys_nwk, 'pos')
phys_point_cols = nx.get_node_attributes(phys_nwk, 'color').values()
phys_edge_cols = nx.get_edge_attributes(phys_nwk, 'color').values()
nx.draw(phys_nwk, pos = phys_point_pos, with_labels = False, ax = phys_ax, node_color = phys_point_cols, node_size = 20, edge_color = phys_edge_cols, width = 2, arrows = False)
nodes_to_label = [n for n, attr in phys_nwk.nodes(data = True) if attr.get("type") in ['Rx', 'Tx']]
nx.draw_networkx_labels(phys_nwk, pos = phys_point_pos, ax = phys_ax, verticalalignment = 'top',horizontalalignment = "right", labels = {n: n for n in nodes_to_label})
phys_ax.axis('equal')

comm_ax = fig.add_subplot(122)
comm_ax.plot(x_0 + x_c, y_0 + y_c, color = 'black')
comm_node_pos = nx.get_node_attributes(comm_nwk, 'pos')
comm_node_cols = nx.get_node_attributes(comm_nwk, 'color').values()
comm_edge_cols = nx.get_edge_attributes(comm_nwk, 'color').values()
nx.draw(comm_nwk, pos = comm_node_pos, with_labels = True, ax = comm_ax, node_color = comm_node_cols, node_size = 20, edge_color = comm_edge_cols, width = 2, arrows = True, arrowstyle='->')
comm_ax.axis('equal')
plt.show()