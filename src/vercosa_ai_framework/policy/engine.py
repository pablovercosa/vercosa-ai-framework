"""Deterministic Policy Engine MVP.

The implementation resolves explicit in-memory policy sets only. It does not
call Guardian Engine, LLMs, providers, databases, network services, MCPs, or
runtime adapters.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from vercosa_ai_framework.policy.types import (
    PolicyConflict,
    PolicyEngine,
    PolicyEvaluationContext,
    PolicyResolutionResult,
    PolicyRule,
    PolicyScope,
    PolicySet,
    PolicySeverity,
    ResolvedPolicySet,
)


@dataclass(frozen=True, slots=True)
class _RuleCandidate:
    """Internal sortable rule candidate."""

    rule: PolicyRule
    policy_set: PolicySet


class DeterministicPolicyEngine(PolicyEngine):
    """Side-effect-free MVP for declarative policy resolution."""

    def resolve(
        self,
        policy_sets: tuple[PolicySet, ...] | list[PolicySet],
        context: PolicyEvaluationContext | None = None,
    ) -> PolicyResolutionResult:
        """Resolve explicit policy sets by priority and stable identifiers."""

        resolution_context = context or PolicyEvaluationContext()
        ordered_sets = tuple(
            sorted(
                (policy_set for policy_set in policy_sets if policy_set.enabled),
                key=self._policy_set_sort_key,
            )
        )
        candidates = self._collect_rule_candidates(ordered_sets, resolution_context)
        grouped: dict[tuple[str, str], list[_RuleCandidate]] = defaultdict(list)

        for candidate in candidates:
            grouped[candidate.rule.conflict_key].append(candidate)

        resolved_rules: list[PolicyRule] = []
        conflicts: list[PolicyConflict] = []
        effective_values: dict[str, object] = {}

        for group_key in sorted(grouped):
            group = sorted(grouped[group_key], key=self._rule_candidate_sort_key)
            winner = group[0]
            resolved_rules.append(winner.rule)
            effective_values[self._effective_value_key(winner.rule)] = (
                winner.rule.value if winner.rule.value is not None else winner.rule.effect.value
            )

            losing_conflicts = tuple(
                candidate.rule.rule_id for candidate in group[1:] if candidate.rule.effect_signature != winner.rule.effect_signature
            )
            if losing_conflicts:
                conflicts.append(
                    PolicyConflict(
                        key=winner.rule.key,
                        scope=winner.rule.scope,
                        winning_rule_id=winner.rule.rule_id,
                        losing_rule_ids=losing_conflicts,
                        reason="regras com mesmo escopo e chave declararam efeitos ou valores diferentes; a maior prioridade venceu",
                        severity=self._highest_severity(tuple(candidate.rule for candidate in group)),
                    )
                )

        sorted_resolved_rules = tuple(sorted(resolved_rules, key=self._rule_sort_key))
        resolved = ResolvedPolicySet(
            resolved_rules=sorted_resolved_rules,
            source_policy_set_ids=tuple(policy_set.policy_set_id for policy_set in ordered_sets),
            conflicts=tuple(conflicts),
            effective_values=effective_values,
            warnings=tuple(conflict.reason for conflict in conflicts),
        )
        return PolicyResolutionResult(
            resolved_policy_set=resolved,
            context=resolution_context,
            ordered_policy_set_ids=tuple(policy_set.policy_set_id for policy_set in ordered_sets),
            conflicts=resolved.conflicts,
            warnings=resolved.warnings,
        )

    def _collect_rule_candidates(
        self,
        ordered_sets: tuple[PolicySet, ...],
        context: PolicyEvaluationContext,
    ) -> tuple[_RuleCandidate, ...]:
        candidates: list[_RuleCandidate] = []
        for policy_set in ordered_sets:
            for rule in policy_set.rules:
                if rule.enabled and self._matches_context(rule, context):
                    candidates.append(_RuleCandidate(rule=rule, policy_set=policy_set))
        return tuple(sorted(candidates, key=self._rule_candidate_sort_key))

    def _matches_context(self, rule: PolicyRule, context: PolicyEvaluationContext) -> bool:
        requested_scopes = set(context.requested_scopes)
        if context.target_scope is not None:
            requested_scopes.add(context.target_scope)
        if requested_scopes and rule.scope not in requested_scopes and rule.scope != PolicyScope.GLOBAL:
            return False
        if context.requested_keys and rule.key not in set(context.requested_keys):
            return False
        return True

    def _policy_set_sort_key(self, policy_set: PolicySet) -> tuple[int, str, str, str, str]:
        return (-policy_set.priority, policy_set.source.value, policy_set.scope.value, policy_set.name, policy_set.policy_set_id)

    def _rule_candidate_sort_key(
        self,
        candidate: _RuleCandidate,
    ) -> tuple[int, int, str, str, str, str, str]:
        return (
            -candidate.rule.priority,
            -candidate.policy_set.priority,
            candidate.rule.source.value,
            candidate.rule.scope.value,
            candidate.rule.key,
            candidate.policy_set.policy_set_id,
            candidate.rule.rule_id,
        )

    def _rule_sort_key(self, rule: PolicyRule) -> tuple[int, str, str, str]:
        return (-rule.priority, rule.scope.value, rule.key, rule.rule_id)

    def _effective_value_key(self, rule: PolicyRule) -> str:
        return f"{rule.scope.value}.{rule.key}"

    def _highest_severity(self, rules: tuple[PolicyRule, ...]) -> PolicySeverity:
        order = {
            PolicySeverity.LOW: 0,
            PolicySeverity.MEDIUM: 1,
            PolicySeverity.HIGH: 2,
            PolicySeverity.CRITICAL: 3,
        }
        return max((rule.severity for rule in rules), key=lambda severity: order[severity])


__all__ = ["DeterministicPolicyEngine"]
