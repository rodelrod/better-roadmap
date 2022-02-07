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


@dataclass
class ScheduledDateSpans:
    ux: ScheduledDateSpan
    conception: ScheduledDateSpan
    dev: ScheduledDateSpan
