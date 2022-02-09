#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import yaml

from free_slots import FreeSlots
from feature import Feature
from parameters import Parameters, Phase, Sprint
from span import FeatureDateSpans, GraphSegment

FEATURES_FILE = Path("data", "features.yml")
PARAMETERS_FILE = Path("data", "parameters.yml")
PROJECT_START = datetime(2021, 10, 1)


def main():
    graph_segments = []
    parameters = parse_parameters()
    free_slots = FreeSlots(parameters)
    for feature in parse_features():
        graph_segments.extend(schedule_feature(feature, free_slots))

    df = pd.DataFrame(graph_segments)

    fig = px.timeline(df, x_start="start", x_end="end", y="feature", color="phase")
    fig.update_yaxes(autorange="reversed")
    fig.show()


def parse_features() -> list[Feature]:
    with FEATURES_FILE.open() as features_file:
        feature_dicts = yaml.load(features_file, Loader=yaml.SafeLoader)
    features = [Feature.from_dict(d) for d in feature_dicts]
    return features


def parse_parameters() -> Parameters:
    with PARAMETERS_FILE.open() as parameters_file:
        parameters_dict = yaml.load(parameters_file, Loader=yaml.SafeLoader)
    parameters = Parameters.from_dict(
        {
            "project_start": parameters_dict["project_start"],
            "default_sprint_duration": parameters_dict["default_sprint_duration"],
            "phases": [Phase.from_dict(p) for p in parameters_dict["phases"]],
            "sprints": [Sprint.from_dict(s) for s in parameters_dict["sprints"]],
        }
    )
    return parameters


def schedule_feature(
    feature: Feature, free_slots: FreeSlots = None
) -> list[GraphSegment]:
    if not free_slots:
        free_slots = FreeSlots()
    feature_sprint_spans = free_slots.schedule_feature(feature)
    feature_data_spans = FeatureDateSpans.from_feature_sprint_spans(
        feature_sprint_spans, project_start=PROJECT_START
    )
    return feature_data_spans.get_graph_segments()


if __name__ == "__main__":
    main()
