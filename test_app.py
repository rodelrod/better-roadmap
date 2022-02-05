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
