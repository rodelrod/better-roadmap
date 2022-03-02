from datetime import date

import better_roadmap.services.sprint_to_date as sut
from better_roadmap.models.span import SprintDuration


class TestSprintToStartDate:
    def test_sprint_3_without_abnormal_sprints(self):
        assert sut.sprint_to_start_date(
            sprint=3, project_start=date(2022, 1, 6)
        ) == date(2022, 1, 20)

    def test_sprint_5_with_abnormal_sprints(self):
        sprint_durations = [
            SprintDuration(number=2, duration=3),
            SprintDuration(number=3, duration=2),
            SprintDuration(number=6, duration=2),
        ]
        assert sut.sprint_to_start_date(
            sprint=5,
            project_start=date(2022, 1, 6),
            sprint_durations=sprint_durations,
        ) == date(2022, 2, 24)

    def test_sprint_5_with_custom_default_sprint_duration(self):
        assert sut.sprint_to_start_date(
            sprint=5, project_start=date(2022, 1, 6), default_sprint_duration=2
        ) == date(2022, 3, 3)


class TestSprintToEndDate:
    def test_sprint_3_without_abnormal_sprints(self):
        assert sut.sprint_to_end_date(sprint=3, project_start=date(2022, 1, 6)) == date(
            2022, 1, 27
        )

