import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
from dash.dependencies import Input, Output

import numpy as np
from numpy import pi, cos

app = dash.Dash()

app.layout = html.Div(children=[
    html.Label('Enter w1'),
    dcc.Input(value=0, type='number', id='input1'),
    html.Label('Enter w2'),
    dcc.Input(value=0, type='number', id='input2'),
    html.Label('Enter d / pi'),
    dcc.Input(value=0, type='number', id='input3', step=0.05),
    html.Label('Enter x0'),
    dcc.Input(value=1, type='number', id='input4'),
    html.Label('Enter y0'),
    dcc.Input(value=1, type='number', id='input5'),
    dcc.Graph(
        id='graph',
        figure={
            'data': [go.Scatter(x=[], y=[], mode='lines')],
            'layout': {
                "title": "My Dash Graph",
                "height": 850,
                "width": 850
            }
        }
    )
])


@app.callback(
    Output("graph", "figure"),
    [Input("input1", "value"),
     Input("input2", "value"),
     Input("input3", "value"),
     Input("input4", "value"),
     Input("input5", "value")
     ],
)
def update_graph(w1, w2, d, x0, y0):
    try:
        w1 = float(w1)
        w2 = float(w2)
        d = float(d)
        x0 = float(x0)
        y0 = float(y0)
    except ValueError:
        return go.Figure()

    graph = []
    graph_obj = go.Scatter(
        line=dict(color="#00CED1", width=6),
        x=[x0 * cos(w1 * t) for t in np.arange(0., 2 * pi, 0.01)],
        y=[y0 * cos(w2 * t + d * pi) for t in np.arange(0., 2 * pi, 0.01)])
    graph.append(graph_obj)

    figure = go.Figure(data=graph)
    return figure


if __name__ == '__main__':
    app.run_server()
