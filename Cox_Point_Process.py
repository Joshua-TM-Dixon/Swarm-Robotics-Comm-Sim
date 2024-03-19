import numpy as np
import plotly.graph_objects as go
import Poisson_Process as pp

r = 10
x_0 = 0
y_0 = 0
lambda_0 = 0.4
mu_0 = 0.2
n_links = np.random.poisson(2 * np.pi * r * lambda_0)


p, q, theta = pp.Calc_Line_Par(n_links, r)
x_l1, y_l1, x_l2, y_l2 = pp.Calc_Line_Pos(p, q, theta, x_0, y_0)

x_p = []
y_p = []
for i in range(n_links):
    n_nodes = np.random.poisson(2 * q[i] * mu_0)
    for j in range(n_nodes):
        u = np.random.uniform(-1, 1)
        x, y = pp.Calc_Point_Pos(p[i], q[i], theta[i], x_0, y_0, u)
        x_p.append(x)
        y_p.append(y)
    

xc, yc = pp.Gen_Circle(r, x_0, y_0)


fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x = xc,
        y = yc,
        mode = 'lines',
        line = dict(color = 'black'),
        name = 'Area'))

for i in range(n_links):
        fig.add_trace(
            go.Scatter(
                x = [x_l1[i], x_l2[i]],
                y = [y_l1[i], y_l2[i]],
                mode = 'lines',
                line = dict(color = 'red', dash = 'dash'),
                name = f'Link {i}'))
        
fig.add_trace(
    go.Scatter(
        x = x_p,
        y = y_p,
        mode = 'markers',
        marker = dict(color = 'blue', symbol = 'circle'),
        name = 'Nodes'))

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