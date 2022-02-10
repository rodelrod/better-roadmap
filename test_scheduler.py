from datetime import datetime
import scheduler as sut


def _feature(ux_estimation):
    return sut.Feature(
        "Skynet",
        estimations={"ux": ux_estimation, "conception": 1, "dev": 2},
    )


class TestStateIsValid:
    class TestWhenInitialStateIsMalformed:
        def test_when_too_many_slots_in_ux_then_false(self):
            params = sut.Parameters(
                datetime(2020, 1, 1), 1, [sut.Phase("ux", 1, 0), sut.Phase("dev", 1, 0)]
            )
            assert not sut.Scheduler._state_is_valid(
                params,
                state={"ux": [1, 1], "dev": [1]},
            )

        def test_when_too_few_slots_in_dev_then_false(self):
            params = sut.Parameters(
                datetime(2020, 1, 1), 1, [sut.Phase("ux", 1, 0), sut.Phase("dev", 4, 0)]
            )
            assert not sut.Scheduler._state_is_valid(
                params,
                state={"ux": [1], "dev": [1, 1]},
            )

        def test_when_missing_phase_then_false(self):
            params = sut.Parameters(
                datetime(2020, 1, 1), 1, [sut.Phase("ux", 1, 0), sut.Phase("dev", 4, 0)]
            )
            assert not sut.Scheduler._state_is_valid(
                params,
                state={"ux": [1]},
            )

    class TestWhenInitialStateIsWellformed:
        def test_when_slots_are_correct_then_true(self):
            params = sut.Parameters(
                datetime(2020, 1, 1), 1, [sut.Phase("ux", 1, 0), sut.Phase("dev", 4, 0)]
            )
            assert sut.Scheduler._state_is_valid(
                params,
                state={"ux": [1], "dev": [1, 1, 1, 1]},
            )


class TestScheduleFeature:
    class TestWhenIsFirstFeature:
        def test_ux_estimation_2_and_dev_estimation_4(self):
            scheduler_empty = sut.Scheduler()
            assert scheduler_empty.schedule_feature(
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
