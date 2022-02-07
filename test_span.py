import span as sut

from datetime import datetime


class TestSprintToDate:
    def test_sprint_to_start_date(self):
        assert sut.sprint_to_start_date(
            sprint=3, project_start=datetime(2022, 1, 6)
        ) == datetime(2022, 1, 20)

    def test_sprint_to_end_date(self):
        assert sut.sprint_to_end_date(
            sprint=3, project_start=datetime(2022, 1, 6)
        ) == datetime(2022, 1, 27)
