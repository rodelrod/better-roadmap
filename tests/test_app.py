from datetime import datetime
import pytest

import better_roadmap.app as sut
from better_roadmap.parameters import Phase
from better_roadmap.scheduler import Scheduler


class TestScheduleFeature:
    @pytest.fixture
    def scheduler(self) -> Scheduler:
        phases = [
            Phase("ux", 1, 0),
            Phase("conception", 2, 0, 3, 1),
            Phase("dev", 2, 1),
        ]
        return Scheduler(phases)

    def test_schedule_feature_in_first_sprint(self, scheduler):
        feature = {"name": "Internal Blast", "ux_estimation": 2, "dev_estimation": 4}
        feature = sut.Feature(name="Internal Blast", estimations={"ux": 2, "dev": 4})
        assert sut.schedule_feature(feature, datetime(2021, 10, 1), scheduler) == [
            sut.GraphSegment(
                feature="Internal Blast",
                start=datetime(2021, 10, 1),
                end=datetime(2021, 10, 15),
                phase="ux",
            ),
            sut.GraphSegment(
                feature="Internal Blast",
                start=datetime(2021, 10, 15),
                end=datetime(2021, 10, 22),
                phase="conception",
            ),
            sut.GraphSegment(
                feature="Internal Blast",
                start=datetime(2021, 10, 29),
                end=datetime(2021, 11, 26),
                phase="dev",
            ),
        ]
