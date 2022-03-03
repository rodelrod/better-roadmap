from datetime import date, timedelta
from typing import Optional

from better_roadmap.models.parameters import SprintDuration


def sprint_to_end_date(
    sprint: int,
    project_start: date,
    sprint_durations: Optional[list[SprintDuration]] = None,
    default_sprint_duration: int = 1,
) -> date:
    abnormal_sprints = []
    abnormal_sprints_in_weeks = 0
    if sprint_durations:
        abnormal_sprints = [sd for sd in sprint_durations if sd.number <= sprint]
        abnormal_sprints_in_weeks = sum(sd.duration for sd in abnormal_sprints)
    normal_sprints_in_weeks = (sprint - len(abnormal_sprints)) * default_sprint_duration
    return project_start + timedelta(
        weeks=(abnormal_sprints_in_weeks + normal_sprints_in_weeks)
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
