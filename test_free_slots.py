import pytest

import free_slots as sut


class TestNextSlots:
    class TestWhenIsFirstFeature:
        @pytest.fixture
        def free_slots_empty(self):
            return sut.FreeSlots()

        class TestWhenUxEstimationIsOne:
            def test_ux_is_slotted_on_first_sprint(self, free_slots_empty):
                assert free_slots_empty.get_next_ux_slot() == 1

            def test_conception_is_slotted_on_second_slot(self, free_slots_empty):
                assert free_slots_empty.get_next_conception_slot(ux_estimation=1) == 2

            def test_dev_is_slotted_on_fourth_slot(self, free_slots_empty):
                assert free_slots_empty.get_next_dev_slot(ux_estimation=1) == 4

        class TestWhenUxEstimationIsGreaterThanOne:
            def test_ux_is_slotted_on_first_sprint(self, free_slots_empty):
                assert free_slots_empty.get_next_ux_slot() == 1

            def test_conception_is_slotted_on_second_slot(self, free_slots_empty):
                assert free_slots_empty.get_next_conception_slot(ux_estimation=3) == 4

            def test_dev_is_slotted_on_fourth_slot(self, free_slots_empty):
                assert free_slots_empty.get_next_dev_slot(ux_estimation=3) == 6

    class TestWhenDevTeamIsLate:
        @pytest.fixture
        def free_slots_late_dev(self):
            initial_state = {"ux": [3], "conception": [3, 3], "dev": [10, 11]}
            return sut.FreeSlots(initial_state=initial_state)

        def test_dev_is_slotted_on_first_available_slot_ie_ten(
            self, free_slots_late_dev
        ):
            assert free_slots_late_dev.get_next_dev_slot(ux_estimation=1) == 10

        def test_conception_is_slotted_three_sprints_before_dev_and_not_before(
            self, free_slots_late_dev
        ):
            assert free_slots_late_dev.get_next_conception_slot(ux_estimation=1) == 6


class TestSetState:
    class TestWhenInitialStateIsMalformed:
        def test_when_too_many_slots_in_ux_raise(self):
            max_concurrency = sut.FreeSlotsMaxConcurrency(ux=1, conception=1, dev=1)
            with pytest.raises(sut.ArgumentError):
                sut.FreeSlots(
                    max_concurrency=max_concurrency,
                    initial_state={"ux": [1, 1], "conception": [1], "dev": [1]},
                )

        def test_when_too_few_slots_in_dev_raise(self):
            max_concurrency = sut.FreeSlotsMaxConcurrency(ux=1, conception=1, dev=4)
            with pytest.raises(sut.ArgumentError):
                sut.FreeSlots(
                    max_concurrency=max_concurrency,
                    initial_state={
                        "ux": [1],
                        "conception": [1],
                        "dev": [
                            1,
                            1,
                            1,
                        ],
                    },
                )

    class TestWhenInitialStateIsWellformed:
        def test_when_slots_are_correct_do_not_raise(self):
            max_concurrency = sut.FreeSlotsMaxConcurrency(ux=2, conception=1, dev=3)
            sut.FreeSlots(
                max_concurrency=max_concurrency,
                initial_state={"ux": [1, 1], "conception": [1], "dev": [1, 1, 1]},
            )


class TestScheduleFeature:
    class TestWhenIsFirstFeature:
        def test_ux_estimation_2_and_dev_estimation_4(self):
            free_slots_empty = sut.FreeSlots()
            assert free_slots_empty.schedule_feature(
                sut.Feature(name="Skynet", ux_estimation=2, dev_estimation=4)
            ) == sut.ScheduledSprintSpans(
                ux=sut.ScheduledSprintSpan(1, 2),
                conception=sut.ScheduledSprintSpan(3, 3),
                dev=sut.ScheduledSprintSpan(5, 8),
            )
            assert free_slots_empty._next_ux_slots == [3]
            assert free_slots_empty._next_conception_slots == [4, 1]
            assert free_slots_empty._next_dev_slots == [9, 1]
