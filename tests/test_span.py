import better_roadmap.models.span as sut
from better_roadmap.models.parameters import SprintDuration

from datetime import date


class TestFeatureDateSpans:
    def test_convert_sprint_to_date_spans_with_normal_sprints_only(self):
        fss = sut.FeatureSprintSpans(
            feature="Skynet",
            spans=[
                sut.SprintSpan(phase="ux", start=1, end=3),
                sut.SprintSpan(phase="conception", start=4, end=4),
                sut.SprintSpan(phase="dev", start=6, end=8),
            ],
        )
        fds = sut.FeatureDateSpans(
            feature="Skynet",
            spans=[
                sut.DateSpan("ux", date(2022, 1, 6), date(2022, 1, 27)),
                sut.DateSpan("conception", date(2022, 1, 27), date(2022, 2, 3)),
                sut.DateSpan("dev", date(2022, 2, 10), date(2022, 3, 3)),
            ],
        )
        assert (
            sut.FeatureDateSpans.from_feature_sprint_spans(
                feature_sprint_spans=fss,
                project_start=date(2022, 1, 6),
                sprint_durations=[],
                default_sprint_duration=1,
            ) == fds
        )

    def test_convert_sprint_to_date_spans_with_normal_and_abnormal_sprints(self):
        fss = sut.FeatureSprintSpans(
            feature="Skynet",
            spans=[
                sut.SprintSpan(phase="ux", start=1, end=3),
                sut.SprintSpan(phase="conception", start=4, end=4),
                sut.SprintSpan(phase="dev", start=6, end=8),
            ],
        )
        sprint_durations = [
            SprintDuration(number=4, duration=2),
            SprintDuration(number=5, duration=3),
        ]
        fds = sut.FeatureDateSpans(
            feature="Skynet",
            spans=[
                sut.DateSpan("ux", date(2022, 1, 6), date(2022, 1, 27)),
                sut.DateSpan("conception", date(2022, 1, 27), date(2022, 2, 10)),
                sut.DateSpan("dev", date(2022, 3, 3), date(2022, 3, 24)),
            ],
        )
        assert (
            sut.FeatureDateSpans.from_feature_sprint_spans(
                feature_sprint_spans=fss,
                project_start=date(2022, 1, 6),
                sprint_durations=sprint_durations,
                default_sprint_duration=1,
            ) == fds
        )
