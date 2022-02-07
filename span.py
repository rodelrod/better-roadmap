from dataclasses import dataclass
from datetime import datetime, timedelta


def sprint_to_start_date(sprint: int, project_start: datetime) -> datetime:
    # Sprint numbers are 1-based. To get the sprint start date we need to subtract 1.
    return project_start + timedelta(weeks=(sprint - 1))


def sprint_to_end_date(sprint: int, project_start: datetime) -> datetime:
    return project_start + timedelta(weeks=sprint)


@dataclass
class SprintSpan:
    start: int
    end: int


@dataclass
class FeatureSprintSpans:
    ux: SprintSpan
    conception: SprintSpan
    dev: SprintSpan


@dataclass
class DateSpan:
    start: datetime
    end: datetime

    @classmethod
    def from_sprint_span(cls, sprint_span: SprintSpan, project_start: datetime):
        return cls(
            start=sprint_to_start_date(
                sprint=sprint_span.start, project_start=project_start
            ),
            end=sprint_to_end_date(sprint=sprint_span.end, project_start=project_start),
        )


@dataclass
class FeatureDateSpans:
    ux: DateSpan
    conception: DateSpan
    dev: DateSpan

    @classmethod
    def from_feature_sprint_spans(
        cls, sprint_spans: FeatureSprintSpans, project_start: datetime
    ):
        return cls(
            ux=DateSpan.from_sprint_span(sprint_spans.ux, project_start),
            conception=DateSpan.from_sprint_span(
                sprint_spans.conception, project_start
            ),
            dev=DateSpan.from_sprint_span(sprint_spans.dev, project_start),
        )


@dataclass
class GraphSegment:
    """Scheduled span for a Feature to be developed, ready to be put in the Roadmap."""

    feature: str
    start: datetime
    end: datetime
    phase: str
