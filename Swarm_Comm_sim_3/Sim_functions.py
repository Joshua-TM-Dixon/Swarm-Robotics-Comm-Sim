import numpy as np
import networkx as nx
from shapely.geometry import Point
import csv
import Environment_Generation as eg
import Cox_Point_Process as cpp
import Sinr_Functions as Sinr

def gen_circle(r, centre_pos):
    theta = np.linspace(0, 2 * np.pi, 200)
    x = centre_pos.x + r * np.cos(theta)
    y = centre_pos.y + r * np.sin(theta)
    return x, y

def gen_environment(r, centre_pos, lambda_0, mu_0):
    cox_point = cpp.Cox_Point(r, centre_pos, lambda_0, mu_0)
    paths, nodes = cox_point.run_process()
    env = eg.Sim_Environment()   
    env.gen_path_gdf(paths)
    env.gen_node_gdf(nodes)
    env.gen_intersection_gdf() 
    env.populate_graph('black', 'lightgrey', 'grey', 'darkgrey')
    return env

def rand_movement(graph, robots):
    phys_nodes = list(graph.nodes())
    np.random.shuffle(phys_nodes)
    for i, phys_node in enumerate(phys_nodes[:len(robots)]):
        node_x, node_y = graph.nodes[phys_node]['pos']
        path_n = graph.nodes[phys_node]['path_n']
        robots[i].update(path_n, Point(node_x, node_y))

def check_point_on_line(point_l1, point_l2, point_p):
    cross_product = (point_p.y - point_l1.y) * (point_l2.x - point_l1.x) - (point_p.x - point_l1.x) * (point_l2.y - point_l1.y)
    dot_product = (point_p.x - point_l1.x) * (point_l2.x - point_l1.x) + (point_p.y - point_l1.y)*(point_l2.y - point_l1.y)
    length_sqrd = (point_l2.x - point_l1.x)**2 + (point_l2.y - point_l1.y)**2
    if abs(cross_product) < 0.01 and dot_product > 0 and dot_product < length_sqrd:
        return 1
    else:
        return 0

def sel_fading_par(robots, robot_1, robot_2, m_los, m_nlos):
    m = m_los
    for robot_3 in filter(lambda robot_3: robot_3.name != robot_1.name and robot_3.name != robot_2.name, robots):
        if check_point_on_line(robot_1.pos, robot_2.pos, robot_3.pos) == True:
            m = m_nlos
            break
    return m

def calc_coverage_prob(n_sims, robots, tx_tgt, rx_tgt, sinr_threshold, N, m_los, m_nlos, omega, d_0, a):
    common_path_n = None
    for path_n_tx in tx_tgt.path_n:
        if path_n_tx in rx_tgt.path_n:
            common_path_n = path_n_tx
            break
    if common_path_n:
        count = 0
        for i in range(n_sims):
            m_tgt = sel_fading_par(robots, tx_tgt, rx_tgt, m_los, m_nlos)
            F_tgt = Sinr.gen_fading_var(m_tgt, omega)
            d_tgt = np.sqrt((tx_tgt.pos.x - rx_tgt.pos.x)** 2 + (tx_tgt.pos.y - rx_tgt.pos.y)** 2)
            L_tgt = Sinr.calc_path_loss(tx_tgt.f, d_tgt, d_0, a)
            P_rx_tgt = Sinr.calc_rx_power(F_tgt, tx_tgt.P_t, tx_tgt.G, rx_tgt.G, L_tgt) 
            
            P_rx_intf = []
            for tx_intf in filter(lambda robot: robot.state == 'Tx' and robot.name != tx_tgt.name, robots):
                if common_path_n in tx_intf.path_n:
                    m_intf = sel_fading_par(robots, tx_intf, rx_tgt, m_los, m_nlos)
                    F_intf = Sinr.gen_fading_var(m_intf, omega)
                    d_intf = np.sqrt((tx_intf.pos.x - rx_tgt.pos.x)** 2 + (tx_intf.pos.y - rx_tgt.pos.y)** 2)
                    L_intf = Sinr.calc_path_loss(tx_intf.f, d_intf, d_0, a)
                    P_rx_intf.append(Sinr.calc_rx_power(F_intf, tx_intf.P_t, tx_intf.G, rx_tgt.G, L_intf))       
            
            sinr = Sinr.calc_sinr(P_rx_tgt, P_rx_intf, N)
            if sinr > sinr_threshold:
                count += 1
        coverage_prob = count / n_sims
    else:
        coverage_prob = 0
    return coverage_prob

def store_results(file_name, results):
    with open(file_name, mode = 'w', newline = '') as results_csv:
        writer = csv.DictWriter(results_csv, fieldnames = ['Tx', 'Rx', 'Coverage Probability'])
        writer.writeheader()
        for result in results:
            writer.writerow({'Tx': result[0], 'Rx': result[1], 'Coverage Probability': result[2]})