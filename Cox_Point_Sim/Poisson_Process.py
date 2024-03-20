import numpy as np

# Generate circle points
def gen_circle(r, x_0, y_0):
    phi = np.linspace(0, 2 * np.pi, 200)
    x = x_0 + r * np.cos(phi)
    y = y_0 + r * np.sin(phi)
    return x, y

# Calculate Poisson point parameters
def calc_point_par(n, r):
    d = r * np.sqrt(np.random.uniform(0, 1, n))
    theta = 2 * np.pi * np.random.uniform(0, 1, n)
    return d, theta

# Calculate Poisson point positions
def calc_point_pos(p, q, theta, x_0, y_0, u):
    x = x_0 + p * np.cos(theta) + u * q * np.sin(theta)
    y = y_0 + p * np.sin(theta) - u * q * np.cos(theta)
    return x, y

# Calculate Poisson line parameters
def calc_line_par(n, r):
    p = r * np.random.uniform(0, 1, n)
    q = np.sqrt((r ** 2) - (p ** 2))
    theta = 2 * np.pi * np.random.uniform(0, 1, n)
    return p, q, theta

# Calculate Poisson line positions
def calc_line_pos(p, q, theta, x_0, y_0):
    x_1 = x_0 + p * np.cos(theta) + q *np.sin(theta)
    y_1 = y_0 + p * np.sin(theta) - q *np.cos(theta)
    x_2 = x_0 + p * np.cos(theta) - q *np.sin(theta)
    y_2 = y_0 + p * np.sin(theta) + q *np.cos(theta)
    return x_1, y_1, x_2, y_2

# Perform Poisson Point 
def gen_poisson_points(lambda_0, r, x_0, y_0):
    n = np.random.poisson((np.pi * r ** 2) * lambda_0)
    d, theta = calc_point_par(n, r)
    x, y = calc_point_pos(d, 0, theta, x_0, y_0, 0)
    return x, y

def gen_poisson_lines(lambda_0, r, x_0, y_0):
    n = np.random.poisson((2 * np.pi * r) * lambda_0)
    p, q, theta = calc_line_par(n, r)
    x_1, y_1, x_2, y_2 = calc_line_pos(p, q, theta, x_0, y_0)
    return x_1, y_1, x_2, y_2
    