#!/usr/bin/env python3
from pathlib import Path

import pandas as pd
import plotly.express as px
import yaml

FEATURES_FILE = Path("data", "features.yml")
PARAMETERS_FILE = Path("data", "parameters.yml")


def main():
    df = pd.DataFrame(
        [
            dict(
                Feature="Internal Blast",
                Start="2021-10-01",
                Finish="2021-10-15",
                Resource="UX",
            ),
            dict(
                Feature="Internal Blast",
                Start="2021-10-21",
                Finish="2021-10-28",
                Resource="Conception",
            ),
            dict(
                Feature="Internal Blast",
                Start="2021-11-05",
                Finish="2021-11-20",
                Resource="Dev",
            ),
            dict(
                Feature="Authentication",
                Start="2021-10-01",
                Finish="2021-10-07",
                Resource="Conception",
            ),
            dict(
                Feature="Authentication",
                Start="2021-10-28",
                Finish="2021-11-05",
                Resource="Dev",
            ),
        ]
    )

    fig = px.timeline(
        df, x_start="Start", x_end="Finish", y="Feature", color="Resource"
    )
    fig.update_yaxes(autorange="reversed")
    fig.show()


def parse_features() -> dict:
    with FEATURES_FILE.open() as features_file:
        features = yaml.load(features_file, Loader=yaml.SafeLoader)
    return features


if __name__ == "__main__":
    main()
