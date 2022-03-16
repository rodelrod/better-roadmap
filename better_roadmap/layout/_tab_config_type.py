import dash_bootstrap_components as dbc
from dash import dcc, html


def tab_config_type(config_type: str, config_text: str, label: str) -> dbc.Tab:

    return dbc.Tab(
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                config_type_textarea(config_type, config_text),
                            ),
                            dbc.Col(
                                [
                                    config_type_download_button(config_type),
                                    config_type_validation_alert(config_type),
                                ]
                            ),
                        ],
                    )
                ]
            ),
            style={"borderTop": "none"},
        ),
        label=label,
    )


def config_type_textarea(config_type: str, config_text: str) -> dbc.Textarea:
    return dbc.Textarea(
        id=f"{config_type}-textarea",
        value=config_text,
        rows=30,
        persistence=True,
        persistence_type="local",
    )


def config_type_download_button(config_type: str):
    return dbc.Row(
        dbc.Col(
            [
                dcc.Download(id=f"{config_type}-download"),
                dbc.Button(
                    html.Span(
                        [
                            "Download",
                            html.I(className="bi bi-download ms-2"),
                        ]
                    ),
                    id=f"{config_type}-download-button",
                    n_clicks=0,
                    className="btn-lg d-grid col-8 mx-auto",
                ),
            ]
        )
    )


def config_type_validation_alert(config_type: str):
    return dbc.Row(
        className="mt-4",
        children=[
            dbc.Alert(
                [
                    html.H4("Validation error", className="alert-heading"),
                    html.P(
                        "", id=f"{config_type}-validation-alert-text", className="mb-0"
                    ),
                ],
                is_open=False,
                color="danger",
                id=f"{config_type}-validation-alert",
            )
        ],
    )
