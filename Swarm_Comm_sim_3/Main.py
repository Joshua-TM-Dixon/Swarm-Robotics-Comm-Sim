import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point
import Sinr_Functions as Sinr
import Sim_functions as sim
import Robot as rb

r = 10
T = 300
centre_pos = Point(0, 0)
lambda_0 = 0.2
mu_0 = 0.1
n_sims = 100
n_robots = 30
m_los = 4
m_nlos = 1
omega = 0.75
d_0 = 0.01 * r
a = 2
sinr_threshold = 1

x_c, y_c = sim.gen_circle(r, centre_pos)
env = sim.gen_environment(r, centre_pos, lambda_0, mu_0)
comm_nwk = nx.Graph()

robots = []
for i in range(n_robots):
    robots.append(rb.Robot(i, 10 ** 6, 2.4835 * 10 ** 9, 10 ** (-5), 10 ** (2.15 / 10)))    
sim.rand_movement(env.graph, robots)
for robot in robots:
    env.graph.add_node(robot.name, pos = (robot.pos.x, robot.pos.y), color = robot.col, type = robot.state, path_n = robot.path_n)
    comm_nwk.add_node(robot.name, pos = (robot.pos.x, robot.pos.y), color = robot.col, type = robot.state, path_n = robot.path_n)

results = []
N = Sinr.calc_noise_power(robots[0].B, T)
for tx_tgt in filter(lambda robot: robot.state == 'Tx', robots):
    for rx_tgt in filter(lambda robot: robot.state == 'Rx', robots):
            coverage_prob = sim.calc_coverage_prob(n_sims, robots, tx_tgt, rx_tgt, sinr_threshold, N, m_los, m_nlos, omega, d_0, a)
            if coverage_prob > 0.1:
                results.append([tx_tgt.name, rx_tgt.name, coverage_prob])
                if coverage_prob > 0.9:
                    comm_nwk.add_edge(tx_tgt.name, rx_tgt.name, color = 'green')
                elif coverage_prob > 0.5:
                    comm_nwk.add_edge(tx_tgt.name, rx_tgt.name, color = 'orange')
                else:
                    comm_nwk.add_edge(tx_tgt.name, rx_tgt.name, color = 'red')   

sim.store_results('Simulation_Results.csv', results)           
           
fig = plt.figure(figsize = (60, 60))
phys_ax = fig.add_subplot(121)
phys_ax.plot(centre_pos.x + x_c, centre_pos.y + y_c, color = 'black')
phys_point_pos = nx.get_node_attributes(env.graph, 'pos')
phys_point_cols = nx.get_node_attributes(env.graph, 'color').values()
phys_edge_cols = nx.get_edge_attributes(env.graph, 'color').values()
nx.draw(env.graph, pos = phys_point_pos, with_labels = False, ax = phys_ax, node_color = phys_point_cols, node_size = 20, edge_color = phys_edge_cols, width = 2, arrows = False)
nodes_to_label = [n for n, attr in env.graph.nodes(data = True) if attr.get("type") in ['Rx', 'Tx']]
nx.draw_networkx_labels(env.graph, pos = phys_point_pos, ax = phys_ax, verticalalignment = 'top',horizontalalignment = "right", labels = {n: n for n in nodes_to_label})
phys_ax.axis('equal')

comm_ax = fig.add_subplot(122)
comm_ax.plot(centre_pos.x + x_c, centre_pos.y + y_c, color = 'black')
comm_node_pos = nx.get_node_attributes(comm_nwk, 'pos')
comm_node_cols = nx.get_node_attributes(comm_nwk, 'color').values()
comm_edge_cols = nx.get_edge_attributes(comm_nwk, 'color').values()
nx.draw(comm_nwk, pos = comm_node_pos, with_labels = True, ax = comm_ax, node_color = comm_node_cols, node_size = 20, edge_color = comm_edge_cols, width = 2, arrows = True, arrowstyle='->')
comm_ax.axis('equal')
plt.show()