import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import Cox_Point_Process as cpp
import Environment_Generation as eg
from shapely.geometry import Point

r = 100
centre_pos = Point(0, 0)
lambda_0 = 0.03
mu_0 = 0.01

def plot_data(x_c, y_c, env):
    plt.figure(figsize = (60, 60))
    plt.plot(centre_pos.x + x_c, centre_pos.y + y_c, color = 'black')
    phys_point_pos = nx.get_node_attributes(env.graph, 'pos')
    phys_point_cols = nx.get_node_attributes(env.graph, 'color').values()
    phys_edge_cols = nx.get_edge_attributes(env.graph, 'color').values()
    nx.draw(env.graph, pos = phys_point_pos, with_labels = False, node_color = phys_point_cols, node_size = 20, edge_color = phys_edge_cols, width = 2, arrows = False)
    nodes_to_label = [n for n, attr in env.graph.nodes(data = True) if attr.get("type") in ['Rx', 'Tx']]
    nx.draw_networkx_labels(env.graph, pos = phys_point_pos, verticalalignment = 'top',horizontalalignment = "right", labels = {n: n for n in nodes_to_label})
    plt.show()


phi = np.linspace(0, 2 * np.pi, 200)
x_c = centre_pos.x + r * np.cos(phi)
y_c = centre_pos.y + r * np.sin(phi)


cox_point = cpp.Cox_Point(r, centre_pos, lambda_0, mu_0)
paths, nodes = cox_point.run_process()
env = eg.Sim_Environment()   
env.gen_path_gdf(paths)
env.gen_node_gdf(nodes)
env.gen_intersection_gdf() 
env.populate_graph('black', 'grey', 'red', 'blue')
plot_data(x_c, y_c, env)