import numpy as np

def Gen_Circle(r, x_0, y_0):
    phi = np.linspace(0, 2 * np.pi, 200)
    x = x_0 + r * np.cos(phi)
    y = y_0 + r * np.sin(phi)
    return x, y

def Calc_Point_Par(n, r):
    d = r * np.sqrt(np.random.uniform(0, 1, n))
    theta = 2 * np.pi * np.random.uniform(0, 1, n)
    return d, theta

def Calc_Point_Pos(p, q, theta, x_0, y_0, u):
    x = x_0 + p * np.cos(theta) + u * q * np.sin(theta)
    y = y_0 + p * np.sin(theta) - u * q * np.cos(theta)
    return x, y

def Calc_Line_Par(n, r):
    p = r * np.random.uniform(0, 1, n)
    q = np.sqrt((r ** 2) - (p ** 2))
    theta = 2 * np.pi * np.random.uniform(0, 1, n)
    return p, q, theta

def Calc_Line_Pos(p, q, theta, x_0, y_0):
    x_1 = x_0 + p * np.cos(theta) + q *np.sin(theta)
    y_1 = y_0 + p * np.sin(theta) - q *np.cos(theta)
    x_2 = x_0 + p * np.cos(theta) - q *np.sin(theta)
    y_2 = y_0 + p * np.sin(theta) + q *np.cos(theta)
    return x_1, y_1, x_2, y_2

def Poisson_Point(lambda_0, r, x_0, y_0):
    n = np.random.poisson((np.pi * r ** 2) * lambda_0)
    d, theta = Calc_Point_Par(n, r)
    x, y = Calc_Point_Pos(d, 0, theta, x_0, y_0, 0)
    return x, y

def Poisson_Line(lambda_0, r, x_0, y_0):
    n = np.random.poisson((2 * np.pi * r) * lambda_0)
    p, q, theta = Calc_Line_Par(n, r)
    x_1, y_1, x_2, y_2 = Calc_Line_Pos(p, q, theta, x_0, y_0)
    return x_1, y_1, x_2, y_2
    