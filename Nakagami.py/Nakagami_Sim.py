import numpy as np
import scipy.stats as stats
import plotly.subplots as subplots
import plotly.graph_objects as go

# Define parameters
m_values = [0.5, 1, 2, 4]
omega_values = [1/3, 0.5, 2/3, 3/4, 1]

# Create subplots
fig = subplots.make_subplots(rows=len(omega_values), cols=1,
                              subplot_titles=[f'Nakagami Probability Density Function (omega={omega})' for omega in omega_values],
                              shared_xaxes=True,
                              vertical_spacing=0.05)

for i, omega in enumerate(omega_values, start=1):
    for m in m_values:
        # Create Nakagami PDF for current m and omega
        x = np.linspace(0, 5, 500)
        pdf_values = stats.nakagami.pdf(x, m, scale=omega)

        # Add trace to subplot
        fig.add_trace(go.Scatter(x=x, y=pdf_values, mode='lines', name=f'm={m}'), row=i, col=1)

    
# Update layout
fig.update_layout(height=300*len(omega_values), width=1000, template="plotly_white")

# Show plot
fig.show()
