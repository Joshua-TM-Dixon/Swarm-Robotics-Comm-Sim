import numpy as np
from shapely.geometry import LineString, Point

class Cox_Point:
    def __init__(self, r, centre_pos, lambda_0, mu_0):
        self.r = r
        self.centre_pos = centre_pos
        self.lambda_0 = lambda_0
        self.mu_0 = mu_0


    def gen_line_par(self):
        p = self.r * np.random.uniform(0, 1)
        q = np.sqrt((self.r ** 2) - (p ** 2))
        theta = 2 * np.pi * np.random.uniform(0, 1)
        return p, q, theta
  
  
    def calc_line_pos(self, p, q, theta):
        x_1 = self.centre_pos.x + p * np.cos(theta) + q *np.sin(theta)
        y_1 = self.centre_pos.y + p * np.sin(theta) - q *np.cos(theta)
        x_2 = self.centre_pos.x + p * np.cos(theta) - q *np.sin(theta)
        y_2 = self.centre_pos.y + p * np.sin(theta) + q *np.cos(theta)
        points = sorted([(x_1, y_1), (x_2, y_2)], key = lambda point: point[0])
        return LineString(points)


    def calc_point_pos(self, p, q, theta):
            u = np.random.uniform(-1, 1)
            x = self.centre_pos.x + p * np.cos(theta) + u * q * np.sin(theta)
            y = self.centre_pos.y + p * np.sin(theta) - u * q * np.cos(theta)
            return Point(x, y)


    def run_process(self):
        lines = []
        points = []
        n_itterations = 0
        n_lines = np.random.poisson(2 * np.pi * self.r * self.lambda_0)
        for i in range(n_lines):
            p, q, theta = self.gen_line_par()
            line = self.calc_line_pos(p, q, theta)
            lines.append(line)
            
            line_points = []
            n_points = np.random.poisson(2 * q * self.mu_0)
            for j in range(n_points):
                point = self.calc_point_pos(p, q, theta)
                line_points.append(point)
            
            line_points.sort(key = lambda point: point.x)
            points.append(line_points)
        n_itterations += 1
                
        return lines, points