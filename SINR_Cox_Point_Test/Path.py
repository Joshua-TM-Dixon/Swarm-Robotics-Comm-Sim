import numpy as np
import plotly.graph_objects as go

class Path:
    def __init__(self, path_n, r, x_0, y_0):
        self.name = path_n
        self.p, self.q, self.theta = self.Calc_Line_Par(r)
        self.x_1, self.y_1, self.x_2, self.y_2 = self.Calc_Line_Pos(x_0, y_0)
        
        
    def __str__(self):
        return f'{self.path_n}[{self.p}, {self.q}, {self.theta}]'
    
    
    def Calc_Line_Par(self, r):
        p = r * np.random.uniform(0, 1)
        q = np.sqrt((r ** 2) - (p ** 2))
        theta = 2 * np.pi * np.random.uniform(0, 1)
        return p, q, theta
    
    
    def Calc_Line_Pos(self, x_0, y_0):
        x_1 = x_0 + self.p * np.cos(self.theta) + self.q *np.sin(self.theta)
        y_1 = y_0 + self.p * np.sin(self.theta) - self.q *np.cos(self.theta)
        x_2 = x_0 + self.p * np.cos(self.theta) - self.q *np.sin(self.theta)
        y_2 = y_0 + self.p * np.sin(self.theta) + self.q *np.cos(self.theta)
        return x_1, y_1, x_2, y_2


    def Draw(self):
        return go.Scatter(
            x = [self.x_1, self.x_2],
            y = [self.y_1, self.y_2],
            mode = 'lines',
            line = dict(color = 'grey', dash = 'dash'),
            name = f'Path {self.name}',
            legendgroup = 'Paths')
