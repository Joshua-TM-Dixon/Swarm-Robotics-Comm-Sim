import numpy as np
import plotly.graph_objects as go

class Circle:
    def __init__(self, name, r, x_0, y_0):
        self.name = name
        self.r = r
        self.x_0 = x_0
        self.y_0 = y_0
        self.x, self.y = self.Gen()
        
        
    def __str__(self):
        return f'{self.name}[{self.r}, ({self.x_0}, {self.y_0})]'
        
        
    def Gen(self):
        theta = np.linspace(0, 2 * np.pi, 200)
        x = self.x_0 + self.r * np.cos(theta)
        y = self.y_0 + self.r * np.sin(theta)
        return x, y
    
    
    def Draw(self):
        return go.Scatter(
            x = self.x,
            y = self.y,
            mode = 'lines',
            line = dict(color = 'black'),
            name = self.name)