import dash_bootstrap_components as dbc
from dash import dcc, html


def tab_elapsed(elapsed_text: str) -> dbc.Tab:

    return dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                elapsed_textarea(elapsed_text),
                            ),
                            dbc.Col(
                                [
                                    elapsed_update_download_buttons(),
                                    elapsed_download_button(),
                                    elapsed_validation_alert(),
                                ]
                            ),
                        ],
                    )
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="✅ Elapsed Sprints",
    )


def elapsed_textarea(elapsed_text: str) -> dbc.Textarea:
    return dbc.Textarea(
        id="elapsed-textarea",
        value=elapsed_text,
        rows=30,
        persistence=True,
        persistence_type="local",
    )


def elapsed_update_download_buttons():
    return dbc.Row(
        dbc.ButtonGroup(
            [
                dbc.Button(
                    html.Span(
                        [
                            "Update",
                            html.I(className="bi bi-bar-chart-steps ms-2"),
                        ]
                    ),
                    id="elapsed-update-button",
                    n_clicks=0,
                    className="btn-lg",
                ),
                dcc.Download(id="elapsed-download"),
                dbc.Button(
                    html.Span(
                        [
                            "Download",
                            html.I(className="bi bi-download ms-2"),
                        ]
                    ),
                    id="elapsed-download-button",
                    n_clicks=0,
                    className="btn-lg",
                ),
            ]
        ),
    )


def elapsed_download_button():
    return dbc.Row(
        className="mt-3",
        children=dbc.Col(
            dbc.Button(
                outline=True,
                color="primary",
                className="text-center d-grid gap-2 col-8 mx-auto",
                children=dcc.Upload(
                    id="elapsed-upload",
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
    )


def elapsed_validation_alert():
    return dbc.Row(
        className="mt-4",
        children=[
            dbc.Alert(
                [
                    html.H4("Validation error", className="alert-heading"),
                    html.P("", id="elapsed-validation-alert-text", className="mb-0"),
                ],
                is_open=False,
                color="danger",
                id="elapsed-validation-alert",
            )
        ],
    )
