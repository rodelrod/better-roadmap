from datetime import datetime
import pytest

import better_roadmap.models.scheduler as sut
from better_roadmap.models.parameters import Phase


class TestStateIsValid:
    class TestWhenInitialStateIsMalformed:
        def test_when_too_many_slots_in_ux_then_false(self):
            phases = [Phase("ux", 1, 0), Phase("dev", 1, 0)]
            assert not sut.Scheduler._state_is_valid(
                phases,
                state={"ux": [1, 1], "dev": [1]},
            )

        def test_when_too_few_slots_in_dev_then_false(self):
            phases = [Phase("ux", 1, 0), Phase("dev", 4, 0)]
            assert not sut.Scheduler._state_is_valid(
                phases,
                state={"ux": [1], "dev": [1, 1]},
            )

        def test_when_missing_phase_then_false(self):
            phases = [Phase("ux", 1, 0), Phase("dev", 4, 0)]
            assert not sut.Scheduler._state_is_valid(
                phases,
                state={"ux": [1]},
            )

    class TestWhenInitialStateIsWellformed:
        def test_when_slots_are_correct_then_true(self):
            phases = [Phase("ux", 1, 0), Phase("dev", 4, 0)]
            assert sut.Scheduler._state_is_valid(
                phases,
                state={"ux": [1], "dev": [1, 1, 1, 1]},
            )


class TestScheduleFeature:
    @pytest.fixture
    def phases(self) -> list[Phase]:
        return [
            Phase("ux", 1, 0),
            Phase("conception", 2, 0, 3, 1),
            Phase("dev", 2, 1),
        ]

    @pytest.fixture
    def scheduler(self, phases):
        return sut.Scheduler(phases)

    class TestAsSprints:
        class TestWhenIsFirstFeature:
            def test_ux_estimation_2_and_dev_estimation_4(self, phases):
                scheduler_empty = sut.Scheduler(phases)
                assert scheduler_empty.schedule_feature_as_sprints(
                    sut.Feature(
                        name="Skynet", estimations={"ux": 2, "conception": 1, "dev": 4}
                    )
                ) == sut.FeatureSprintSpans(
                    feature="Skynet",
                    spans=[
                        sut.SprintSpan("ux", 1, 2),
                        sut.SprintSpan("conception", 3, 3),
                        sut.SprintSpan("dev", 5, 8),
                    ],
                )
                assert scheduler_empty._next_slots == {
                    "ux": [3],
                    "conception": [4, 1],
                    "dev": [9, 1],
                }

            def test_no_conception(self, phases):
                scheduler_empty = sut.Scheduler(phases)
                assert scheduler_empty.schedule_feature_as_sprints(
                    sut.Feature(
                        name="Skynet", estimations={"ux": 2, "conception": 0, "dev": 4}
                    )
                ) == sut.FeatureSprintSpans(
                    feature="Skynet",
                    spans=[
                        sut.SprintSpan("ux", 1, 2),
                        sut.SprintSpan("dev", 4, 7),
                    ],
                )
                assert scheduler_empty._next_slots == {
                    "ux": [3],
                    "conception": [1, 1],
                    "dev": [8, 1],
                }

            def test_only_dev(self, phases):
                scheduler_empty = sut.Scheduler(phases)
                assert scheduler_empty.schedule_feature_as_sprints(
                    sut.Feature(
                        name="Skynet", estimations={"ux": 0, "conception": 0, "dev": 4}
                    )
                ) == sut.FeatureSprintSpans(
                    feature="Skynet",
                    spans=[
                        sut.SprintSpan("dev", 1, 4),
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
            assert scheduler.schedule_feature_as_dates(
                feature, datetime(2021, 10, 1)
            ) == [
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
