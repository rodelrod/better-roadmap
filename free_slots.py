from dataclasses import dataclass

from feature import Feature
from span import SprintSpan, FeatureSprintSpans
from utils import replace_min


class ArgumentError(Exception):
    pass


@dataclass
class FreeSlotsMaxConcurrency:
    ux: int = 1
    conception: int = 2
    dev: int = 2


@dataclass
class FreeSlotsGaps:
    max_gap_between_conception_and_dev: int = 3
    min_gap_between_conception_and_dev: int = 1
    min_gap_between_ux_and_conception: int = 0


class FreeSlots:
    """Keep track of the latest sprints for each phase."""

    CONCEPTION_ESTIMATION = 1

    def __init__(
        self,
        max_concurrency: FreeSlotsMaxConcurrency = None,
        gaps: FreeSlotsGaps = None,
        initial_state: dict[str, list[int]] = None,
    ) -> None:
        self.max_concurrency = max_concurrency or FreeSlotsMaxConcurrency()
        self.gaps = gaps or FreeSlotsGaps()
        if not initial_state:
            self._next_ux_slots = [1] * self.max_concurrency.ux
            self._next_conception_slots = [1] * self.max_concurrency.conception
            self._next_dev_slots = [1] * self.max_concurrency.dev
        else:
            self._set_state(initial_state)

    def _set_state(self, state: dict[str, list[int]]) -> None:
        for phase in ["ux", "conception", "dev"]:
            if len(state[phase]) != getattr(self.max_concurrency, phase):
                raise ArgumentError(
                    "State dictionary contains the wrong number of slots for one of the phases."
                )
            else:
                setattr(self, f"_next_{phase}_slots", state[phase])

    def schedule_feature(self, feature: Feature) -> FeatureSprintSpans:
        ux_start = self.get_next_ux_slot()
        ux_end = ux_start + feature.ux_estimation - 1
        conception_start = self.get_next_conception_slot(feature.ux_estimation)
        conception_end = conception_start + self.CONCEPTION_ESTIMATION - 1
        dev_start = self.get_next_dev_slot(feature.ux_estimation)
        dev_end = dev_start + feature.dev_estimation - 1

        replace_min(self._next_ux_slots, ux_end + 1)
        replace_min(self._next_conception_slots, conception_end + 1)
        replace_min(self._next_dev_slots, dev_end + 1)

        return FeatureSprintSpans(
            feature=feature.name,
            ux=SprintSpan(start=ux_start, end=ux_end),
            conception=SprintSpan(start=conception_start, end=conception_end),
            dev=SprintSpan(start=dev_start, end=dev_end),
        )

    def _get_slot_index(self, phase: str, sprint: int):
        return getattr(self, f"_next_{phase}_slots").index(sprint)

    def get_next_ux_slot(self) -> int:
        return min(self._next_ux_slots)

    def get_next_conception_slot(self, ux_estimation: int) -> int:
        """Take Conception as soon as possible but not too early."""
        return max(
            # not too early before Dev, so that it does not need to be redone
            min(self._next_dev_slots)
            - self.gaps.max_gap_between_conception_and_dev
            - self.CONCEPTION_ESTIMATION,
            max(
                # in the first available conception slot…
                min(self._next_conception_slots),
                # …as long as it's after UX is done
                self.get_next_ux_slot()
                + ux_estimation
                + self.gaps.min_gap_between_ux_and_conception,
            ),
        )

    def get_next_dev_slot(self, ux_estimation: int) -> int:
        """Start dev in the next slot available but only if gap with conception is respected"""
        return max(
            # in the first available slot…
            min(self._next_dev_slots),
            # …as long as the conception is done
            self.get_next_conception_slot(ux_estimation)
            + self.CONCEPTION_ESTIMATION
            + self.gaps.min_gap_between_conception_and_dev,
        )
