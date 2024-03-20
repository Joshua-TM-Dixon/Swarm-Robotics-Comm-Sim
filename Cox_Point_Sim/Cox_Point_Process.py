import numpy as np
import plotly.graph_objects as go
import Poisson_Process as pp

# Global variables
r_circ = 10  # Circle radius
x_0_circ = 0 # Cirlce centre x coordinate
y_0_circ = 0  # Cirlce centre y coordinate
lambda_0 = 0.4  # Poisson line distribution parameter
mu_0 = 0.2  # Poisson point distribution parameter
x_points = []  # Poisson point x coordinates
y_points = []  # Poisson point y coordinates

# Simulate Cox Point process
x_circ, y_circ = pp.Gen_Circle(r_circ, x_0_circ, y_0_circ)
n_lines = np.random.poisson(2 * np.pi * r_circ * lambda_0)
p, q, theta = pp.Calc_Line_Par(n_lines, r_circ)
x_ln_1, y_ln_1, x_ln_2, y_ln_2 = pp.Calc_Line_Pos(p, q, theta, x_0_circ, y_0_circ)
for i in range(n_lines):
    n_points = np.random.poisson(2 * q[i] * mu_0)
    for j in range(n_points):
        u = np.random.uniform(-1, 1)
        x_points, y_points = pp.Calc_Point_Pos(p[i], q[i], theta[i], x_0_circ, y_0_circ, u)
        x_points.append(x_points)
        y_points.append(y_points)
    
# Plot Cox Point Graph
fig = go.Figure()

fig.add_trace(
    
    # Plot circle
    go.Scatter(
        x = x_circ,
        y = y_circ,
        mode = 'lines',
        line = dict(color = 'black'),
        name = 'Area'))

# Plot poisson lines
for line in range(n_lines):
        fig.add_trace(
            go.Scatter(
                x = [x_ln_1[line], x_ln_2[line]],
                y = [y_ln_1[line], y_ln_2[line]],
                mode = 'lines',
                line = dict(color = 'red', dash = 'dash'),
                name = f'Link {i}'))

# Plot poisson points        
fig.add_trace(
    go.Scatter(
        x = x_points,
        y = y_points,
        mode = 'markers',
        marker = dict(color = 'blue', symbol = 'circle'),
        name = 'Nodes'))

# modify graph appearance
fig.update_layout(
    title = dict(
        text = "Poisson-Line-Based Cox-Point Process",
        font = dict(family="Arial", size=26, color="black")),
    xaxis = dict(
        title = dict(
            text = "x (m)",
            font = dict(family="Arial", size=22, color="black")),
        tickfont = dict(family="Arial", size=18, color="black")),
    yaxis = dict(
        title = dict(
            text = "y (m)",
            font = dict(family="Arial", size=22, color="black")),
        tickfont = dict(family="Arial", size=18, color="black")),
    showlegend = False,
    autosize = False,
    width = 750,
    height = 750)

fig.show()