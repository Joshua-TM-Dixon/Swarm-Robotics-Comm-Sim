import numpy as np
import networkx as nx
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
import Cox_Point as cp
import Graph_Functions as gph
import Sinr_Functions as Sinr


r = 10
T = 300
x_0 = 0
y_0 = 0
thr = 0.1
lambda_0 = 0.15
mu_0 = 0.1
n_sims = 100
sinr_threshold = 1


x_c, y_c = cp.gen_circle(r, x_0, y_0)

paths, nodes = cp.cox_point_process(r, x_0, y_0, lambda_0, mu_0)   
path_gdf = gph.create_path_gdf(paths)
node_gdf = gph.create_node_gdf(nodes)
intersection_gdf = gph.create_intersection_gdf(path_gdf) 

phys_nwk = nx.Graph()
gph.populate_graph(phys_nwk, path_gdf, intersection_gdf, node_gdf)
             
fig = plt.figure(figsize = (60, 60))
phys_ax = fig.add_subplot(121)
phys_ax.plot(x_0 + x_c, y_0 + y_c, color = 'black')
phys_point_pos = nx.get_node_attributes(phys_nwk, 'pos')
phys_point_cols = nx.get_node_attributes(phys_nwk, 'color').values()
phys_edge_cols = nx.get_edge_attributes(phys_nwk, 'color').values()
nx.draw(phys_nwk, pos = phys_point_pos, with_labels = True, ax = phys_ax, node_color = phys_point_cols, node_size = 20, edge_color = phys_edge_cols, width = 2, arrows = False)
phys_ax.axis('equal')

comm_ax = fig.add_subplot(122)
comm_ax.plot(x_0 + x_c, y_0 + y_c, color = 'black')
comm_node_pos = nx.get_node_attributes(comm_nwk, 'pos')
comm_node_cols = nx.get_node_attributes(comm_nwk, 'color').values()
comm_edge_cols = nx.get_edge_attributes(comm_nwk, 'color').values()
nx.draw(comm_nwk, pos = comm_node_pos, with_labels = True, ax = comm_ax, node_color = comm_node_cols, node_size = 20, edge_color = comm_edge_cols, width = 2, arrows = True, arrowstyle='->')
comm_ax.axis('equal')
plt.show()