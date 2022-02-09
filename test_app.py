from datetime import datetime

import app as sut


class TestScheduleFeature:
    def test_schedule_feature_in_first_sprint(self):
        feature = {"name": "Internal Blast", "ux_estimation": 2, "dev_estimation": 4}
        feature = sut.Feature(name="Internal Blast", estimations={"ux": 2, "dev": 4})
        assert sut.schedule_feature(feature) == [
            sut.GraphSegment(
                feature="Internal Blast",
                start=datetime(2021, 10, 1),
                end=datetime(2021, 10, 15),
                phase="UX",
            ),
            sut.GraphSegment(
                feature="Internal Blast",
                start=datetime(2021, 10, 15),
                end=datetime(2021, 10, 22),
                phase="Conception",
            ),
            sut.GraphSegment(
                feature="Internal Blast",
                start=datetime(2021, 10, 29),
                end=datetime(2021, 11, 26),
                phase="Dev",
            ),
        ]
