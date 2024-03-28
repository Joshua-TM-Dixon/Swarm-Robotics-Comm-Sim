import numpy as np
import networkx as nx
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import Cox_Point as cp
import Sinr_Functions as Sinr


r = 10
T = 300
x_0 = 0
y_0 = 0
thr = 0.1
lambda_0 = 0.25
mu_0 = 0.15
n_sims = 100
sinr_threshold = 1


x_c, y_c = cp.gen_circle(r, x_0, y_0)
paths, robots = cp.cox_point_process(r, x_0, y_0, lambda_0, mu_0)   

   
path_gdf = gpd.GeoDataFrame(geometry = paths) 
path_gdf['center_point'] = path_gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
path_gdf['center_point'] = [coords[0] for coords in path_gdf['center_point']]
for i, path in path_gdf.iterrows():
        path_gdf.loc[i, 'path_n'] = str(i)
    
  
intersections_gdf = pd.DataFrame()
for i, path in path_gdf.iterrows():
    path_intrs = path_gdf.intersection(path['geometry'])
    path_intr_points = path_intrs[path_intrs.geom_type == 'Point']
    path_intrs_df = pd.DataFrame(path_intr_points)
    path_intrs_df['path_n2'] = path['path_n']
    path_intrs_df = path_intrs_df.join(path_gdf['path_n'])
    intersections_gdf= pd.concat([intersections_gdf, path_intrs_df])
    
intersections_gdf = intersections_gdf.rename(columns = {0: 'geometry'})
intersections_gdf['intersection_n'] = intersections_gdf.apply(lambda row: '.'.join(sorted([row['path_n2'], row['path_n']])), axis = 1)
intersections_gdf = intersections_gdf.groupby('intersection_n').first()
intersections_gdf = intersections_gdf.reset_index()
intersections_gdf = gpd.GeoDataFrame(intersections_gdf, geometry = 'geometry')


phys_nwk = nx.Graph()
comm_nwk = nx.Graph()
for i, path in path_gdf.iterrows():
    path_n = path['path_n']
    path_x, path_y = path['geometry'].xy
    mins = np.argmin(path_x)
    path_strt_name = 'p(' + path_n + '.1)'
    path_strt_x = path_x[mins]
    path_strt_y = path_y[mins]
    path_end_name = 'p(' + path_n + '.2)'
    path_end_x = path_x[1 - mins]
    path_end_y = path_y[1 - mins]

    phys_nwk.add_node(path_strt_name, pos = (path_strt_x, path_strt_y), color = 'black', type = 'path')
    phys_nwk.add_node(path_end_name, pos = (path_end_x, path_end_y), color = 'black', type = 'path')
    
    path_intrs = intersections_gdf.loc[(intersections_gdf['path_n'] == path_n) | (intersections_gdf['path_n2'] == path_n)]
    path_intrs = path_intrs.iloc[path_intrs.geometry.x.argsort().values]
    
    count = 1
    prev_point_name = path_strt_name
    
    for j, intr in path_intrs.iterrows():
        intr_n = intr['intersection_n']
        intr_x = intr['geometry'].x
        intr_y = intr['geometry'].y
        intr_name = 'i(' + intr_n + ')'
        
        phys_nwk.add_node(intr_name, pos = (intr_x, intr_y), color = 'gray', type = 'intersection')
        phys_nwk.add_edge(prev_point_name, intr_name, color = 'lightgray')
        
        prev_point_name = intr_name
        
        if count == path_intrs.shape[0]:
            phys_nwk.add_edge(intr_name, path_end_name, color = 'lightgray')
        count += 1
        
    if path_intrs.shape[0] == 0:
        phys_nwk.add_edge(path_strt_name, path_end_name, colour = 'lightgray')


for robot in robots:
    robot.update()
    phys_nwk.add_node(robot.name, pos = (robot.x, robot.y), color = robot.col, type = robot.state)
    comm_nwk.add_node(robot.name, pos = (robot.x, robot.y), color = robot.col, type = robot.state)
    

coverage_probs = []
N = Sinr.calc_noise_power(robots[0].B, T)
for tx_tgt in filter(lambda robot: robot.state == 'Tx', robots):
    for rx_tgt in filter(lambda robot: robot.state == 'Rx', robots):
        count = 0
        for i in range(n_sims):
            if tx_tgt.path_n == rx_tgt.path_n:
                tgt_coeff = 2
            else:
                tgt_coeff = 3
            d_tx_tgt = np.sqrt((tx_tgt.x - rx_tgt.x) ** 2 + (tx_tgt.y - rx_tgt.y) ** 2)
            L_tx_tgt = Sinr.calc_path_loss(tx_tgt.f, d_tx_tgt, tgt_coeff)
            F_tx_tgt = Sinr.gen_fading_var('F', 0, 1)
            P_rx_tgt = Sinr.calc_rx_power(F_tx_tgt, tx_tgt.P_t, tx_tgt.G, rx_tgt.G, L_tx_tgt)  
            
            P_rx_intf = []
            for tx_intf in filter(lambda robot: robot.state == 'Tx' and robot.name != tx_tgt.name, robots):
                if tx_intf.path_n == rx_tgt.path_n:
                    intf_coeff = 2
                else:
                    intf_coeff = 3
                d_tx_intf = np.sqrt((tx_intf.x - rx_tgt.x) ** 2 + (tx_intf.y - rx_tgt.y) ** 2)
                L_tx_intf = Sinr.calc_path_loss(tx_intf.f, d_tx_intf, intf_coeff)
                F_tx_intf = Sinr.gen_fading_var('F', 0, 1) 
                P_rx_intf.append(Sinr.calc_rx_power(F_tx_intf, tx_intf.P_t, tx_intf.G, rx_tgt.G, L_tx_intf))
            
            sinr = Sinr.calc_sinr(P_rx_tgt, P_rx_intf, N)
            if sinr > sinr_threshold:
                count += 1
        coverage_prob = count / n_sims
        if coverage_prob > 0.1:
            coverage_probs.append(count / n_sims)
            print(tx_tgt.name, rx_tgt.name, count / n_sims)
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
phys_ax.axis('equal')


comm_ax = fig.add_subplot(122)
comm_ax.plot(x_0 + x_c, y_0 + y_c, color = 'black')
comm_node_pos = nx.get_node_attributes(comm_nwk, 'pos')
comm_node_cols = nx.get_node_attributes(comm_nwk, 'color').values()
comm_edge_cols = nx.get_edge_attributes(comm_nwk, 'color').values()
nx.draw(comm_nwk, pos = comm_node_pos, with_labels = False, ax = comm_ax, node_color = comm_node_cols, node_size = 20, edge_color = comm_edge_cols, width = 2, arrows = True, arrowstyle='->')
comm_ax.axis('equal')
plt.show()