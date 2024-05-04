import numpy as np
import networkx as nx
import geopandas as gpd
import pandas as pd

class Sim_Environment:
    def __init__(self):
        self.graph = nx.Graph()
        self.path_gdf = None
        self.node_gdf = None
        self.intersection_gdf = None

    def gen_path_gdf(self, paths):   
        self.path_gdf = gpd.GeoDataFrame(geometry = paths) 
        self.path_gdf['path_n'] = self.path_gdf.index
        self.path_gdf['start_name'] = 'p ' + self.path_gdf['path_n'].astype(str) + '.1'
        self.path_gdf['end_name'] = 'p ' + self.path_gdf['path_n'].astype(str) + '.2'

    def gen_node_gdf(self, nodes):
        node_data = []
        for i, path_nodes in enumerate(nodes):
            for j, node in enumerate(path_nodes): 
                node_data.append({'geometry': node, 'path_n': i, 'name': 'n ' + str(i) + '.' + str(j)})      
        self.node_gdf = gpd.GeoDataFrame(node_data, geometry = 'geometry')

    def gen_intersection_gdf(self):
        intersection_df = pd.DataFrame()
        for i, path in self.path_gdf.iterrows():
            path_intersections = self.path_gdf.intersection(path['geometry'])
            path_intersection_points = path_intersections[path_intersections.geom_type == 'Point']
            path_intersection_df = pd.DataFrame({'geometry': path_intersection_points})
            path_intersection_df['path_n2'] = path['path_n']
            path_intersection_df = path_intersection_df.join(self.path_gdf['path_n'])
            intersection_df = pd.concat([intersection_df, path_intersection_df])
            
        intersection_df['name'] = intersection_df.apply(lambda intersection: 'i ' + '.'.join(sorted([str(intersection['path_n2']), str(intersection['path_n'])])), axis = 1)
        intersection_df = intersection_df.groupby('name').first()
        intersection_df = intersection_df.reset_index()
        self.intersection_gdf = gpd.GeoDataFrame(intersection_df, geometry = 'geometry')        

    def insert_nodes(self, path_n, path_col, node_col, prev_node_name):
        for i, node in self.node_gdf.iterrows():
            if node['path_n'] == path_n and self.graph.has_node(node['name']) == False:
                self.graph.add_node(node['name'], pos = [node['geometry'].x, node['geometry'].y], color = node_col, type = 'node', path_n = [node['path_n']])
                d = np.sqrt((self.graph.nodes[node['name']]['pos'][0] - self.graph.nodes[prev_node_name]['pos'][0])**2 + (self.graph.nodes[node['name']]['pos'][1] - self.graph.nodes[prev_node_name]['pos'][1])**2)
                self.graph.add_edge(node['name'], prev_node_name, color = path_col, weight = d)
                prev_node_name = node['name']
        return prev_node_name

    def populate_graph(self, boarder_col, path_col, intersection_col, node_col):
        for i, path in self.path_gdf.iterrows():
            path_x, path_y = path['geometry'].xy
            mins = np.argmin(path_x)
            path_strt_x = path_x[mins]
            path_strt_y = path_y[mins]
            path_end_x = path_x[1 - mins]
            path_end_y = path_y[1 - mins]
            path_intrs = self.intersection_gdf.loc[(self.intersection_gdf['path_n'] == path['path_n']) | (self.intersection_gdf['path_n2'] == path['path_n'])]
            path_intrs = path_intrs.iloc[path_intrs.geometry.x.argsort().values]
            self.graph.add_node(path['start_name'], pos = (path_strt_x, path_strt_y), color = boarder_col, type = 'path', path_n = [path['path_n']])
            self.graph.add_node(path['end_name'], pos = (path_end_x, path_end_y), color = boarder_col, type = 'path', path_n = [path['path_n']])
            
            prev_node_name = path['start_name']
            if path_intrs.shape[0] == 0:
                prev_node_name = self.insert_nodes(path['path_n'], path_col, node_col, prev_node_name)
                d = np.sqrt((self.graph.nodes[path['end_name']]['pos'][0] - self.graph.nodes[prev_node_name]['pos'][0])**2 + (self.graph.nodes[path['end_name']]['pos'][1] - self.graph.nodes[prev_node_name]['pos'][1])**2)
                self.graph.add_edge(prev_node_name, path['end_name'], colour = path_col, weight = d)
            else: 
                for j, intr in path_intrs.iterrows():
                    self.graph.add_node(intr['name'], pos = (intr['geometry'].x, intr['geometry'].y), color = intersection_col, type = 'intersection', path_n = [intr['path_n2'], intr['path_n']])
                    prev_node_name = self.insert_nodes(path['path_n'], path_col, node_col, prev_node_name)
                    d = np.sqrt((self.graph.nodes[intr['name']]['pos'][0] - self.graph.nodes[prev_node_name]['pos'][0])**2 + (self.graph.nodes[intr['name']]['pos'][1] - self.graph.nodes[prev_node_name]['pos'][1])**2)
                    self.graph.add_edge(prev_node_name, intr['name'], color = path_col, weight = d)
                    prev_node_name = intr['name']
                prev_node_name = self.insert_nodes(path['path_n'], path_col, node_col, prev_node_name)
                d = np.sqrt((self.graph.nodes[path['end_name']]['pos'][0] - self.graph.nodes[prev_node_name]['pos'][0])**2 + (self.graph.nodes[path['end_name']]['pos'][1] - self.graph.nodes[prev_node_name]['pos'][1])**2)
                self.graph.add_edge(prev_node_name, path['end_name'], color = path_col, weight = d)
        