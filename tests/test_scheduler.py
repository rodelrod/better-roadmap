from datetime import date
import pytest

import better_roadmap.services.scheduler as sut
from better_roadmap.models.parameters import Phase


class TestStateIsValid:
    class TestWhenInitialStateIsMalformed:
        def test_when_too_many_slots_in_ux_then_false(self):
            phases = [
                Phase(name="ux", max_concurrency=1, min_gap_before=0),
                Phase(name="dev", max_concurrency=1, min_gap_before=0),
            ]
            assert not sut.FeatureScheduler._state_is_valid(
                phases,
                state={"ux": [1, 1], "dev": [1]},
            )

        def test_when_too_few_slots_in_dev_then_false(self):
            phases = [
                Phase(name="ux", max_concurrency=1, min_gap_before=0),
                Phase(name="dev", max_concurrency=4, min_gap_before=0),
            ]
            assert not sut.FeatureScheduler._state_is_valid(
                phases,
                state={"ux": [1], "dev": [1, 1]},
            )

        def test_when_missing_phase_then_false(self):
            phases = [
                Phase(name="ux", max_concurrency=1, min_gap_before=0),
                Phase(name="dev", max_concurrency=4, min_gap_before=0),
            ]
            assert not sut.FeatureScheduler._state_is_valid(
                phases,
                state={"ux": [1]},
            )

    class TestWhenInitialStateIsWellformed:
        def test_when_slots_are_correct_then_true(self):
            phases = [
                Phase(name="ux", max_concurrency=1, min_gap_before=0),
                Phase(name="dev", max_concurrency=4, min_gap_before=0),
            ]
            assert sut.FeatureScheduler._state_is_valid(
                phases,
                state={"ux": [1], "dev": [1, 1, 1, 1]},
            )


class TestScheduleFeature:
    @pytest.fixture
    def phases(self) -> list[Phase]:
        return [
            Phase(name="ux", max_concurrency=1, min_gap_before=0),
            Phase(
                name="conception",
                max_concurrency=2,
                min_gap_before=0,
                max_gap_after=3,
                default_estimation=1,
            ),
            Phase(name="dev", max_concurrency=2, min_gap_before=1),
        ]

    @pytest.fixture
    def scheduler(self, phases):
        return sut.FeatureScheduler(phases)

    class TestAsSprints:
        class TestWhenIsFirstFeature:
            def test_ux_estimation_2_and_dev_estimation_4(self, phases):
                scheduler_empty = sut.FeatureScheduler(phases)
                assert scheduler_empty.schedule_feature_as_sprints(
                    sut.Feature(
                        name="Skynet", estimations={"ux": 2, "conception": 1, "dev": 4}
                    )
                ) == sut.FeatureSprintSpans(
                    feature="Skynet",
                    spans=[
                        sut.SprintSpan(phase="ux", start=1, end=2),
                        sut.SprintSpan(phase="conception", start=3, end=3),
                        sut.SprintSpan(phase="dev", start=5, end=8),
                    ],
                )
                assert scheduler_empty._next_slots == {
                    "ux": [3],
                    "conception": [4, 1],
                    "dev": [9, 1],
                }

            def test_no_conception(self, phases):
                scheduler_empty = sut.FeatureScheduler(phases)
                assert scheduler_empty.schedule_feature_as_sprints(
                    sut.Feature(
                        name="Skynet", estimations={"ux": 2, "conception": 0, "dev": 4}
                    )
                ) == sut.FeatureSprintSpans(
                    feature="Skynet",
                    spans=[
                        sut.SprintSpan(phase="ux", start=1, end=2),
                        sut.SprintSpan(phase="dev", start=4, end=7),
                    ],
                )
                assert scheduler_empty._next_slots == {
                    "ux": [3],
                    "conception": [1, 1],
                    "dev": [8, 1],
                }

            def test_only_dev(self, phases):
                scheduler_empty = sut.FeatureScheduler(phases)
                assert scheduler_empty.schedule_feature_as_sprints(
                    sut.Feature(
                        name="Skynet", estimations={"ux": 0, "conception": 0, "dev": 4}
                    )
                ) == sut.FeatureSprintSpans(
                    feature="Skynet",
                    spans=[
                        sut.SprintSpan(phase="dev", start=1, end=4),
                    ],
                )
                assert scheduler_empty._next_slots == {
                    "ux": [1],
                    "conception": [1, 1],
                    "dev": [5, 1],
                }

    class TestAsDates:
        def test_schedule_feature_in_first_sprint(self, scheduler):
            feature = {
                "name": "Internal Blast",
                "ux_estimation": 2,
                "dev_estimation": 4,
            }
            feature = sut.Feature(
                name="Internal Blast", estimations={"ux": 2, "dev": 4}
            )
            assert scheduler.schedule_feature_as_dates(feature, date(2021, 10, 1)) == [
                sut.GraphSegment(
                    feature="Internal Blast",
                    start=date(2021, 10, 1),
                    end=date(2021, 10, 15),
                    phase="ux",
                ),
                sut.GraphSegment(
                    feature="Internal Blast",
                    start=date(2021, 10, 15),
                    end=date(2021, 10, 22),
                    phase="conception",
                ),
                sut.GraphSegment(
                    feature="Internal Blast",
                    start=date(2021, 10, 29),
                    end=date(2021, 11, 26),
                    phase="dev",
                ),
            ]
