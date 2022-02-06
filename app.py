#!/usr/bin/env python3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import yaml

from free_slots import FreeSlots

FEATURES_FILE = Path("data", "features.yml")
PARAMETERS_FILE = Path("data", "parameters.yml")


@dataclass
class FeatureSpan:
    """Scheduled span for a Feature to be developed, ready to be put in the Roadmap."""

    feature: str
    start: datetime
    end: datetime
    phase: str


def main():
    df = pd.DataFrame(
        [
            FeatureSpan(
                feature="Internal Blast",
                start=datetime(2021, 10, 1),
                end=datetime(2021, 10, 15),
                phase="UX",
            ),
            FeatureSpan(
                feature="Internal Blast",
                start=datetime(2021, 10, 21),
                end=datetime(2021, 10, 28),
                phase="Conception",
            ),
            FeatureSpan(
                feature="Internal Blast",
                start=datetime(2021, 11, 5),
                end=datetime(2021, 11, 20),
                phase="Dev",
            ),
            FeatureSpan(
                feature="Authentication",
                start=datetime(2021, 10, 1),
                end=datetime(2021, 10, 7),
                phase="Conception",
            ),
            FeatureSpan(
                feature="Authentication",
                start=datetime(2021, 10, 28),
                end=datetime(2021, 11, 5),
                phase="Dev",
            ),
        ]
    )

    fig = px.timeline(df, x_start="start", x_end="end", y="feature", color="phase")
    fig.update_yaxes(autorange="reversed")
    fig.show()


def parse_features() -> dict:
    with FEATURES_FILE.open() as features_file:
        features = yaml.load(features_file, Loader=yaml.SafeLoader)
    return features


if __name__ == "__main__":
    main()
