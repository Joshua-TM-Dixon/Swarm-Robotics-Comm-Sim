import numpy as np
import plotly.graph_objects as go


class Robot:
    def __init__(self, path_n, robot_n, B, f, P_t, G, x, y):
        self.path_n = path_n
        self.robot_n = robot_n
        self.name = 'n(' + str(path_n) + str(robot_n) + ')'
        self.B = B
        self.f = f
        self.P_t = P_t
        self.G = G
        self.active = 0
        self.state = 'n'
        self.col = 'black'
        self.x = x
        self.y = y

    
    def Get_Status(self):
        return {
            'Robot name' : self.name,
            'Bandwidth' : self.B,
            'Frequency' : self.f,
            'Transmit power' : self.P_t,
            'Antenna gain' : self.G,
            'Active' : self.active,
            'State' : self.state,
            'x' : self.x,
            'y' : self.y
        }

       
    def Update(self):
        state = np.random.choice([0,1])
        if state == 0:
            self.state = 'Tx'
            self.col = 'red'
        else:
            self.state = 'Rx'
            self.col = 'blue'
        self.name = str(self.state) + '(' + str(self.path_n) + '.' + str(self.robot_n) + ')'
        