from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta

from .parameters import SprintDuration
from .actuals import ActualFeature


def sprint_to_end_date(
    sprint: int,
    project_start: datetime,
    sprint_durations: Optional[list[SprintDuration]] = None,
    default_sprint_duration: int = 1,
) -> datetime:
    atypical_sprints = []
    atypical_sprints_in_weeks = 0
    if sprint_durations:
        atypical_sprints = [sd for sd in sprint_durations if sd.number <= sprint]
        atypical_sprints_in_weeks = sum(sd.duration for sd in atypical_sprints)
    normal_sprints_in_weeks = (sprint - len(atypical_sprints)) * default_sprint_duration
    return project_start + timedelta(
        weeks=(atypical_sprints_in_weeks + normal_sprints_in_weeks)
    )


def sprint_to_start_date(
    sprint: int,
    project_start: datetime,
    sprint_durations: Optional[list[SprintDuration]] = None,
    default_sprint_duration=1,
) -> datetime:
    return sprint_to_end_date(
        sprint - 1, project_start, sprint_durations, default_sprint_duration
    )


@dataclass
class GraphSegment:
    """Scheduled span for a Feature to be developed, ready to be put in the Roadmap."""

    feature: str
    start: datetime
    end: datetime
    phase: str


@dataclass
class SprintSpan:
    phase: str
    start: int
    end: int


@dataclass
class FeatureSprintSpans:
    feature: str
    spans: list[SprintSpan]

    @classmethod
    def from_actual_feature(cls, actual_feature: ActualFeature):
        return cls(
            feature=actual_feature.name,
            spans=[
                SprintSpan(phase=phase, start=span.start, end=span.end)
                for (phase, span) in actual_feature.actual.items()
            ],
        )


@dataclass
class DateSpan:
    phase: str
    start: datetime
    end: datetime

    @classmethod
    def from_sprint_span(
        cls,
        sprint_span: SprintSpan,
        project_start: datetime,
        sprint_durations: Optional[list[SprintDuration]] = None,
        default_sprint_duration: int = 1,
    ):
        return cls(
            phase=sprint_span.phase,
            start=sprint_to_start_date(
                sprint_span.start,
                project_start,
                sprint_durations,
                default_sprint_duration,
            ),
            end=sprint_to_end_date(
                sprint_span.end,
                project_start,
                sprint_durations,
                default_sprint_duration,
            ),
        )


@dataclass
class FeatureDateSpans:
    feature: str
    spans: list[DateSpan]

    @classmethod
    def from_feature_sprint_spans(
        cls, feature_sprint_spans: FeatureSprintSpans, project_start: datetime
    ):
        return cls(
            feature=feature_sprint_spans.feature,
            spans=[
                DateSpan.from_sprint_span(sprint_span, project_start)
                for sprint_span in feature_sprint_spans.spans
            ],
        )

    @classmethod
    def from_actual_feature(
        cls, actual_feature: ActualFeature, project_start: datetime
    ):
        feature_sprint_spans = FeatureSprintSpans.from_actual_feature(actual_feature)
        return cls.from_feature_sprint_spans(feature_sprint_spans, project_start)

    def get_graph_segments(self) -> list[GraphSegment]:
        return [
            GraphSegment(
                feature=self.feature, start=span.start, end=span.end, phase=span.phase
            )
            for span in self.spans
        ]
