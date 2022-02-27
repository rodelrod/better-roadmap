import dash_bootstrap_components as dbc
from dash import dcc, html


def tab_parameters(parameters_text: str) -> dbc.Tab:
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


def parameters_textarea(parameters_text: str) -> dbc.Textarea:
    return dbc.Textarea(
        id="parameters-textarea",
        value=parameters_text,
        rows=20,
        persistence=True,
        persistence_type="local",
    )


def parameters_buttons() -> list[dbc.Row]:
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
