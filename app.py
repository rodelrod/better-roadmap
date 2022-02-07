#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import yaml

from free_slots import FreeSlots
from feature import Feature
from span import FeatureDateSpans, GraphSegment

FEATURES_FILE = Path("data", "features.yml")
PARAMETERS_FILE = Path("data", "parameters.yml")
PROJECT_START = datetime(2021, 10, 1)


def main():
    graph_segments = []
    free_slots = FreeSlots()
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


def schedule_feature(
    feature: Feature, free_slots: FreeSlots = None
) -> list[GraphSegment]:
    # TODO allow features with default start date
    if not free_slots:
        free_slots = FreeSlots()
    feature_sprint_spans = free_slots.schedule_feature(feature)
    feature_data_spans = FeatureDateSpans.from_feature_sprint_spans(
        feature_sprint_spans, project_start=PROJECT_START
    )
    return feature_data_spans.get_graph_segments()


if __name__ == "__main__":
    main()
