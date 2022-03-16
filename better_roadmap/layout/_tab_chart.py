import dash_bootstrap_components as dbc
from dash import dcc, html
from plotly.graph_objects import Figure


def search_features():
    return [
        dbc.Label("🔍", html_for="search-features-input", width="auto"),
        dbc.Col(
            [
                dbc.Input(
                    id="search-features-input",
                    placeholder="Search features…",
                    type="text",
                    debounce=True,
                ),
                html.Div(id="search-dummy-output", hidden=True),
            ],
            width=4,
        ),
    ]


def select_chart_height():
    return [
        dbc.Label("Chart height:", html_for="select-chart-height", width="auto"),
        dbc.Col(
            dbc.Select(
                id="select-chart-height",
                options=[
                    {"label": "S", "value": 500},
                    {"label": "M", "value": 720},
                    {"label": "L", "value": 1100},
                    {"label": "XL", "value": 1500},
                ],
                value=1100,
            ),
            width=2,
        ),
    ]


def tab_chart(fig: Figure) -> dbc.Tab:
    return dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(search_features() + select_chart_height()),
                    dcc.Graph(id="roadmap-graph", figure=fig),
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="📅 Roadmap",
    )
