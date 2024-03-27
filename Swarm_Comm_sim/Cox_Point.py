# Libraries
import numpy as np
from shapely.geometry import LineString
import Robot as rb

# Functions
# Generates 200 points evenly distributed on a circle
def gen_circle(r, x_0, y_0):
    theta = np.linspace(0, 2 * np.pi, 200)
    x = x_0 + r * np.cos(theta)
    y = y_0 + r * np.sin(theta)
    return x, y


# Generates Poisson line parameters
def gen_line_par(r):
    p = r * np.random.uniform(0, 1)
    q = np.sqrt((r ** 2) - (p ** 2))
    theta = 2 * np.pi * np.random.uniform(0, 1)
    return p, q, theta
  
 
# Calculates the start and end points for the Poisson line process 
def calc_line_pos(x_0, y_0, p, q, theta):
    x_1 = x_0 + p * np.cos(theta) + q *np.sin(theta)
    y_1 = y_0 + p * np.sin(theta) - q *np.cos(theta)
    x_2 = x_0 + p * np.cos(theta) - q *np.sin(theta)
    y_2 = y_0 + p * np.sin(theta) + q *np.cos(theta)
    return LineString([(x_1, y_1), (x_2, y_2)])


# Calculates the positions for the Poisson point process
def calc_point_pos(x_0, y_0, p, q, theta):
        u = np.random.uniform(-1, 1)
        x = x_0 + p * np.cos(theta) + u * q * np.sin(theta)
        y = y_0 + p * np.sin(theta) - u * q * np.cos(theta)
        return x, y


# Performs Cox point process - generates random lines and popl
def cox_point_process(r, x_0, y_0, lambda_0, mu_0):
    lines = []
    points = []
    n_lines = np.random.poisson(2 * np.pi * r * lambda_0)
    for i in range(n_lines):
        p, q, theta = gen_line_par(r)
        line = calc_line_pos(x_0, y_0, p, q, theta)
        lines.append(line)
        
        n_nodes = np.random.poisson(2 * q * mu_0)
        for j in range(n_nodes):
            point_x, point_y = calc_point_pos(x_0, y_0, p, q, theta)
            robot = rb.Robot(i, j, 10 ** 6, 2.4835 * 10 ** 9, 10 ** (-5), 10 ** (-1), point_x, point_y)
            points.append(robot)
            
    return lines, points