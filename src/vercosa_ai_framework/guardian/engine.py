"""Guardian Engine MVP.

This module evaluates mission text and planned actions only. It never executes
commands, calls external APIs, or inspects the host outside the provided input.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from vercosa_ai_framework.guardian.policies import GuardianEvaluationContext
from vercosa_ai_framework.guardian.types import (
    GuardianAction,
    GuardianDecision,
    GuardianMode,
    GuardianRiskLevel,
    GuardianSeverity,
    GuardianViolation,
)


SPEC_REF = "specs/framework/0005-guardian-engine.md"


@dataclass(frozen=True, slots=True)
class GuardianRuleMatch:
    """Internal rule match used to aggregate a final Guardian decision."""

    policy_id: str
    action: GuardianAction
    severity: GuardianSeverity
    message: str
    target_ref: str
    safe_alternative: str = "Revise a acao e solicite aprovacao explicita com escopo limitado."
    redaction: str | None = None


class GuardianEngine:
    """Deterministic, side-effect-free Guardian Engine MVP."""

    _dangerous_command_patterns: tuple[tuple[str, re.Pattern[str], str], ...] = (
        (
            "security.block.rm_root",
            re.compile(r"(?:^|[;&|\s])rm\s+(?:-[^\n;|&]*[rf][^\n;|&]*\s+|[^\n;|&]*\s+-[^\n;|&]*[rf][^\n;|&]*\s+)(?:--\s+)?(?:/(?:\s|$|\*)|~(?:\s|$|/)|\.git(?:\s|$|/))", re.I),
            "destruicao ampla de arquivos ou diretorios",
        ),
        (
            "security.block.mkfs",
            re.compile(r"(?:^|[;&|\s])mkfs(?:\.[\w-]+)?\b", re.I),
            "formatacao de dispositivo detectada",
        ),
        (
            "security.block.dd_destructive",
            re.compile(r"(?:^|[;&|\s])dd\b(?=[^\n;|&]*(?:\bof=/dev/|\bif=/dev/zero\b|\bif=/dev/random\b))", re.I),
            "uso destrutivo provavel de dd detectado",
        ),
        (
            "security.block.poweroff",
            re.compile(r"(?:^|[;&|\s])(?:shutdown|reboot|poweroff|halt)\b", re.I),
            "comando de desligamento ou reinicializacao detectado",
        ),
    )

    _sudo_pattern = re.compile(r"(?:^|[;&|\s])sudo(?:\s|$)", re.I)
    _global_config_patterns: tuple[re.Pattern[str], ...] = (
        re.compile(r"(?:^|\s)(?:/etc/|/usr/(?:local/)?(?:bin|sbin|lib|share)/|/var/lib/|/boot/)", re.I),
        re.compile(r"(?:^|\s)(?:~|\$HOME)/\.config/", re.I),
        re.compile(r"\bgit\s+config\s+--global\b", re.I),
        re.compile(r"\bnpm\s+config\s+(?:set|delete|rm)\b.*\s-g(?:\s|$)", re.I),
    )
    _secret_patterns: tuple[tuple[str, re.Pattern[str]], ...] = (
        ("security.secret.private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
        ("security.secret.aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
        ("security.secret.assignment", re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password|passwd|pwd)\s*[:=]\s*['\"]?[^\s'\"]{8,}")),
        ("security.secret.connection_string", re.compile(r"(?i)\b(?:postgres|postgresql|mysql|mongodb|redis)://[^\s]+:[^\s]+@")),
        ("security.secret.env_file", re.compile(r"(?:^|[\s/])\.env(?:\b|[\s./_-])", re.I)),
    )

    def evaluate(self, context: GuardianEvaluationContext) -> GuardianDecision:
        """Evaluate a mission or action context and return a policy decision."""

        matches: list[GuardianRuleMatch] = []
        mission_text = self._combined_mission_text(context)
        command = context.planned_command or ""
        action_text = self._combined_action_text(context)

        matches.extend(self._validate_mission(context, mission_text))
        matches.extend(self._detect_dangerous_commands(command))
        matches.extend(self._detect_secrets(mission_text, "mission_goal"))
        matches.extend(self._detect_secrets(action_text, "requested_action"))
        matches.extend(self._detect_sudo(command, context.guardian_mode))
        matches.extend(self._detect_global_config(action_text, context.guardian_mode))

        return self._decision_from_matches(context, matches)

    def validate_mission_text(
        self,
        mission_text: str,
        *,
        mission_id: str = "mission",
        guardian_mode: GuardianMode = GuardianMode.STANDARD,
        spec_refs: tuple[str, ...] = (),
        metadata: dict[str, object] | None = None,
    ) -> GuardianDecision:
        """Convenience API for pre-execution validation of raw mission text."""

        context = GuardianEvaluationContext(
            mission_id=mission_id,
            evaluation_type="mission_pre_execution",
            guardian_mode=guardian_mode,
            mission_goal=mission_text,
            spec_refs=spec_refs,
            metadata=metadata or {},
        )
        return self.evaluate(context)

    def _validate_mission(self, context: GuardianEvaluationContext, mission_text: str) -> list[GuardianRuleMatch]:
        matches: list[GuardianRuleMatch] = []
        normalized = mission_text.strip()
        if not normalized:
            return [
                GuardianRuleMatch(
                    policy_id="mission.requires_goal",
                    action=GuardianAction.BLOCK,
                    severity=GuardianSeverity.HIGH,
                    message="missao sem objetivo claro",
                    target_ref="mission_goal",
                    safe_alternative="Informe objetivo, entregaveis, restricoes e criterios de aceite.",
                )
            ]

        lower = normalized.lower()
        requires_implementation = any(word in lower for word in ("implementar", "implementation", "codigo", "code", "mvp"))
        if requires_implementation and not context.spec_refs:
            matches.append(
                GuardianRuleMatch(
                    policy_id="mission.requires_spec",
                    action=self._ambiguous_action(context.guardian_mode),
                    severity=GuardianSeverity.HIGH,
                    message="missao de implementacao sem referencia de Spec",
                    target_ref="spec_refs",
                    safe_alternative="Inclua a Spec aprovada que governa a implementacao.",
                )
            )

        required_markers = {
            "mission.requires_deliverables": ("entregavel", "deliverable", "entregáveis", "entregaveis"),
            "mission.requires_acceptance_criteria": ("criterio de aceite", "critérios de aceite", "criterios de aceite", "acceptance"),
        }
        for policy_id, markers in required_markers.items():
            metadata_key = "deliverables" if "deliverables" in policy_id else "acceptance_criteria"
            has_metadata = bool(context.metadata.get(metadata_key))
            if not has_metadata and not any(marker in lower for marker in markers):
                matches.append(
                    GuardianRuleMatch(
                        policy_id=policy_id,
                        action=self._mission_validation_action(context.guardian_mode),
                        severity=GuardianSeverity.MEDIUM,
                        message="missao sem campo minimo de validacao pre-execucao",
                        target_ref="mission_goal",
                        safe_alternative="Declare entregaveis e criterios de aceite proporcionais ao risco.",
                    )
                )
        return matches

    def _detect_dangerous_commands(self, command: str) -> list[GuardianRuleMatch]:
        if not command:
            return []
        matches = []
        for policy_id, pattern, message in self._dangerous_command_patterns:
            if pattern.search(command):
                matches.append(
                    GuardianRuleMatch(
                        policy_id=policy_id,
                        action=GuardianAction.BLOCK,
                        severity=GuardianSeverity.CRITICAL,
                        message=message,
                        target_ref="planned_command",
                        safe_alternative="Use uma acao reversivel, limitada ao workspace e validada por adapter autorizado.",
                    )
                )
        return matches

    def _detect_sudo(self, command: str, mode: GuardianMode) -> list[GuardianRuleMatch]:
        if not command or not self._sudo_pattern.search(command):
            return []
        action = {
            GuardianMode.STRICT: GuardianAction.BLOCK,
            GuardianMode.STANDARD: GuardianAction.REQUIRE_APPROVAL,
            GuardianMode.PERMISSIVE: GuardianAction.WARN,
        }[mode]
        return [
            GuardianRuleMatch(
                policy_id="security.sudo",
                action=action,
                severity=GuardianSeverity.CRITICAL if mode == GuardianMode.STRICT else GuardianSeverity.HIGH,
                message="execucao privilegiada com sudo detectada",
                target_ref="planned_command",
                safe_alternative="Prefira uma alternativa sem sudo ou solicite aprovacao explicita com justificativa.",
            )
        ]

    def _detect_global_config(self, text: str, mode: GuardianMode) -> list[GuardianRuleMatch]:
        if not text or not any(pattern.search(text) for pattern in self._global_config_patterns):
            return []
        action = {
            GuardianMode.STRICT: GuardianAction.BLOCK,
            GuardianMode.STANDARD: GuardianAction.REQUIRE_APPROVAL,
            GuardianMode.PERMISSIVE: GuardianAction.WARN,
        }[mode]
        return [
            GuardianRuleMatch(
                policy_id="security.global_config",
                action=action,
                severity=GuardianSeverity.HIGH,
                message="alteracao provavel de configuracao global detectada",
                target_ref="target_paths",
                safe_alternative="Restrinja a mudanca ao workspace ou use configuracao local do projeto.",
            )
        ]

    def _detect_secrets(self, text: str, target_ref: str) -> list[GuardianRuleMatch]:
        if not text:
            return []
        matches = []
        for policy_id, pattern in self._secret_patterns:
            if pattern.search(text):
                matches.append(
                    GuardianRuleMatch(
                        policy_id=policy_id,
                        action=GuardianAction.BLOCK,
                        severity=GuardianSeverity.CRITICAL,
                        message="presenca provavel de segredo detectada",
                        target_ref=target_ref,
                        safe_alternative="Remova ou masque o segredo antes de prosseguir.",
                        redaction="secret_value",
                    )
                )
        return matches

    def _decision_from_matches(self, context: GuardianEvaluationContext, matches: list[GuardianRuleMatch]) -> GuardianDecision:
        if not matches:
            return GuardianDecision(
                mission_id=context.mission_id,
                evaluation_id=context.evaluation_id or context.mission_id,
                decision=GuardianAction.ALLOW,
                risk_level=GuardianRiskLevel.LOW,
                guardian_mode=context.guardian_mode,
                matched_policies=("guardian.mvp",),
                reasons=("nenhuma politica bloqueante ou sensivel detectada",),
            )

        decision = self._most_restrictive(match.action for match in matches)
        risk_level = self._risk_from_matches(matches)
        violations = tuple(
            GuardianViolation(
                policy_id=match.policy_id,
                severity=match.severity,
                message=match.message,
                action=match.action,
                target_refs=(match.target_ref,),
                evidence_refs=(SPEC_REF,),
                redactions_applied=(match.redaction,) if match.redaction else (),
            )
            for match in matches
        )
        return GuardianDecision(
            mission_id=context.mission_id,
            evaluation_id=context.evaluation_id or context.mission_id,
            decision=decision,
            risk_level=risk_level,
            guardian_mode=context.guardian_mode,
            matched_policies=tuple(dict.fromkeys(match.policy_id for match in matches)),
            violations=violations,
            reasons=tuple(dict.fromkeys(match.message for match in matches)),
            required_actions=self._required_actions(matches),
            approval_requirements=tuple(match.message for match in matches if match.action == GuardianAction.REQUIRE_APPROVAL),
            blocked_items=tuple(match.target_ref for match in matches if match.action == GuardianAction.BLOCK),
            warnings=tuple(match.message for match in matches if match.action == GuardianAction.WARN),
            safe_alternatives=tuple(dict.fromkeys(match.safe_alternative for match in matches)),
            redactions_applied=tuple(dict.fromkeys(match.redaction for match in matches if match.redaction)),
        )

    def _combined_mission_text(self, context: GuardianEvaluationContext) -> str:
        return "\n".join(part for part in (context.mission_goal, context.requested_action or "") if part)

    def _combined_action_text(self, context: GuardianEvaluationContext) -> str:
        return "\n".join(
            part
            for part in (
                context.requested_action or "",
                context.planned_command or "",
                "\n".join(context.target_paths),
            )
            if part
        )

    def _mission_validation_action(self, mode: GuardianMode) -> GuardianAction:
        if mode == GuardianMode.STRICT:
            return GuardianAction.REQUIRE_APPROVAL
        return GuardianAction.WARN

    def _ambiguous_action(self, mode: GuardianMode) -> GuardianAction:
        if mode == GuardianMode.STRICT:
            return GuardianAction.BLOCK
        return GuardianAction.REQUIRE_APPROVAL

    def _most_restrictive(self, actions: object) -> GuardianAction:
        rank = {
            GuardianAction.ALLOW: 0,
            GuardianAction.WARN: 1,
            GuardianAction.REQUIRE_APPROVAL: 2,
            GuardianAction.BLOCK: 3,
        }
        return max(actions, key=lambda action: rank[action])

    def _risk_from_matches(self, matches: list[GuardianRuleMatch]) -> GuardianRiskLevel:
        rank = {
            GuardianSeverity.LOW: GuardianRiskLevel.LOW,
            GuardianSeverity.MEDIUM: GuardianRiskLevel.MEDIUM,
            GuardianSeverity.HIGH: GuardianRiskLevel.HIGH,
            GuardianSeverity.CRITICAL: GuardianRiskLevel.CRITICAL,
        }
        severity_order = {
            GuardianSeverity.LOW: 0,
            GuardianSeverity.MEDIUM: 1,
            GuardianSeverity.HIGH: 2,
            GuardianSeverity.CRITICAL: 3,
        }
        highest = max((match.severity for match in matches), key=lambda severity: severity_order[severity])
        return rank[highest]

    def _required_actions(self, matches: list[GuardianRuleMatch]) -> tuple[str, ...]:
        actions = []
        if any(match.action == GuardianAction.BLOCK for match in matches):
            actions.append("interromper a acao bloqueada")
        if any(match.action == GuardianAction.REQUIRE_APPROVAL for match in matches):
            actions.append("obter aprovacao explicita antes de prosseguir")
        if any(match.redaction for match in matches):
            actions.append("mascarar ou remover segredos detectados")
        return tuple(actions)


__all__ = ["GuardianEngine"]
