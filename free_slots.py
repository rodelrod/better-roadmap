import logging

from feature import Feature
from parameters import DEFAULT_PARAMETERS, Parameters, Phase, Sprint
from span import FeatureSprintSpans, SprintSpan
from utils import replace_min

log = logging.getLogger(__name__)


class ArgumentError(Exception):
    pass


class FreeSlots:
    """Keep track of the latest sprints for each phase."""

    def __init__(
        self,
        params: Parameters = DEFAULT_PARAMETERS,
        initial_state: dict[str, list[int]] = None,
    ) -> None:
        self.params = params
        if initial_state and self._state_is_valid(params, initial_state):
            self._next_slots = initial_state
        else:
            self._next_slots = {}
            for phase in params.phases:
                self._next_slots[phase.name] = [1] * phase.max_concurrency

    @staticmethod
    def _state_is_valid(params: Parameters, state: dict[str, list[int]]) -> bool:
        for phase in params.phases:
            if len(state.get(phase.name, [])) != phase.max_concurrency:
                log.warning(
                    f"Initial state malformed: '{phase.name}' has {len(state.get(phase.name, []))}"
                    f" slots instead of {phase.max_concurrency}."
                )
                return False
        return True

    def schedule_feature(self, feature: Feature) -> FeatureSprintSpans:
        ux_start = self.get_next_ux_slot()
        ux_end = ux_start + feature.estimations["ux"] - 1
        conception_start = self.get_next_conception_slot(feature)
        conception_end = conception_start + feature.estimations.get("conception", 1) - 1
        dev_start = self.get_next_dev_slot(feature)
        dev_end = dev_start + feature.estimations["dev"] - 1

        replace_min(self._next_slots["ux"], ux_end + 1)
        replace_min(self._next_slots["conception"], conception_end + 1)
        replace_min(self._next_slots["dev"], dev_end + 1)

        return FeatureSprintSpans(
            feature=feature.name,
            ux=SprintSpan(start=ux_start, end=ux_end),
            conception=SprintSpan(start=conception_start, end=conception_end),
            dev=SprintSpan(start=dev_start, end=dev_end),
        )

    def _get_slot_index(self, phase: str, sprint: int):
        return getattr(self, f"_next_{phase}_slots").index(sprint)

    def get_next_ux_slot(self) -> int:
        return min(self._next_slots["ux"])

    def get_next_conception_slot(self, feature: Feature) -> int:
        """Take Conception as soon as possible but not too early."""
        conception_params = Phase("conception", 2, 0, 3)
        for phase in self.params.phases:
            if phase.name == "conception":
                conception_params = phase
                break
        return max(
            # not too early before Dev, so that it does not need to be redone
            min(self._next_slots["dev"])
            - (conception_params.max_gap_after or 0)
            - feature.estimations.get("conception", 1),
            max(
                # in the first available conception slot…
                min(self._next_slots["conception"]),
                # …as long as it's after UX is done
                self.get_next_ux_slot()
                + feature.estimations["ux"]
                + conception_params.min_gap_before,
            ),
        )

    def get_next_dev_slot(self, feature: Feature) -> int:
        """Start dev in the next slot available but only if gap with conception is respected"""
        dev_params = Phase("dev", 2, 1)
        for phase in self.params.phases:
            if phase.name == "dev":
                dev_params = phase
                break
        return max(
            # in the first available slot…
            min(self._next_slots["dev"]),
            # …as long as the conception is done
            self.get_next_conception_slot(feature)
            + feature.estimations.get("conception", 1)
            + dev_params.min_gap_before,
        )
