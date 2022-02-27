import dash_bootstrap_components as dbc
from dash import dcc
from plotly.graph_objects import Figure


def tab_chart(fig: Figure) -> dbc.Tab:
    return dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id="roadmap-graph", figure=fig),
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="📅 Roadmap",
    )
