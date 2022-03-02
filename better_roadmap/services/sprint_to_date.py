from datetime import date, timedelta
from typing import Optional

from better_roadmap.models.parameters import SprintDuration


def sprint_to_end_date(
    sprint: int,
    project_start: date,
    sprint_durations: Optional[list[SprintDuration]] = None,
    default_sprint_duration: int = 1,
) -> date:
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
    project_start: date,
    sprint_durations: Optional[list[SprintDuration]] = None,
    default_sprint_duration=1,
) -> date:
    return sprint_to_end_date(
        sprint - 1, project_start, sprint_durations, default_sprint_duration
    )
