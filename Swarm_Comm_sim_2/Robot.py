import numpy as np
import plotly.graph_objects as go


class Robot:
    def __init__(self, robot_n, B, f, P_t, G):
        self.path_n = [0]
        self.robot_n = robot_n
        self.name = 'R' + str(robot_n)
        self.B = B
        self.f = f
        self.P_t = P_t
        self.G = G
        self.active = 0
        self.state = 'n'
        self.col = 'black'
        self.x = 0
        self.y = 0

    
    def get_status(self):
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


    def update(self, path_n, x, y):
        state = np.random.choice([0,1])
        if state == 0:
            self.state = 'Tx'
            self.col = 'red'
        else:
            self.state = 'Rx'
            self.col = 'blue'
        self.x = x
        self.y = y
        self.path_n = path_n
        