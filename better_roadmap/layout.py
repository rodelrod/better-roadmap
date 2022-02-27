import dash_bootstrap_components as dbc
from dash import dcc, html
from plotly.graph_objects import Figure


def layout(roadmap_chart: Figure, features_text: str, parameters_text: str):
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
                dbc.Tabs(
                    [
                        tab_chart(roadmap_chart),
                        tab_features(features_text),
                        tab_parameters(parameters_text),
                    ]
                ),
            ]
        ),
    )
    return dbc.Container(layout, fluid=True)


def tab_chart(fig):
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


def tab_features(features_text):

    return dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                features_textarea(features_text),
                            ),
                            dbc.Col(
                                features_buttons(),
                            ),
                        ],
                    )
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="🏆 Features",
    )


def features_textarea(features_text):
    return dbc.Textarea(
        id="features-textarea",
        value=features_text,
        rows=30,
        persistence=True,
        persistence_type="local",
    )


def features_buttons():
    return [
        dbc.Row(
            dbc.ButtonGroup(
                [
                    dbc.Button(
                        html.Span(
                            [
                                "Update",
                                html.I(className="bi bi-bar-chart-steps ms-2"),
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
                                html.I(className="bi bi-download ms-2"),
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
                                style={"fontSize": "xx-large"},
                            ),
                            html.Br(),
                            "drag & drop or select file",
                        ],
                    ),
                ),
            ),
        ),
    ]


def tab_parameters(parameters_text):
    return dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                parameters_textarea(parameters_text),
                            ),
                            dbc.Col(
                                parameters_buttons(),
                            ),
                        ]
                    )
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="⚙ ️Parameters",
    )


def parameters_textarea(parameters_text):
    return dbc.Textarea(
        id="parameters-textarea",
        value=parameters_text,
        rows=20,
        persistence=True,
        persistence_type="local",
    )


def parameters_buttons():
    return [
        dbc.Row(
            dbc.ButtonGroup(
                [
                    dbc.Button(
                        html.Span(
                            [
                                "Update",
                                html.I(className="bi bi-bar-chart-steps ms-2"),
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
                                html.I(className="bi bi-download ms-2"),
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
                                style={"fontSize": "xx-large"},
                            ),
                            html.Br(),
                            "drag & drop or select file",
                        ],
                    ),
                ),
            ),
        ),
    ]
