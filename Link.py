import numpy as np
import plotly.graph_objects as go
import Sinr

class Link:
    def __init__(self, path_n, link_n, tx, rx, a):
        self.name = f'{path_n}.{link_n}'
        self.sinr = 7
        self.tx = tx
        self.rx = rx
        self.v = 3 * 10 ** 8
        self.d = self.Calc_d(tx.x, tx.y, rx.x, rx.y)
        self.F = Sinr.Gen_F('F', 0, 1)
        self.L = Sinr.Calc_L(tx.f, self.d, a)
        self.P_r = Sinr.Calc_P_r(self.F, tx.P_t, tx.G, rx.G, self.L)
        
        
    def __str__(self):
        pass
    
    
    def Calc_d(self, x_1, y_1, x_2, y_2):
        return np.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)
        
    
    def Draw(self):
        return go.Scatter(
            x = [self.tx.x, self.rx.x],
            y = [self.tx.y, self.rx.y],
            mode = 'lines',
            line = dict(color = 'green', dash = 'dot'),
            name = f'Link {self.name} = {self.sinr}',
            legendgroup = 'Links')