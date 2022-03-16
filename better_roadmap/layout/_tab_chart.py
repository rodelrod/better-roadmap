import dash_bootstrap_components as dbc
from dash import dcc, html
from plotly.graph_objects import Figure


def search_features():
    return [
        dbc.Col(
            [
                dbc.Input(
                    id="search-features-input",
                    placeholder="🔍  Search features…",
                    type="text",
                    debounce=True,
                ),
                html.Div(id="search-dummy-output", hidden=True),
            ],
            width=4,
        )
    ]


def select_chart_height():
    return [
        dbc.Col(
            dbc.Label("Chart height", html_for="select-chart-height"),
            width=2,
        ),
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


def tab_chart(fig: Figure) -> dbc.Tab:
    return dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(search_features()),
                    dcc.Graph(id="roadmap-graph", figure=fig),
                    dbc.Row(select_chart_height()),
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="📅 Roadmap",
    )
