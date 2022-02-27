import dash_bootstrap_components as dbc
from dash import dcc, html


def layout(fig, features_text: str, parameters_text: str):
    tab_chart = dbc.Tab(
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
    tab_features = dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        children=[
                            dbc.Col(
                                dbc.Textarea(
                                    id="features-textarea",
                                    value=features_text,
                                    rows=30,
                                    persistence=True,
                                    persistence_type="local",
                                ),
                            ),
                            dbc.Col(
                                [
                                    dbc.Row(
                                        dbc.ButtonGroup(
                                            [
                                                dbc.Button(
                                                    html.Span(
                                                        [
                                                            "Update",
                                                            html.I(
                                                                className="bi bi-bar-chart-steps ms-2"
                                                            ),
                                                        ]
                                                    ),
                                                    id="features-update-button",
                                                    n_clicks=0,
                                                    className="btn-lg",
                                                ),
                                                dcc.Download(id="features-download"),
                                                dbc.Button(
                                                    html.Span(
                                                        [
                                                            "Download",
                                                            html.I(
                                                                className="bi bi-download ms-2"
                                                            ),
                                                        ]
                                                    ),
                                                    id="features-download-button",
                                                    n_clicks=0,
                                                    className="btn-lg",
                                                ),
                                            ]
                                        ),
                                    ),
                                    dbc.Row(
                                        className="mt-3",
                                        children=dbc.Col(
                                            dbc.Button(
                                                outline=True,
                                                color="primary",
                                                className="text-center d-grid gap-2 col-8 mx-auto",
                                                children=dcc.Upload(
                                                    id="features-upload",
                                                    children=[
                                                        html.I(
                                                            className="bi bi-cloud-upload me-2",
                                                            style={
                                                                "fontSize": "xx-large"
                                                            },
                                                        ),
                                                        html.Br(),
                                                        "drag & drop or select file",
                                                    ],
                                                ),
                                            ),
                                        ),
                                    ),
                                ]
                            ),
                        ],
                    )
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="🏆 Features",
    )
    tab_parameters = dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Textarea(
                                    id="parameters-textarea",
                                    value=parameters_text,
                                    rows=20,
                                    persistence=True,
                                    persistence_type="local",
                                ),
                            ),
                            dbc.Col(
                                [
                                    dbc.Row(
                                        dbc.ButtonGroup(
                                            [
                                                dbc.Button(
                                                    html.Span(
                                                        [
                                                            "Update",
                                                            html.I(
                                                                className="bi bi-bar-chart-steps ms-2"
                                                            ),
                                                        ]
                                                    ),
                                                    id="parameters-update-button",
                                                    n_clicks=0,
                                                    className="btn-lg",
                                                ),
                                                dcc.Download(id="parameters-download"),
                                                dbc.Button(
                                                    html.Span(
                                                        [
                                                            "Download",
                                                            html.I(
                                                                className="bi bi-download ms-2"
                                                            ),
                                                        ]
                                                    ),
                                                    id="parameters-download-button",
                                                    n_clicks=0,
                                                    className="btn-lg",
                                                ),
                                            ]
                                        ),
                                    ),
                                    dbc.Row(
                                        className="mt-3",
                                        children=dbc.Col(
                                            dbc.Button(
                                                outline=True,
                                                color="primary",
                                                className="text-center d-grid gap-2 col-8 mx-auto",
                                                children=dcc.Upload(
                                                    id="parameters-upload",
                                                    children=[
                                                        html.I(
                                                            className="bi bi-cloud-upload me-2",
                                                            style={
                                                                "fontSize": "xx-large"
                                                            },
                                                        ),
                                                        html.Br(),
                                                        "drag & drop or select file",
                                                    ],
                                                ),
                                            ),
                                        ),
                                    ),
                                ]
                            ),
                        ]
                    )
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="⚙ ️Parameters",
    )
    layout = (
        html.Div(
            [
                html.H1(children="Better Roadmap", className="display-3"),
                html.P(
                    """
                        Estimate your "agile sprints" until the end of days to please the PHBs.
                    """,
                    className="lead",
                ),
                dbc.Tabs([tab_chart, tab_features, tab_parameters]),
            ]
        ),
    )
    return dbc.Container(layout, fluid=True)
