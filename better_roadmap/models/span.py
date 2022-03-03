from dataclasses import dataclass
from typing import Optional
from datetime import date

from .parameters import SprintDuration
from .elapsed import ElapsedFeature
from ..services.sprint_to_date import sprint_to_end_date, sprint_to_start_date


@dataclass
class GraphSegment:
    """Scheduled span for a Feature to be developed, ready to be put in the Roadmap."""

    feature: str
    start: date
    end: date
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
    def from_elapsed_feature(cls, elapsed_feature: ElapsedFeature):
        return cls(
            feature=elapsed_feature.name,
            spans=[
                SprintSpan(phase=phase, start=span.start, end=span.end)
                for (phase, span) in elapsed_feature.elapsed.items()
            ],
        )


@dataclass
class DateSpan:
    phase: str
    start: date
    end: date

    @classmethod
    def from_sprint_span(
        cls,
        sprint_span: SprintSpan,
        project_start: date,
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
        cls,
        feature_sprint_spans: FeatureSprintSpans,
        project_start: date,
        sprint_durations: list[SprintDuration] = None,
        default_sprint_duration: int = 1,
    ):
        return cls(
            feature=feature_sprint_spans.feature,
            spans=[
                DateSpan.from_sprint_span(
                    sprint_span,
                    project_start,
                    sprint_durations,
                    default_sprint_duration,
                )
                for sprint_span in feature_sprint_spans.spans
            ],
        )

    def get_graph_segments(self) -> list[GraphSegment]:
        return [
            GraphSegment(
                feature=self.feature, start=span.start, end=span.end, phase=span.phase
            )
            for span in self.spans
        ]
