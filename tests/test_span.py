import better_roadmap.models.span as sut

from datetime import date


class TestSprintToDate:
    def test_sprint_to_start_date(self):
        assert sut.sprint_to_start_date(
            sprint=3, project_start=date(2022, 1, 6)
        ) == date(2022, 1, 20)

    def test_sprint_to_end_date(self):
        assert sut.sprint_to_end_date(sprint=3, project_start=date(2022, 1, 6)) == date(
            2022, 1, 27
        )

    def test_sprint_to_start_date_with_longer_sprints(self):
        sprint_durations = [
            sut.SprintDuration(number=2, duration=3),
            sut.SprintDuration(number=3, duration=2),
            sut.SprintDuration(number=6, duration=2),
        ]
        assert sut.sprint_to_start_date(
            sprint=5,
            project_start=date(2022, 1, 6),
            sprint_durations=sprint_durations,
        ) == date(2022, 2, 24)

    def test_sprint_to_start_date_with_custom_sprint_duration(self):
        assert sut.sprint_to_start_date(
            sprint=5, project_start=date(2022, 1, 6), default_sprint_duration=2
        ) == date(2022, 3, 3)


class TestScheduledSpan:
    def test_sprint_to_date_spans(self):
        sss = sut.FeatureSprintSpans(
            feature="Skynet",
            spans=[
                sut.SprintSpan(phase="ux", start=1, end=3),
                sut.SprintSpan(phase="conception", start=4, end=4),
                sut.SprintSpan(phase="dev", start=6, end=8),
            ],
        )
        sts = sut.FeatureDateSpans(
            feature="Skynet",
            spans=[
                sut.DateSpan("ux", date(2022, 1, 6), date(2022, 1, 27)),
                sut.DateSpan("conception", date(2022, 1, 27), date(2022, 2, 3)),
                sut.DateSpan("dev", date(2022, 2, 10), date(2022, 3, 3)),
            ],
        )
        assert (
            sut.FeatureDateSpans.from_feature_sprint_spans(sss, date(2022, 1, 6)) == sts
        )
