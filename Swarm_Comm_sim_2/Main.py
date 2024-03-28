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
n_sims = 100
n_robots = 15
sinr_threshold = 1


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

unique_nodes = []
while len(unique_nodes) < n_robots:
    rand_i = np.random.randint(0, len(node_gdf))
    random_node = node_gdf.iloc[rand_i]
    print(random_node['name'])
    if random_node['name'] not in unique_nodes:
        robots[len(unique_nodes)].update(random_node['path_n'], random_node['geometry'].x, random_node['geometry'].y)
        unique_nodes.append(random_node['name']) 

for robot in robots:
    phys_nwk.add_node(robot.name, pos = (robot.x, robot.y), color = robot.col, type = robot.state)
    comm_nwk.add_node(robot.name, pos = (robot.x, robot.y), color = robot.col, type = robot.state)

         
fig = plt.figure(figsize = (60, 60))
phys_ax = fig.add_subplot(121)
phys_ax.plot(x_0 + x_c, y_0 + y_c, color = 'black')
phys_point_pos = nx.get_node_attributes(phys_nwk, 'pos')
phys_point_cols = nx.get_node_attributes(phys_nwk, 'color').values()
phys_edge_cols = nx.get_edge_attributes(phys_nwk, 'color').values()
nx.draw(phys_nwk, pos = phys_point_pos, with_labels = False, ax = phys_ax, node_color = phys_point_cols, node_size = 20, edge_color = phys_edge_cols, width = 2, arrows = False)
nodes_to_label = [n for n, attr in phys_nwk.nodes(data=True) if attr.get("type") in ['Rx', 'Tx']]
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