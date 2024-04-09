import numpy as np
import networkx as nx
import Graph_Functions as gph
import Cox_Point as cp
import Sinr_Functions as Sinr

# Generates 200 points evenly distributed on a circle
def gen_circle(r, x_0, y_0):
    theta = np.linspace(0, 2 * np.pi, 200)
    x = x_0 + r * np.cos(theta)
    y = y_0 + r * np.sin(theta)
    return x, y


def gen_phys_nwk(r, x_0, y_0, lambda_0, mu_0):
    phys_nwk = nx.Graph()
    paths, nodes = cp.cox_point_process(r, x_0, y_0, lambda_0, mu_0)   
    path_gdf = gph.create_path_gdf(paths)
    node_gdf = gph.create_node_gdf(nodes)
    intersection_gdf = gph.create_intersection_gdf(path_gdf) 
    gph.populate_graph(phys_nwk, 'black', path_gdf, 'lightgrey', intersection_gdf, 'grey', node_gdf, 'darkgrey')
    return phys_nwk


def rand_movement(phys_nwk, robots):
    phys_nodes = list(phys_nwk.nodes())
    np.random.shuffle(phys_nodes)
    for i, phys_node in enumerate(phys_nodes[:len(robots)]):
        node_x, node_y = phys_nwk.nodes[phys_node]['pos']
        path_n = phys_nwk.nodes[phys_node]['path_n']
        robots[i].update(path_n, node_x, node_y)


def check_point_on_line(point_l1, point_l2, point_p):
    cross_product = (point_p[1] - point_l1[1]) * (point_l2[0] - point_l1[0]) - (point_p[0] - point_l1[0]) * (point_l2[1] - point_l1[1])
    dot_product = (point_p[0] - point_l1[0]) * (point_l2[0] - point_l1[0]) + (point_p[1] - point_l1[1])*(point_l2[1] - point_l1[1])
    length_sqrd = (point_l2[0] - point_l1[0])**2 + (point_l2[1] - point_l1[1])**2
    if abs(cross_product) < 0.01 and dot_product > 0 and dot_product < length_sqrd:
        return 1
    else:
        return 0


def sel_fading_par(robots, robot_1, robot_2, m_los, m_nlos):
    m = m_los
    for robot_3 in filter(lambda robot_3: robot_3.name != robot_1.name and robot_3.name != robot_2.name, robots):
        if check_point_on_line([robot_1.x, robot_1.y], [robot_2.x, robot_2.y], [robot_3.x, robot_3.y]) == True:
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
            d_tgt = np.sqrt((tx_tgt.x - rx_tgt.x)** 2 + (tx_tgt.y - rx_tgt.y)** 2)
            L_tgt = Sinr.calc_path_loss(tx_tgt.f, d_tgt, d_0, a)
            P_rx_tgt = Sinr.calc_rx_power(F_tgt, tx_tgt.P_t, tx_tgt.G, rx_tgt.G, L_tgt) 
            
            P_rx_intf = []
            for tx_intf in filter(lambda robot: robot.state == 'Tx' and robot.name != tx_tgt.name, robots):
                if common_path_n in tx_intf.path_n:
                    m_intf = sel_fading_par(robots, tx_intf, rx_tgt, m_los, m_nlos)
                    F_intf = Sinr.gen_fading_var(m_intf, omega)
                    d_intf = np.sqrt((tx_intf.x - rx_tgt.x)** 2 + (tx_intf.y - rx_tgt.y)** 2)
                    L_intf = Sinr.calc_path_loss(tx_intf.f, d_intf, d_0, a)
                    P_rx_intf.append(Sinr.calc_rx_power(F_intf, tx_intf.P_t, tx_intf.G, rx_tgt.G, L_intf))       
            
            sinr = Sinr.calc_sinr(P_rx_tgt, P_rx_intf, N)
            if sinr > sinr_threshold:
                count += 1
        coverage_prob = count / n_sims
    else:
        coverage_prob = 0
    return coverage_prob