import logging
from datetime import datetime
from sys import maxsize
from typing import Union

from .actuals import ActualFeature
from .features import Feature
from .parameters import Phase
from .span import FeatureDateSpans, FeatureSprintSpans, SprintSpan, GraphSegment
from ..utils import replace_min

log = logging.getLogger(__name__)


class ConfigurationError(Exception):
    pass


class FeatureScheduler:
    """Keep track of the latest sprints for each phase."""

    def __init__(
        self,
        phases: list[Phase],
        initial_state: dict[str, list[int]] = None,
    ) -> None:
        self.phases = phases
        if initial_state and self._state_is_valid(phases, initial_state):
            self._next_slots = initial_state
        else:
            self._next_slots = {}
            for phase in phases:
                self._next_slots[phase.name] = [1] * phase.max_concurrency

    @staticmethod
    def _state_is_valid(phases: list[Phase], state: dict[str, list[int]]) -> bool:
        for phase in phases:
            if len(state.get(phase.name, [])) != phase.max_concurrency:
                log.warning(
                    f"Initial state malformed: '{phase.name}' has "
                    f"{len(state.get(phase.name, []))} slots "
                    f"instead of {phase.max_concurrency}."
                )
                return False
        return True

    def schedule_feature_as_dates(
        self, feature: Union[Feature, ActualFeature], project_start: datetime
    ) -> list[GraphSegment]:
        if isinstance(feature, Feature):
            feature_sprint_spans = self._schedule_feature_as_sprints(feature)
        else:
            feature_sprint_spans = FeatureSprintSpans.from_actual_feature(feature)
        feature_date_spans = FeatureDateSpans.from_feature_sprint_spans(
            feature_sprint_spans, project_start=project_start
        )
        return feature_date_spans.get_graph_segments()

    def _sprint_to_date_spans(
        self, feature_sprint_spans: FeatureSprintSpans, project_start: datetime
    ):
        return FeatureDateSpans.from_feature_sprint_spans(
            feature_sprint_spans, project_start
        )

    def _schedule_feature_as_sprints(self, feature: Feature) -> FeatureSprintSpans:
        sprint_spans, _ = self._schedule_phase(feature, self.phases, 0)

        for sprint_span in sprint_spans:
            replace_min(self._next_slots[sprint_span.phase], sprint_span.end + 1)

        return FeatureSprintSpans(feature=feature.name, spans=sprint_spans)

    def _schedule_phase(
        self,
        feature: Feature,
        phase_list: list[Phase],
        prev_end: int,
        no_phases_scheduled: bool = True,
    ) -> tuple[list[SprintSpan], int]:
        if not phase_list:
            return ([], maxsize)
        cur_phase, next_phases = phase_list[0], phase_list[1:]
        estimation = self._get_estimation(feature, cur_phase)
        phase_name = cur_phase.name
        min_available_slot = min(self._next_slots[phase_name])
        if no_phases_scheduled:
            min_start = max(prev_end + 1, min_available_slot)
        else:
            min_start = max(prev_end + cur_phase.min_gap_before + 1, min_available_slot)
        min_end = min_start + estimation - 1
        still_no_phases_scheduled = (estimation == 0) and no_phases_scheduled
        next_sprint_spans, next_start = self._schedule_phase(
            feature, next_phases, min_end, still_no_phases_scheduled
        )
        if cur_phase.max_gap_after:
            end = max(min_end, next_start - cur_phase.max_gap_after)
        else:
            end = min_end
        start = end - estimation + 1
        if estimation == 0:
            return (next_sprint_spans, start)
        return ([SprintSpan(phase_name, start, end)] + next_sprint_spans, start)

    def _get_estimation(self, feature: Feature, phase: Phase) -> int:
        if phase.name in feature.estimations:
            return feature.estimations[phase.name]
        if phase.default_estimation is not None:
            return phase.default_estimation
        raise ConfigurationError(
            f"Could not find an estimation for phase '{phase.name}'"
            f" in feature '{feature.name}'."
        )
