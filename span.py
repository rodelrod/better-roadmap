from dataclasses import dataclass
from datetime import datetime, timedelta


def sprint_to_start_date(sprint: int, project_start: datetime) -> datetime:
    # Sprint numbers are 1-based. To get the sprint start date we need to subtract 1.
    return project_start + timedelta(weeks=(sprint - 1))


def sprint_to_end_date(sprint: int, project_start: datetime) -> datetime:
    return project_start + timedelta(weeks=sprint)


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


@dataclass
class DateSpan:
    phase: str
    start: datetime
    end: datetime

    @classmethod
    def from_sprint_span(cls, sprint_span: SprintSpan, project_start: datetime):
        return cls(
            phase=sprint_span.phase,
            start=sprint_to_start_date(
                sprint=sprint_span.start, project_start=project_start
            ),
            end=sprint_to_end_date(sprint=sprint_span.end, project_start=project_start),
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

    def get_graph_segments(self) -> list[GraphSegment]:
        return [
            GraphSegment(
                feature=self.feature, start=span.start, end=span.end, phase=span.phase
            )
            for span in self.spans
        ]
