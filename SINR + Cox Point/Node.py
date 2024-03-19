import numpy as np
import plotly.graph_objects as go

class Node:
    def __init__(self, node_n, path, B, f, P_t, G, thr, x_0, y_0):
        self.name = f'{path.name}.{node_n}'
        self.B = B
        self.f = f
        self.P_t = P_t
        self.G = G
        self.thr = thr
        self.active = 0
        self.state = np.random.choice([0,1])
        self.u = np.random.uniform(-1, 1)
        self.x, self.y = self.Calc_Point_Pos(path.p, path.q, path.theta, x_0, y_0)
        
        
    def __str__(self):
        return f'Node{self.link_n}.{self.node_n}({self.state}, {self.x}, {self.y})'
            
            
    def Calc_Point_Pos(self, p, q, theta, x_0, y_0):
        x = x_0 + p * np.cos(theta) + self.u * q * np.sin(theta)
        y = y_0 + p * np.sin(theta) - self.u * q * np.cos(theta)
        return x, y
    
    
    def Draw(self):
        if self.active == 0 and self.state == 1:
            colour = 'cyan'
            group = 'rx'
        elif self.active == 1 and self.state == 0:
            colour = 'red'
            group = 'tx'
        elif self.active == 1 and self.state == 1:
            colour = 'blue'
            group = 'rx'
        else:
            colour = 'orange'
            group = 'tx'
            
        return go.Scatter(
            x = [self.x],
            y = [self.y],
            mode = 'markers',
            marker = dict(color = colour, symbol = 'circle'),
            name = f'{group} {self.name}',
            legendgroup = group)
    