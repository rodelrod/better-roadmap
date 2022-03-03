from datetime import date
from typing import Optional, cast

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

from better_roadmap.models.elapsed import ElapsedFeatureList
from better_roadmap.models.features import FeatureList
from better_roadmap.models.parameters import Parameters
from better_roadmap.models.span import GraphSegment
from better_roadmap.services.scheduler import FeatureScheduler


class RoadmapChart:
    def __init__(
        self,
        elapsed_text: Optional[str] = None,
        features_text: Optional[str] = None,
        parameters_text: Optional[str] = None,
    ):
        # Make sure either all texts are provided or none of them is, in which
        # case we use the defaults from the yaml files in the server
        cast(
            Optional[tuple[str, str, str]],
            (elapsed_text, features_text, parameters_text),
        )
        parameters = Parameters.from_text(parameters_text)
        elapsed_feature_list = ElapsedFeatureList.from_text(elapsed_text)
        feature_list = FeatureList.from_text(features_text)
        ordered_phase_names = [phase.name for phase in parameters.phases]
        ordered_elapsed_features = [
            elapsed_feature.name for elapsed_feature in elapsed_feature_list
        ]
        ordered_features = [feature.name for feature in feature_list]
        scheduled_sprints = pd.DataFrame(
            self._get_graph_segments(parameters, elapsed_feature_list, feature_list)
        )
        self.figure = self._configure_chart(
            scheduled_sprints,
            ordered_phase_names,
            ordered_elapsed_features,
            ordered_features,
        )

    @staticmethod
    def _configure_chart(
        df: pd.DataFrame,
        ordered_phase_names,
        ordered_elapsed_features,
        ordered_features,
    ) -> Figure:
        fig = px.timeline(
            df,
            x_start="start",
            x_end="end",
            y="feature",
            color="phase",
            height=720,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            # This is necessary to ensure that the order of features in the YAML is respected
            category_orders={
                "phase": ordered_phase_names,
                "feature": ordered_elapsed_features + ordered_features,
            },
        )
        fig.add_vline(x=date.today())
        return fig

    @staticmethod
    def _get_graph_segments(
        parameters, elapsed_feature_list, feature_list
    ) -> list[GraphSegment]:
        graph_segments = []
        scheduler = FeatureScheduler(parameters.phases)
        for elapsed_feature in elapsed_feature_list:
            elapsed_feature_segments = scheduler.schedule_feature_as_dates(
                elapsed_feature,
                parameters.project_start,
                parameters.default_sprint_duration,
                parameters.sprint_durations,
            )
            graph_segments.extend(elapsed_feature_segments)
        for feature in feature_list:
            feature_segments = scheduler.schedule_feature_as_dates(
                feature,
                parameters.project_start,
                parameters.default_sprint_duration,
                parameters.sprint_durations,
            )
            graph_segments.extend(feature_segments)
        return graph_segments
