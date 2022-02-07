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
        sss = sut.ScheduledSprintSpans(
            ux=sut.ScheduledSprintSpan(1, 3),
            conception=sut.ScheduledSprintSpan(4, 4),
            dev=sut.ScheduledSprintSpan(6, 8),
        )
        sts = sut.ScheduledDateSpans(
            ux=sut.ScheduledDateSpan(datetime(2022, 1, 6), datetime(2022, 1, 27)),
            conception=sut.ScheduledDateSpan(
                datetime(2022, 1, 27), datetime(2022, 2, 3)
            ),
            dev=sut.ScheduledDateSpan(datetime(2022, 2, 10), datetime(2022, 3, 3)),
        )
        assert (
            sut.ScheduledDateSpans.from_scheduled_sprint_spans(
                sss, datetime(2022, 1, 6)
            )
            == sts
        )
