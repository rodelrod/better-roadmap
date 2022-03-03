import dash_bootstrap_components as dbc
from dash import dcc
from plotly.graph_objects import Figure


def select_chart_height():
    return dbc.Row(
        [
            dbc.Label("Chart height", html_for="select-chart-height", width=2),
            dbc.Col(
                dbc.Select(
                    id="select-chart-height",
                    options=[
                        {"label": "S", "value": 500},
                        {"label": "M", "value": 720},
                        {"label": "L", "value": 1100},
                        {"label": "XL", "value": 1500},
                    ],
                    value=720,
                ),
                width=2,
            ),
        ]
    )


def tab_chart(fig: Figure) -> dbc.Tab:
    return dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id="roadmap-graph", figure=fig),
                    select_chart_height(),
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="📅 Roadmap",
    )
