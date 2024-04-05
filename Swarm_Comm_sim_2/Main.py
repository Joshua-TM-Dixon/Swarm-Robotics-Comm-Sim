import networkx as nx
import matplotlib.pyplot as plt
import Sinr_Functions as Sinr
import Sim_functions as sim
import Robot as rb


r = 10
T = 300
x_0 = 0
y_0 = 0
lambda_0 = 0.2
mu_0 = 0.1

n_sims = 100
n_robots = 20
sinr_threshold = 1


x_c, y_c = sim.gen_circle(r, x_0, y_0)
phys_nwk = sim.gen_phys_nwk(r, x_0, y_0, lambda_0, mu_0)
comm_nwk = nx.Graph()


robots = []
for i in range(n_robots):
    robots.append(rb.Robot(i, 10 ** 6, 2.4835 * 10 ** 9, 10 ** (-5), 10 ** (-1)))    
sim.rand_movement(phys_nwk, robots)
for robot in robots:
    phys_nwk.add_node(robot.name, pos = (robot.x, robot.y), color = robot.col, type = robot.state, path_n = robot.path_n)
    comm_nwk.add_node(robot.name, pos = (robot.x, robot.y), color = robot.col, type = robot.state, path_n = robot.path_n)


results = []
N = Sinr.calc_noise_power(robots[0].B, T)
for tx_tgt in filter(lambda robot: robot.state == 'Tx', robots):
    for rx_tgt in filter(lambda robot: robot.state == 'Rx', robots):
            coverage_prob = sim.calc_coverage_prob(n_sims, robots, tx_tgt, rx_tgt, sinr_threshold, N)
            
            print(tx_tgt.name, tx_tgt.path_n, rx_tgt.name, rx_tgt.path_n, coverage_prob)
            if coverage_prob > 0.9:
                results.append({'Transmitter': tx_tgt.name, 'Receiver': rx_tgt.name, 'Coverage Probability': coverage_prob})
                comm_nwk.add_edge(tx_tgt.name, rx_tgt.name, color = 'green')
            elif coverage_prob > 0.5:
                comm_nwk.add_edge(tx_tgt.name, rx_tgt.name, color = 'orange')
            elif coverage_prob > 0.1:
                comm_nwk.add_edge(tx_tgt.name, rx_tgt.name, color = 'red')
                
                   
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