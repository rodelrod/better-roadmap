import logging

from feature import Feature
from parameters import DEFAULT_PARAMETERS, Parameters, Phase, Sprint
from span import FeatureSprintSpans, SprintSpan
from sys import maxsize
from utils import replace_min

log = logging.getLogger(__name__)


class ConfigurationError(Exception):
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
        sprint_spans, _ = self._schedule_phase(feature, self.params.phases, 0)

        for sprint_span in sprint_spans:
            replace_min(self._next_slots[sprint_span.phase], sprint_span.end + 1)

        return FeatureSprintSpans(feature=feature.name, spans=sprint_spans)

    def _schedule_phase(
        self,
        feature: Feature,
        phase_list: list[Phase],
        prev_end: int,
    ) -> tuple[list[SprintSpan], int]:
        if not phase_list:
            return ([], maxsize)
        cur_phase, next_phases = phase_list[0], phase_list[1:]
        estimation = self._get_estimation(feature, cur_phase)
        phase_name = cur_phase.name
        min_available_slot = min(self._next_slots[phase_name])
        min_start = max(prev_end + cur_phase.min_gap_before + 1, min_available_slot)
        min_end = min_start + estimation - 1
        next_sprint_spans, next_start = self._schedule_phase(
            feature, next_phases, min_end
        )
        if cur_phase.max_gap_after:
            end = max(min_end, next_start - cur_phase.max_gap_after)
        else:
            end = min_end
        start = end - estimation + 1
        return ([SprintSpan(phase_name, start, end)] + next_sprint_spans, start)

    def _get_estimation(self, feature: Feature, phase: Phase) -> int:
        if phase.name in feature.estimations:
            return feature.estimations[phase.name]
        if phase.default_estimation:
            return phase.default_estimation
        raise ConfigurationError(
            f"Could not find an estimation for phase '{phase.name}'"
            f" in feature '{feature.name}'."
        )
