import numpy as np
import networkx as nx
import geopandas as gpd
import pandas as pd

def create_path_gdf(paths):   
    path_gdf = gpd.GeoDataFrame(geometry = paths) 
    path_gdf['path_n'] = path_gdf.index
    path_gdf['start_name'] = 'p ' + path_gdf['path_n'].astype(str) + '.1'
    path_gdf['end_name'] = 'p ' + path_gdf['path_n'].astype(str) + '.2'
            
    return path_gdf


def create_node_gdf(nodes):
    node_data = []
    for i, path_nodes in enumerate(nodes):
        for j, node in enumerate(path_nodes): 
           node_data.append({'geometry': node, 'path_n': i, 'name': 'n ' + str(i) + '.' + str(j)})      
    node_gdf = gpd.GeoDataFrame(node_data, geometry = 'geometry')
    
    return node_gdf


def create_intersection_gdf(path_gdf):
    intersection_df = pd.DataFrame()
    for i, path in path_gdf.iterrows():
        path_intersections = path_gdf.intersection(path['geometry'])
        path_intersection_points = path_intersections[path_intersections.geom_type == 'Point']
        path_intersection_df = pd.DataFrame({'geometry': path_intersection_points})
        path_intersection_df['path_n2'] = path['path_n']
        path_intersection_df = path_intersection_df.join(path_gdf['path_n'])
        intersection_df = pd.concat([intersection_df, path_intersection_df])
        
    intersection_df['name'] = intersection_df.apply(lambda intersection: 'i ' + '.'.join(sorted([str(intersection['path_n2']), str(intersection['path_n'])])), axis = 1)
    intersection_df = intersection_df.groupby('name').first()
    intersection_df = intersection_df.reset_index()
    intersection_gdf = gpd.GeoDataFrame(intersection_df, geometry = 'geometry')        
    
    return intersection_gdf


def check_on_path(start, end, point):
    cross_product = (end[0] - start[0]) * (point[1] - start[1]) - (point[0] - start[0]) * (end[1] - start[1])
    dot_product = (end[0] - start[0]) * (point[0] - start[0]) + (end[1] - start[1]) * (point[1] - start[1])
    sqr_length = (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
    
    if abs(cross_product) > 0.01 or dot_product < 0 or dot_product > sqr_length:
        return False
    else:
        return True


def check_for_nodes(graph, path_n, node_gdf, prev_name):
    for i, node in node_gdf.iterrows():
        if node['path_n'] == path_n and graph.has_node(node['name']) == False:
            graph.add_node(node['name'], pos = [node['geometry'].x, node['geometry'].y], color = 'dimgray', type = 'node')
            graph.add_edge(node['name'], prev_name, color = 'lightgray')
            prev_name = node['name']
    
    return prev_name


def populate_graph(graph, path_gdf, intersection_gdf, node_gdf):
    for i, path in path_gdf.iterrows():
        path_x, path_y = path['geometry'].xy
        mins = np.argmin(path_x)
        path_strt_x = path_x[mins]
        path_strt_y = path_y[mins]
        path_end_x = path_x[1 - mins]
        path_end_y = path_y[1 - mins]
        path_intrs = intersection_gdf.loc[(intersection_gdf['path_n'] == path['path_n']) | (intersection_gdf['path_n2'] == path['path_n'])]
        path_intrs = path_intrs.iloc[path_intrs.geometry.x.argsort().values]
        graph.add_node(path['start_name'], pos = (path_strt_x, path_strt_y), color = 'black', type = 'path')
        graph.add_node(path['end_name'], pos = (path_end_x, path_end_y), color = 'black', type = 'path')
        
        prev_node_name = path['start_name']
        if path_intrs.shape[0] == 0:
            prev_node_name = check_for_nodes(graph, path['path_n'], node_gdf, prev_node_name)
            graph.add_edge(prev_node_name, path['end_name'], colour = 'lightgray')
        else: 
            for j, intr in path_intrs.iterrows():
                graph.add_node(intr['name'], pos = (intr['geometry'].x, intr['geometry'].y), color = 'gray', type = 'intersection')
                prev_node_name = check_for_nodes(graph, path['path_n'], node_gdf, prev_node_name)
                graph.add_edge(prev_node_name, intr['name'], color = 'lightgray')
                prev_node_name = intr['name']
            prev_node_name = check_for_nodes(graph, path['path_n'], node_gdf, prev_node_name)
            graph.add_edge(prev_node_name, path['end_name'], color = 'lightgray')