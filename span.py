from dataclasses import dataclass
from datetime import datetime, timedelta


def sprint_to_start_date(sprint: int, project_start: datetime) -> datetime:
    # Sprint numbers are 1-based. To get the sprint start date we need to subtract 1.
    return project_start + timedelta(weeks=(sprint - 1))


def sprint_to_end_date(sprint: int, project_start: datetime) -> datetime:
    return project_start + timedelta(weeks=sprint)


@dataclass
class ScheduledSprintSpan:
    start: int
    end: int


@dataclass
class ScheduledSprintSpans:
    ux: ScheduledSprintSpan
    conception: ScheduledSprintSpan
    dev: ScheduledSprintSpan


@dataclass
class ScheduledDateSpan:
    start: datetime
    end: datetime

    @classmethod
    def from_scheduled_sprint_span(
        cls, sprint_span: ScheduledSprintSpan, project_start: datetime
    ):
        return cls(
            start=sprint_to_start_date(
                sprint=sprint_span.start, project_start=project_start
            ),
            end=sprint_to_end_date(sprint=sprint_span.end, project_start=project_start),
        )


@dataclass
class ScheduledDateSpans:
    ux: ScheduledDateSpan
    conception: ScheduledDateSpan
    dev: ScheduledDateSpan

    @classmethod
    def from_scheduled_sprint_spans(
        cls, sprint_spans: ScheduledSprintSpans, project_start: datetime
    ):
        return cls(
            ux=ScheduledDateSpan.from_scheduled_sprint_span(
                sprint_spans.ux, project_start
            ),
            conception=ScheduledDateSpan.from_scheduled_sprint_span(
                sprint_spans.conception, project_start
            ),
            dev=ScheduledDateSpan.from_scheduled_sprint_span(
                sprint_spans.dev, project_start
            ),
        )
