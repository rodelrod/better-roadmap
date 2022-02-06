from dataclasses import dataclass


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
        initial_state: dict[str, tuple] = None,
    ) -> None:
        self.max_concurrency = max_concurrency or FreeSlotsMaxConcurrency()
        self.gaps = gaps or FreeSlotsGaps()
        if not initial_state:
            self._next_ux_slots = tuple([1] * self.max_concurrency.ux)
            self._next_conception_slots = tuple([1] * self.max_concurrency.conception)
            self._next_dev_slots = tuple([1] * self.max_concurrency.dev)
        else:
            self.set_state(initial_state)

    def set_state(self, initial_state: dict[str, tuple]) -> None:
        for phase in ["ux", "conception", "dev"]:
            if len(initial_state[phase]) != getattr(self.max_concurrency, phase):
                raise ArgumentError("Initial_state is malformed")
            else:
                setattr(self, f"_next_{phase}_slots", initial_state[phase])

    def next_ux_slot(self) -> int:
        return min(self._next_ux_slots)

    def next_conception_slot(self, ux_estimation) -> int:
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
                self.next_ux_slot()
                + ux_estimation
                + self.gaps.min_gap_between_ux_and_conception,
            ),
        )

    def next_dev_slot(self, ux_estimation) -> int:
        """Start dev in the next slot available but only if gap with conception is respected"""
        return max(
            # in the first available slot…
            min(self._next_dev_slots),
            # …as long as the conception is done
            self.next_conception_slot(ux_estimation)
            + self.CONCEPTION_ESTIMATION
            + self.gaps.min_gap_between_conception_and_dev,
        )
