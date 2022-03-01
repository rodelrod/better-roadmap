import dash_bootstrap_components as dbc
from dash import dcc, html


def tab_actuals(actuals_text: str) -> dbc.Tab:

    return dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                actuals_textarea(actuals_text),
                            ),
                            dbc.Col(
                                actuals_buttons(),
                            ),
                        ],
                    )
                ]
            ),
            style={"borderTop": "none"},
        ),
        label="✅ Actual Sprints",
    )


def actuals_textarea(actuals_text: str) -> dbc.Textarea:
    return dbc.Textarea(
        id="actuals-textarea",
        value=actuals_text,
        rows=30,
        persistence=True,
        persistence_type="local",
    )


def actuals_buttons() -> list[dbc.Row]:
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
                        id="actuals-update-button",
                        n_clicks=0,
                        className="btn-lg",
                    ),
                    dcc.Download(id="actuals-download"),
                    dbc.Button(
                        html.Span(
                            [
                                "Download",
                                html.I(className="bi bi-download ms-2"),
                            ]
                        ),
                        id="actuals-download-button",
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
                        id="actuals-upload",
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
