# Libraries
import numpy as np
from shapely.geometry import LineString, Point
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
    points = sorted([(x_1, y_1), (x_2, y_2)], key = lambda point: point[0])
    return LineString(points)


# Calculates the positions for the Poisson point process
def calc_point_pos(x_0, y_0, p, q, theta):
        u = np.random.uniform(-1, 1)
        x = x_0 + p * np.cos(theta) + u * q * np.sin(theta)
        y = y_0 + p * np.sin(theta) - u * q * np.cos(theta)
        return Point(x, y)


# Performs Cox point process - generates random lines and popl
def cox_point_process(r, x_0, y_0, lambda_0, mu_0, n_points_min):
    lines = []
    points = []
    n_itterations = 0
    while len(points) < n_points_min:
        n_lines = np.random.poisson(2 * np.pi * r * lambda_0)
        for i in range(n_lines):
            p, q, theta = gen_line_par(r)
            line = calc_line_pos(x_0, y_0, p, q, theta)
            lines.append(line)
            
            line_points = []
            n_points = np.random.poisson(2 * q * mu_0)
            for j in range(n_points):
                point = calc_point_pos(x_0, y_0, p, q, theta)
                line_points.append(point)
            
            line_points.sort(key = lambda point: point.x)
            points.append(line_points)
        n_itterations += 1
        if n_itterations == 20:
            print('Error: n_points_min too high for given mu and lambda')
            break
            
    return lines, points