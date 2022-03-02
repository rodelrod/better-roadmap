import better_roadmap.models.span as sut

from datetime import date


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
