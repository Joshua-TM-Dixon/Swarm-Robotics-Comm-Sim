import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point
import Sim_functions as sim

r = 10
centre_pos = Point(0, 0)
lambda_0 = 0.3
mu_0 = 0.1

n_sims = 100
n_robots = 20
sinr_threshold = 1



env = sim.gen_environment(r, centre_pos, lambda_0, mu_0) 
occupied_nodes = sim.rand_movement(env.graph, n_robots)
comm_nwk = nx.Graph()
node_ids = list(env.graph.nodes())
for node_id in node_ids:
    node = env.graph.nodes[node_id]
    if node['occupied'] == True:
        comm_nwk.add_node(node_id, pos = node['pos'], color = node['colour'])

results = []
for node_tx in occupied_nodes:
    for node_rx in filter(lambda node_id: node_id != node_tx, occupied_nodes):
            coverage_prob = sim.calc_coverage_prob(n_sims, sinr_threshold, env.graph, node_tx, node_rx, occupied_nodes)
            if coverage_prob > 0.1:
                results.append([node_tx, node_rx, coverage_prob])
                if coverage_prob > 0.9:
                    comm_nwk.add_edge(node_tx, node_rx, color = 'green')
                elif coverage_prob > 0.5:
                    comm_nwk.add_edge(node_tx, node_rx, color = 'orange')
                else:
                    comm_nwk.add_edge(node_tx, node_rx, color = 'red')   

sim.store_results('Simulation_Results.csv', results)           
           
fig = plt.figure(figsize = (60, 60))
phys_ax = fig.add_subplot(121)
phys_point_pos = nx.get_node_attributes(env.graph, 'pos')
phys_point_cols = nx.get_node_attributes(env.graph, 'color').values()
phys_edge_cols = nx.get_edge_attributes(env.graph, 'color').values()
nx.draw(env.graph, pos = phys_point_pos, with_labels = False, ax = phys_ax, node_color = phys_point_cols, node_size = 20, edge_color = phys_edge_cols, width = 2, arrows = False)
nodes_to_label = [n for n, attr in env.graph.nodes(data = True) if attr.get("type") in ['Rx', 'Tx']]
nx.draw_networkx_labels(env.graph, pos = phys_point_pos, ax = phys_ax, verticalalignment = 'top',horizontalalignment = "right", labels = {n: n for n in nodes_to_label})
phys_ax.axis('equal')

comm_ax = fig.add_subplot(122)
comm_node_pos = nx.get_node_attributes(comm_nwk, 'pos')
comm_node_cols = nx.get_node_attributes(comm_nwk, 'color').values()
comm_edge_cols = nx.get_edge_attributes(comm_nwk, 'color').values()
nx.draw(comm_nwk, pos = comm_node_pos, with_labels = False, ax = comm_ax, node_color = comm_node_cols, node_size = 20, edge_color = comm_edge_cols, width = 2, arrows = True, arrowstyle='->')
comm_ax.axis('equal')
plt.show()