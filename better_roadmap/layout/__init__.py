import dash_bootstrap_components as dbc
from dash import html
from plotly.graph_objects import Figure

from ._tab_chart import tab_chart
from ._tab_config_type import tab_config_type

CONFIG_LABELS = {
    "elapsed": "✅ Elapsed Sprints",
    "features": "🏆 Planned Features",
    "parameters": "⚙ Parameters",
}


def layout(
    roadmap_chart: Figure, elapsed_text: str, features_text: str, parameters_text: str
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
                        tab_config_type(
                            "elapsed", elapsed_text, CONFIG_LABELS["elapsed"]
                        ),
                        tab_config_type(
                            "features", features_text, CONFIG_LABELS["features"]
                        ),
                        tab_config_type(
                            "parameters", parameters_text, CONFIG_LABELS["parameters"]
                        ),
                    ]
                ),
            ]
        ),
    )
    return dbc.Container(layout, fluid=True)
