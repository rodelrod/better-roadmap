from typing import Optional, cast

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

from better_roadmap.models.span import GraphSegment

from .actuals import ActualFeatureList
from .features import FeatureList
from .parameters import Parameters
from .scheduler import FeatureScheduler


class RoadmapChart:
    def __init__(
        self,
        actuals_text: Optional[str] = None,
        features_text: Optional[str] = None,
        parameters_text: Optional[str] = None,
    ):
        # Make sure either all texts are provided or none of them is, in which
        # case we use the defaults from the yaml files in the server
        cast(
            Optional[tuple[str, str, str]],
            (actuals_text, features_text, parameters_text),
        )
        scheduled_sprints = pd.DataFrame(
            self._get_graph_segments(actuals_text, features_text, parameters_text)
        )
        self.figure = self._configure_chart(scheduled_sprints)

    @staticmethod
    def _configure_chart(df: pd.DataFrame) -> Figure:
        fig = px.timeline(
            df, x_start="start", x_end="end", y="feature", color="phase", height=720
        )
        fig.update_yaxes(autorange="reversed")
        return fig

    @staticmethod
    def _get_graph_segments(
        actuals_text: Optional[str],
        features_text: Optional[str],
        parameters_text: Optional[str],
    ) -> list[GraphSegment]:
        graph_segments = []
        parameters = Parameters.from_text(parameters_text)
        scheduler = FeatureScheduler(parameters.phases)
        for actual_feature in ActualFeatureList.from_text(actuals_text):
            graph_segments.extend(
                scheduler.schedule_feature_as_dates(
                    actual_feature, parameters.project_start
                )
            )
        for feature in FeatureList.from_text(features_text):
            graph_segments.extend(
                scheduler.schedule_feature_as_dates(feature, parameters.project_start)
            )
        return graph_segments
