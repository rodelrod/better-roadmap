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


class TestScheduledSpan:
    def test_sprint_to_date_spans(self):
        sss = sut.FeatureSprintSpans(
            ux=sut.SprintSpan(1, 3),
            conception=sut.SprintSpan(4, 4),
            dev=sut.SprintSpan(6, 8),
        )
        sts = sut.FeatureDateSpans(
            ux=sut.DateSpan(datetime(2022, 1, 6), datetime(2022, 1, 27)),
            conception=sut.DateSpan(datetime(2022, 1, 27), datetime(2022, 2, 3)),
            dev=sut.DateSpan(datetime(2022, 2, 10), datetime(2022, 3, 3)),
        )
        assert (
            sut.FeatureDateSpans.from_feature_sprint_spans(sss, datetime(2022, 1, 6))
            == sts
        )
