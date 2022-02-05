#!/usr/bin/env python3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import yaml

FEATURES_FILE = Path("data", "features.yml")
PARAMETERS_FILE = Path("data", "parameters.yml")


@dataclass
class FeatureSpan:
    """Scheduled span for a Feature to be developed, ready to be put in the Roadmap."""

    feature: str
    start: datetime
    end: datetime
    phase: str


class FreeSlots:
    """Keep track of the latest sprints for each phase."""

    MAX_GAP_BETWEEN_CONCEPTION_AND_DEV = 4
    MIN_GAP_BETWEEN_CONCEPTION_AND_DEV = 2
    MIN_GAP_BETWEEN_UX_AND_CONCEPTION = 0

    def __init__(
        self, ux_max_concurrency=1, conception_max_concurrency=2, dev_max_concurrency=2
    ) -> None:
        self._next_ux_slots = tuple([1] * ux_max_concurrency)
        self._next_conception_slots = tuple([1] * conception_max_concurrency)
        self._next_dev_slots = tuple([1] * dev_max_concurrency)

    def next_ux_slot(self):
        return min(self._next_ux_slots)

    def next_conception_slot(self, ux_estimation):
        """Take Conception as soon as possible but not too early."""
        return max(
            # not too early before Dev, so that it does not need to be redone
            min(self._next_dev_slots) - self.MAX_GAP_BETWEEN_CONCEPTION_AND_DEV,
            max(
                # in the first available conception slot…
                min(self._next_conception_slots),
                # …as long as it's after UX is done
                self.next_ux_slot()
                + ux_estimation
                + self.MIN_GAP_BETWEEN_UX_AND_CONCEPTION,
            ),
        )

    def next_dev_slot(self, ux_estimation):
        """Start dev in the next slot available but only if gap with conception is respected"""
        return max(
            # in the first available slot…
            min(self._next_dev_slots),
            # …as long as the conception is done
            self.next_conception_slot(ux_estimation)
            + self.MIN_GAP_BETWEEN_CONCEPTION_AND_DEV,
        )


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
