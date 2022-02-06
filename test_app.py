#!/usr/bin/env python3
import pytest

import app as sut


class TestFreeSlots:
    class TestNextSlots:
        class TestWhenIsFirstFeature:
            @pytest.fixture
            def free_slots_empty(self):
                return sut.FreeSlots()

            class TestWhenUxEstimationIsOne:
                def test_ux_is_slotted_on_first_sprint(self, free_slots_empty):
                    assert free_slots_empty.next_ux_slot() == 1

                def test_conception_is_slotted_on_second_slot(self, free_slots_empty):
                    assert free_slots_empty.next_conception_slot(ux_estimation=1) == 2

                def test_dev_is_slotted_on_fourth_slot(self, free_slots_empty):
                    assert free_slots_empty.next_dev_slot(ux_estimation=1) == 4

            class TestWhenUxEstimationIsGreaterThanOne:
                def test_ux_is_slotted_on_first_sprint(self, free_slots_empty):
                    assert free_slots_empty.next_ux_slot() == 1

                def test_conception_is_slotted_on_second_slot(self, free_slots_empty):
                    assert free_slots_empty.next_conception_slot(ux_estimation=3) == 4

                def test_dev_is_slotted_on_fourth_slot(self, free_slots_empty):
                    assert free_slots_empty.next_dev_slot(ux_estimation=3) == 6

        class TestWhenDevTeamIsLate:
            @pytest.fixture
            def free_slots_late_dev(self):
                initial_state = {"ux": (3,), "conception": (3, 3), "dev": (10, 11)}
                return sut.FreeSlots(initial_state=initial_state)

            def test_dev_is_slotted_on_first_available_slot_ie_ten(
                self, free_slots_late_dev
            ):
                assert free_slots_late_dev.next_dev_slot(ux_estimation=1) == 10

            def test_conception_is_slotted_three_sprints_before_dev_and_not_before(
                self, free_slots_late_dev
            ):
                assert free_slots_late_dev.next_conception_slot(ux_estimation=1) == 6

    class TestSetState:
        class TestWhenInitialStateIsMalformed:
            def test_when_too_many_slots_in_ux_raise(self):
                max_concurrency = sut.FreeSlotsMaxConcurrency(ux=1, conception=1, dev=1)
                with pytest.raises(sut.ArgumentError):
                    sut.FreeSlots(
                        max_concurrency=max_concurrency,
                        initial_state={"ux": (1, 1), "conception": (1,), "dev": (1,)},
                    )

            def test_when_too_few_slots_in_dev_raise(self):
                max_concurrency = sut.FreeSlotsMaxConcurrency(ux=1, conception=1, dev=4)
                with pytest.raises(sut.ArgumentError):
                    sut.FreeSlots(
                        max_concurrency=max_concurrency,
                        initial_state={
                            "ux": (1,),
                            "conception": (1,),
                            "dev": (
                                1,
                                1,
                                1,
                            ),
                        },
                    )

        class TestWhenInitialStateIsWellformed:
            def test_when_slots_are_correct_do_not_raise(self):
                max_concurrency = sut.FreeSlotsMaxConcurrency(ux=2, conception=1, dev=3)
                sut.FreeSlots(
                    max_concurrency=max_concurrency,
                    initial_state={"ux": (1, 1), "conception": (1,), "dev": (1, 1, 1)},
                )
