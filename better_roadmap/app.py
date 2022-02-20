from datetime import datetime
import os
from pathlib import Path

from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import yaml

from .scheduler import Scheduler
from .feature import Feature
from .parameters import Parameters, Phase, SprintDuration
from .span import FeatureDateSpans, GraphSegment

APP_DIR = Path(os.getenv("APP_DIR", ".")).resolve()
FEATURES_FILE = APP_DIR / "data" / "features.yml"
PARAMETERS_FILE = APP_DIR / "data" / "parameters.yml"
ASSETS_FOLDER = APP_DIR / "assets"
PROJECT_START = datetime(2021, 10, 1)

app = Dash(__name__, title="Better Roadmap", assets_folder=ASSETS_FOLDER)


def configure_app(someapp: Dash):
    fig = update_graph()
    someapp.layout = layout(fig)


@app.callback(
    Output("roadmap-graph", "figure"),
    Input("features-textarea-button", "n_clicks"),
    State("features-textarea", "value"),
)
def update_graph_callback(n_clicks, input_value):
    return update_graph(input_value)


def update_graph(features=None):
    graph_segments = []
    parameters = parse_parameters()
    scheduler = Scheduler(parameters.phases)
    for feature in parse_features(features):
        graph_segments.extend(schedule_feature(feature, scheduler))
    df = pd.DataFrame(graph_segments)
    fig = chart(df)
    return fig


def chart(df: pd.DataFrame):
    fig = px.timeline(df, x_start="start", x_end="end", y="feature", color="phase")
    fig.update_yaxes(autorange="reversed")
    return fig


def layout(fig):
    return html.Div(
        children=[
            html.H1(children="Better Roadmap"),
            html.Div(
                children="""
                    Estimate your "agile sprints" until the end of days to please the PHBs.
                """
            ),
            dcc.Graph(id="roadmap-graph", figure=fig),
            dcc.Textarea(
                id="features-textarea",
                value=get_default_features_as_text(),
                persistence=True,
                persistence_type="local",
            ),
            html.Button("Submit", id="features-textarea-button", n_clicks=0),
        ]
    )


def parse_features(features_text) -> list[Feature]:
    if features_text:
        feature_dicts = yaml.safe_load(features_text)
    else:
        with FEATURES_FILE.open() as features_file:
            feature_dicts = yaml.safe_load(features_file)
    features = [Feature.from_dict(d) for d in feature_dicts]
    return features


def get_default_features_as_text() -> str:
    with FEATURES_FILE.open() as features_file:
        default_features = features_file.read()
    return default_features


def parse_parameters() -> Parameters:
    with PARAMETERS_FILE.open() as parameters_file:
        parameters_dict = yaml.load(parameters_file, Loader=yaml.SafeLoader)
    parameters = Parameters.from_dict(
        {
            "project_start": parameters_dict["project_start"],
            "default_sprint_duration": parameters_dict["default_sprint_duration"],
            "phases": [Phase.from_dict(p) for p in parameters_dict["phases"]],
            "sprint_durations": [
                SprintDuration.from_dict(s) for s in parameters_dict["sprints"]
            ],
        }
    )
    return parameters


def schedule_feature(
    feature: Feature, scheduler: Scheduler = None
) -> list[GraphSegment]:
    if not scheduler:
        scheduler = Scheduler()
    feature_sprint_spans = scheduler.schedule_feature(feature)
    feature_data_spans = FeatureDateSpans.from_feature_sprint_spans(
        feature_sprint_spans, project_start=PROJECT_START
    )
    return feature_data_spans.get_graph_segments()


configure_app(app)
