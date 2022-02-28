from operator import xor
from typing import Optional, cast

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

from .features import FeatureList
from .parameters import Parameters
from .scheduler import Scheduler


class RoadmapChart:
    def __init__(
        self,
        features_text: Optional[str] = None,
        parameters_text: Optional[str] = None,
    ):
        # Make sure either both texts are provided or none of them is, in which
        # case we use the defaults from the yaml files in the server
        cast(Optional[tuple[str, str]], (features_text, parameters_text))
        scheduled_sprints = self._get_dataframe(features_text, parameters_text)
        self.figure = self._configure_chart(scheduled_sprints)

    @staticmethod
    def _configure_chart(df: pd.DataFrame) -> Figure:
        fig = px.timeline(
            df, x_start="start", x_end="end", y="feature", color="phase", height=720
        )
        fig.update_yaxes(autorange="reversed")
        return fig

    @staticmethod
    def _get_dataframe(
        features_text: Optional[str], parameters_text: Optional[str]
    ) -> pd.DataFrame:
        graph_segments = []
        parameters = Parameters.from_text(parameters_text)
        scheduler = Scheduler(parameters.phases)
        for feature in FeatureList.from_text(features_text):
            graph_segments.extend(
                scheduler.schedule_feature_as_dates(feature, parameters.project_start)
            )
        return pd.DataFrame(graph_segments)
