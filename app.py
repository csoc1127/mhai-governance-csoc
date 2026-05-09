"""
app.py

MH-AI Governance Dashboard
Ethics of Care Alignment Index for US State MH-AI Legislation

Data: Schumate et al. (2025) JMIR Mental Health, 12, e80739
Framework: Tavory (2024) JMIR Mental Health, 11, e58493
Built by: Ciara Staveley-O'Carroll, MSCAPP, University of Chicago, May 2026

"""

import dash
from dash import html, dcc, Input, Output
from mhai.fetch import fetch_bills
from mhai.index import compute_state_index
from mhai.figures import make_choropleth

# DATA
df_bills = fetch_bills()
df_state = compute_state_index(df_bills)

# APP
app = dash.Dash(__name__, title="MH-AI Governance Dashboard")
server = app.server

# LAYOUT
app.layout = html.Div([
    html.H1("MH-AI Governance Dashboard", style={"textAlign": "center"}),
    html.P("Ethics of Care Alignment Index - U.S. State Legislation 2022-2025"),
    dcc.Graph(id="choropleth", figure=make_choropleth(df_state), style={"height": "500px"}),
])


# RUN
if __name__ == "__main__":
    app.run(debug=True, port=8050)