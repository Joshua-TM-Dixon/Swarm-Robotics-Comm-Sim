import numpy as np
import networkx as nx
from shapely.geometry import Point
import csv
import Environment_Generation as eg
import Cox_Point_Process as cpp
import Sinr_Functions as Sinr


def gen_environment(r, centre_pos, lambda_0, mu_0):
    cox_point = cpp.Cox_Point(r, centre_pos, lambda_0, mu_0)
    paths, nodes = cox_point.run_process()
    env = eg.Sim_Environment()   
    env.gen_path_gdf(paths)
    env.gen_node_gdf(nodes)
    env.gen_intersection_gdf() 
    env.populate_graph('black', 'lightgrey', 'grey', 'darkgrey')
    return env


def rand_movement(graph, n_robots):
    occupied_nodes = []
    node_ids = list(graph.nodes())
    np.random.shuffle(node_ids)
    for node_id in node_ids[:n_robots]:
        graph.nodes[node_id]['occupied'] = True
        graph.nodes[node_id]['colour'] = 'blue'
        occupied_nodes.append(node_id)
    return occupied_nodes


def check_point_on_line(point_l1, point_l2, point_p):
    cross_product = (point_p[1] - point_l1[1]) * (point_l2[0] - point_l1[0]) - (point_p[0] - point_l1[0]) * (point_l2[1] - point_l1[1])
    dot_product = (point_p[0] - point_l1[0]) * (point_l2[0] - point_l1[0]) + (point_p[1] - point_l1[1])*(point_l2[1] - point_l1[1])
    length_sqrd = (point_l2[0] - point_l1[0])**2 + (point_l2[1] - point_l1[1])**2
    if abs(cross_product) < 0.01 and dot_product > 0 and dot_product < length_sqrd:
        return 1
    else:
        return 0
 
   
def sel_fading_par(graph, node_tx, node_rx, occupied_nodes, m_los, m_nlos):
    m = m_los
    if any(path in graph.nodes[node_rx]['path_n'] for path in graph.nodes[node_tx]['path_n']):
        for node_intf in filter(lambda node_id: node_id != node_tx and node_id != node_rx, occupied_nodes):
            if check_point_on_line(graph.nodes[node_tx]['pos'], graph.nodes[node_rx]['pos'], graph.nodes[node_intf]['pos']) == True:
                m = m_nlos
                break
    return m


def calc_coverage_prob(n_sims, sinr_threshold, graph, node_tx, node_rx, occupied_nodes):

    B = 10**6
    f = 2.4835 * 10**9
    P_t = 10**(-5)
    G = 10**(2.15/10)
    m_los = 4
    m_nlos = 1
    omega = 0.75
    d_0 = 1
    a = 2
    T = 300
    N = Sinr.calc_noise_power(B, T)
    
    if not nx.has_path(graph, node_tx, node_rx):
        return 0
    
    count = 0
    for i in range(n_sims):
        m_tx = sel_fading_par(graph, node_tx, node_rx, occupied_nodes, m_los, m_nlos)
        F_tx = Sinr.gen_fading_var(m_tx, omega)
        d_tx = nx.shortest_path_length(graph, node_tx, node_rx)
        L_tx = Sinr.calc_path_loss(f, d_tx, d_0, a)
        P_rx_tx = Sinr.calc_rx_power(F_tx, P_t, G, G, L_tx) 
        
        P_rx_intf = []
        for node_intf in filter(lambda node_id: node_id != node_tx and node_id != node_rx, occupied_nodes):
            intf_state = np.random.choice([0, 1])
            if intf_state == 0 and nx.has_path(graph, node_intf, node_rx):
                m_intf = sel_fading_par(graph, node_intf, node_rx, occupied_nodes, m_los, m_nlos)
                F_intf = Sinr.gen_fading_var(m_intf, omega)
                d_intf = nx.shortest_path_length(graph, node_intf, node_rx)
                L_intf = Sinr.calc_path_loss(f, d_intf, d_0, a)
                P_rx_intf.append(Sinr.calc_rx_power(F_intf, P_t, G, G, L_intf))       
        
        sinr = Sinr.calc_sinr(P_rx_tx, P_rx_intf, N)
        if sinr > sinr_threshold:
            count += 1
    coverage_prob = count / n_sims
    return coverage_prob


def store_results(file_name, results):
    with open(file_name, mode = 'w', newline = '') as results_csv:
        writer = csv.DictWriter(results_csv, fieldnames = ['Tx', 'Rx', 'Coverage Probability'])
        writer.writeheader()
        for result in results:
            writer.writerow({'Tx': result[0], 'Rx': result[1], 'Coverage Probability': result[2]})