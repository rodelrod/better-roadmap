import pytest

from datetime import datetime
import free_slots as sut


def _feature(ux_estimation):
    return sut.Feature(
        "Skynet",
        estimations={"ux": ux_estimation, "conception": 1, "dev": 2},
    )


class TestNextSlots:
    class TestWhenIsFirstFeature:
        @pytest.fixture
        def free_slots_empty(self):
            return sut.FreeSlots()

        class TestWhenUxEstimationIsOne:
            def test_ux_is_slotted_on_first_sprint(self, free_slots_empty):
                assert free_slots_empty.get_next_ux_slot() == 1

            def test_conception_is_slotted_on_second_slot(self, free_slots_empty):
                assert (
                    free_slots_empty.get_next_conception_slot(_feature(ux_estimation=1))
                    == 2
                )

            def test_dev_is_slotted_on_fourth_slot(self, free_slots_empty):
                assert (
                    free_slots_empty.get_next_dev_slot(_feature(ux_estimation=1)) == 4
                )

        class TestWhenUxEstimationIsGreaterThanOne:
            def test_ux_is_slotted_on_first_sprint(self, free_slots_empty):
                assert free_slots_empty.get_next_ux_slot() == 1

            def test_conception_is_slotted_on_second_slot(self, free_slots_empty):
                assert (
                    free_slots_empty.get_next_conception_slot(_feature(ux_estimation=3))
                    == 4
                )

            def test_dev_is_slotted_on_fourth_slot(self, free_slots_empty):
                assert (
                    free_slots_empty.get_next_dev_slot(_feature(ux_estimation=3)) == 6
                )

    class TestWhenDevTeamIsLate:
        @pytest.fixture
        def free_slots_late_dev(self):
            initial_state = {"ux": [3], "conception": [3, 3], "dev": [10, 11]}
            return sut.FreeSlots(initial_state=initial_state)

        def test_dev_is_slotted_on_first_available_slot_ie_ten(
            self, free_slots_late_dev
        ):
            assert (
                free_slots_late_dev.get_next_dev_slot(_feature(ux_estimation=1)) == 10
            )

        def test_conception_is_slotted_three_sprints_before_dev_and_not_before(
            self, free_slots_late_dev
        ):
            assert (
                free_slots_late_dev.get_next_conception_slot(_feature(ux_estimation=1))
                == 6
            )


class TestStateIsValid:
    class TestWhenInitialStateIsMalformed:
        def test_when_too_many_slots_in_ux_then_false(self):
            params = sut.Parameters(
                datetime(2020, 1, 1), 1, [sut.Phase("ux", 1, 0), sut.Phase("dev", 1, 0)]
            )
            assert not sut.FreeSlots._state_is_valid(
                params,
                state={"ux": [1, 1], "dev": [1]},
            )

        def test_when_too_few_slots_in_dev_then_false(self):
            params = sut.Parameters(
                datetime(2020, 1, 1), 1, [sut.Phase("ux", 1, 0), sut.Phase("dev", 4, 0)]
            )
            assert not sut.FreeSlots._state_is_valid(
                params,
                state={"ux": [1], "dev": [1, 1]},
            )

        def test_when_missing_phase_then_false(self):
            params = sut.Parameters(
                datetime(2020, 1, 1), 1, [sut.Phase("ux", 1, 0), sut.Phase("dev", 4, 0)]
            )
            assert not sut.FreeSlots._state_is_valid(
                params,
                state={"ux": [1]},
            )

    class TestWhenInitialStateIsWellformed:
        def test_when_slots_are_correct_then_true(self):
            params = sut.Parameters(
                datetime(2020, 1, 1), 1, [sut.Phase("ux", 1, 0), sut.Phase("dev", 4, 0)]
            )
            assert sut.FreeSlots._state_is_valid(
                params,
                state={"ux": [1], "dev": [1, 1, 1, 1]},
            )


class TestScheduleFeature:
    class TestWhenIsFirstFeature:
        def test_ux_estimation_2_and_dev_estimation_4(self):
            free_slots_empty = sut.FreeSlots()
            assert free_slots_empty.schedule_feature(
                sut.Feature(name="Skynet", estimations={"ux": 2, "dev": 4})
            ) == sut.FeatureSprintSpans(
                feature="Skynet",
                ux=sut.SprintSpan(1, 2),
                conception=sut.SprintSpan(3, 3),
                dev=sut.SprintSpan(5, 8),
            )
            assert free_slots_empty._next_slots == {
                "ux": [3],
                "conception": [4, 1],
                "dev": [9, 1],
            }
