import numpy as np
from shapely.geometry import LineString
import Robot as rb



def Gen_Circle(r, x_0, y_0):
    theta = np.linspace(0, 2 * np.pi, 200)
    x = x_0 + r * np.cos(theta)
    y = y_0 + r * np.sin(theta)
    return x, y



def Gen_Line_Par(r):
    p = r * np.random.uniform(0, 1)
    q = np.sqrt((r ** 2) - (p ** 2))
    theta = 2 * np.pi * np.random.uniform(0, 1)
    return p, q, theta
  
 
    
def Calc_Line_Pos(x_0, y_0, p, q, theta):
    x_1 = x_0 + p * np.cos(theta) + q *np.sin(theta)
    y_1 = y_0 + p * np.sin(theta) - q *np.cos(theta)
    x_2 = x_0 + p * np.cos(theta) - q *np.sin(theta)
    y_2 = y_0 + p * np.sin(theta) + q *np.cos(theta)
    return LineString([(x_1, y_1), (x_2, y_2)])



def Calc_Point_Pos(x_0, y_0, p, q, theta):
        u = np.random.uniform(-1, 1)
        x = x_0 + p * np.cos(theta) + u * q * np.sin(theta)
        y = y_0 + p * np.sin(theta) - u * q * np.cos(theta)
        return x, y



def Cox_Point_Process(r, x_0, y_0, lambda_0, mu_0):
    lines = []
    points = []

    n_lines = np.random.poisson(2 * np.pi * r * lambda_0)
    for i in range(n_lines):
        p, q, theta = Gen_Line_Par(r)
        line = Calc_Line_Pos(x_0, y_0, p, q, theta)
        lines.append(line)
        
        n_nodes = np.random.poisson(2 * q * mu_0)
        for j in range(n_nodes):
            point_x, point_y = Calc_Point_Pos(x_0, y_0, p, q, theta)
            robot = rb.Robot(i, j, 10 ** 6, 2.4835 * 10 ** 9, 10 ** (-5), 10 ** (-1), point_x, point_y)
            points.append(robot)
            
    return lines, points