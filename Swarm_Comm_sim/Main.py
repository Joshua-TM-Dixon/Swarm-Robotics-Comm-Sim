import numpy as np
import networkx as nx
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import Cox_Point as cp
import SINR_Functions as Sinr


r = 2
T = 300
x_0 = 0
y_0 = 0
thr = 0.1
lambda_0 = 2
mu_0 = 1.5


x_c, y_c = cp.Gen_Circle(r, x_0, y_0)
paths, robots = cp.Cox_Point_Process(r, x_0, y_0, lambda_0, mu_0)   

   
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
    robot.Update()
    phys_nwk.add_node(robot.name, pos = (robot.x, robot.y), color = robot.col, type = robot.state)
    comm_nwk.add_node(robot.name, pos = (robot.x, robot.y), color = robot.col, type = robot.state)


links = []
for i, path in path_gdf.iterrows():
    
    for tx in filter(lambda robot: robot.state == 'Tx' and robot.path_n == i, robots):
            d_min = float('inf')
            opt_rx = None
            
            for rx in filter(lambda robot: robot.state == 'Rx' and robot.path_n == i, robots):
                d = np.sqrt((tx.x - rx.x) ** 2 + (tx.y - rx.y) ** 2)
                if d > 0 and d < d_min:
                    d_min = d
                    opt_rx = rx
                    
            if opt_rx is not None:       
                tx.active = 1
                opt_rx.active = 1
                link = [tx, opt_rx]
                links.append(link)
                comm_nwk.add_edge(link[0].name, link[1].name, color = 'green', type = 'link')
    

sinr_vals = []
N = Sinr.Calc_N(robots[0].B, T)
for link in links:
    link_F = Sinr.Gen_F('F', 0, 1)
    link_d = np.sqrt((link[0].x - link[1].x) ** 2 + (link[0].y - link[1].y) ** 2)
    link_L = Sinr.Calc_L(link[0].f, link_d, 2)
    link_P_r = Sinr.Calc_P_r(link_F, link[0].P_t, link[0].G, link[1].G, link_L)  
    
    interference_P_r = []
    for tx in filter(lambda robot: robot.state == 'Tx' and robot.active == 1 and robot.name != link[0].name, robots):
        tx_F = Sinr.Gen_F('F', 0, 1) 
        tx_d = np.sqrt((tx.x - link[1].x) ** 2 + (tx.y - link[1].y) ** 2)
        tx_L = Sinr.Calc_L(tx.f, tx_d, 2)
        tx_P_r = Sinr.Calc_P_r(tx_F, tx.P_t, tx.G, link[1].G, tx_L)
        interference_P_r.append(tx_P_r)
    
    link_sinr = Sinr.Calc_SINR(link_P_r, interference_P_r, N)
    sinr_vals.append([link[0].name, link[1].name, link_sinr])


for sinr_val in sinr_vals:
    print(sinr_val,'\n')          

           
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
nx.draw(comm_nwk, pos = comm_node_pos, with_labels = True, ax = comm_ax, node_color = comm_node_cols, node_size = 20, edge_color = comm_edge_cols, width = 2, arrows = True, arrowstyle='->')
comm_ax.axis('equal')
plt.show()