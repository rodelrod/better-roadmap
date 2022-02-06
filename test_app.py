from datetime import datetime

import app as sut


class TestSprintToStartDate:
    def test_sprint_4_for_a_project_starting_end_of_year(self):
        assert sut.sprint_to_start_date(
            sprint=4, project_start=datetime(2021, 12, 30)
        ) == datetime(2022, 1, 20)
