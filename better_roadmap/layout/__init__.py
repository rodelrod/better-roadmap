import dash_bootstrap_components as dbc
from dash import html
from plotly.graph_objects import Figure

from ._tab_actuals import tab_actuals
from ._tab_chart import tab_chart
from ._tab_features import tab_features
from ._tab_parameters import tab_parameters


def layout(
    roadmap_chart: Figure, actuals_text: str, features_text: str, parameters_text: str
):
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
                        tab_actuals(actuals_text),
                        tab_features(features_text),
                        tab_parameters(parameters_text),
                    ]
                ),
            ]
        ),
    )
    return dbc.Container(layout, fluid=True)
