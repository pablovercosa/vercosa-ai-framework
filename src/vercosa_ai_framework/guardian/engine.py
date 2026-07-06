"""Guardian Engine MVP.

This module evaluates mission text and planned actions only. It never executes
commands, calls external APIs, or inspects the host outside the provided input.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from vercosa_ai_framework.context import (
    ContextItem,
    ContextItemType,
    ContextOmissionReason,
    ContextPackage,
    ContextRiskLevel,
    ContextSource,
    ContextSourceType,
)
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

    def evaluate_context_package(
        self,
        package: ContextPackage,
        *,
        mission_id: str | None = None,
        guardian_mode: GuardianMode = GuardianMode.STANDARD,
        evaluation_id: str | None = None,
    ) -> GuardianDecision:
        """Evaluate operational risk in a Context Package without side effects."""

        context = GuardianEvaluationContext(
            mission_id=mission_id or package.metadata.get("mission_id") or package.request_id,
            evaluation_id=evaluation_id or package.context_package_id,
            evaluation_type="context_package_pre_delivery",
            guardian_mode=guardian_mode,
            mission_goal=package.request_goal,
            spec_refs=("specs/framework/0005-guardian-engine.md", "specs/framework/0014-context-router-token-budget-memory.md"),
            metadata={"context_package_id": package.context_package_id, "request_id": package.request_id},
        )
        matches: list[GuardianRuleMatch] = []
        sources_by_id = {source.source_id: source for source in package.sources}

        matches.extend(self._validate_context_package_traceability(package, sources_by_id))
        matches.extend(self._validate_context_package_sources(package, sources_by_id))
        matches.extend(self._validate_context_package_warnings(package))
        matches.extend(self._validate_context_package_redactions(package))
        matches.extend(self._validate_context_package_budget(package))
        matches.extend(self._validate_context_package_sensitivity(package, sources_by_id))
        matches.extend(self._validate_context_package_omissions(package))

        if not matches:
            return GuardianDecision(
                mission_id=context.mission_id,
                evaluation_id=context.evaluation_id or package.context_package_id,
                decision=GuardianAction.ALLOW,
                risk_level=GuardianRiskLevel.LOW,
                guardian_mode=context.guardian_mode,
                matched_policies=("context_package.deterministic_checks",),
                reasons=("context package sem riscos deterministicos relevantes",),
                limits_applied={
                    "estimated_context_tokens": package.token_estimate.estimated_tokens,
                    "reserved_output_tokens": package.output_token_reservation,
                },
                metadata=context.metadata,
            )

        decision = self._decision_from_matches(context, matches)
        return GuardianDecision(
            mission_id=decision.mission_id,
            evaluation_id=decision.evaluation_id,
            decision=decision.decision,
            risk_level=decision.risk_level,
            guardian_mode=decision.guardian_mode,
            matched_policies=decision.matched_policies,
            violations=decision.violations,
            reasons=decision.reasons,
            required_actions=decision.required_actions,
            approval_requirements=decision.approval_requirements,
            blocked_items=decision.blocked_items,
            warnings=decision.warnings,
            safe_alternatives=decision.safe_alternatives,
            limits_applied={
                "estimated_context_tokens": package.token_estimate.estimated_tokens,
                "reserved_output_tokens": package.output_token_reservation,
            },
            redactions_applied=decision.redactions_applied,
            metadata=context.metadata,
        )

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

    def _validate_context_package_traceability(
        self,
        package: ContextPackage,
        sources_by_id: dict[str, ContextSource],
    ) -> list[GuardianRuleMatch]:
        matches: list[GuardianRuleMatch] = []
        if not package.content_hash:
            matches.append(
                GuardianRuleMatch(
                    policy_id="context.traceability.package_hash_missing",
                    action=GuardianAction.REQUIRE_APPROVAL,
                    severity=GuardianSeverity.HIGH,
                    message="context package sem hash de conteudo rastreavel",
                    target_ref=package.context_package_id,
                    safe_alternative="Regere o pacote com hash de conteudo antes da entrega.",
                )
            )

        for item in package.items:
            if item.source_ref not in sources_by_id:
                matches.append(
                    GuardianRuleMatch(
                        policy_id="context.traceability.source_ref_missing",
                        action=GuardianAction.WARN,
                        severity=GuardianSeverity.MEDIUM,
                        message="item de contexto referencia fonte ausente no pacote",
                        target_ref=item.context_item_id,
                        safe_alternative="Inclua a fonte correspondente ou remova o item do pacote.",
                    )
                )
            if _context_item_requires_traceability(item) and not item.citations and not item.content_ref:
                matches.append(
                    GuardianRuleMatch(
                        policy_id="context.traceability.item_citation_missing",
                        action=GuardianAction.REQUIRE_APPROVAL if item.item_type is ContextItemType.EVIDENCE else GuardianAction.WARN,
                        severity=GuardianSeverity.HIGH if item.item_type is ContextItemType.EVIDENCE else GuardianSeverity.MEDIUM,
                        message="item de contexto sem citacao ou referencia rastreavel",
                        target_ref=item.context_item_id,
                        safe_alternative="Inclua citacao auditavel, content_ref ou omita o item.",
                    )
                )
            if item.content and not item.content_hash:
                matches.append(
                    GuardianRuleMatch(
                        policy_id="context.traceability.item_hash_missing",
                        action=GuardianAction.WARN,
                        severity=GuardianSeverity.MEDIUM,
                        message="item de contexto com conteudo sem hash rastreavel",
                        target_ref=item.context_item_id,
                        safe_alternative="Regere o item com hash de conteudo.",
                    )
                )

        for citation in package.citations:
            has_reference = any((citation.document_id, citation.canonical_uri, citation.source_uri, citation.path, citation.chunk_id))
            if not has_reference:
                matches.append(
                    GuardianRuleMatch(
                        policy_id="context.traceability.citation_reference_missing",
                        action=GuardianAction.WARN,
                        severity=GuardianSeverity.MEDIUM,
                        message="citacao sem referencia auditavel de origem",
                        target_ref=citation.citation_id,
                        safe_alternative="Inclua document_id, URI, path ou chunk_id na citacao.",
                    )
                )
        return matches

    def _validate_context_package_sources(
        self,
        package: ContextPackage,
        sources_by_id: dict[str, ContextSource],
    ) -> list[GuardianRuleMatch]:
        matches: list[GuardianRuleMatch] = []
        for source in package.sources:
            trust = source.trust_level.lower()
            if source.source_type is ContextSourceType.UNKNOWN or trust in {"unknown", "low"}:
                matches.append(
                    GuardianRuleMatch(
                        policy_id="context.source.unknown_or_low_trust",
                        action=GuardianAction.WARN,
                        severity=GuardianSeverity.MEDIUM,
                        message="fonte de contexto desconhecida ou pouco confiavel",
                        target_ref=source.source_id,
                        safe_alternative="Prefira fonte canonica, Spec, ADR ou documento com nivel de confianca conhecido.",
                    )
                )
            if trust in {"untrusted", "blocked"}:
                matches.append(
                    GuardianRuleMatch(
                        policy_id="context.source.untrusted",
                        action=GuardianAction.REQUIRE_APPROVAL,
                        severity=GuardianSeverity.HIGH,
                        message="fonte de contexto marcada como nao confiavel",
                        target_ref=source.source_id,
                        safe_alternative="Revise a fonte manualmente ou substitua por fonte confiavel.",
                    )
                )

        for item in package.items:
            if item.trust_level.lower() in {"untrusted", "blocked"} or item.is_untrusted_data and item.source_ref not in sources_by_id:
                matches.append(
                    GuardianRuleMatch(
                        policy_id="context.item.untrusted",
                        action=GuardianAction.REQUIRE_APPROVAL,
                        severity=GuardianSeverity.HIGH,
                        message="item de contexto marcado como nao confiavel",
                        target_ref=item.context_item_id,
                        safe_alternative="Trate o item como dado nao confiavel e revise antes da entrega.",
                    )
                )
        return matches

    def _validate_context_package_warnings(self, package: ContextPackage) -> list[GuardianRuleMatch]:
        return [
            GuardianRuleMatch(
                policy_id="context.package.warning_present",
                action=GuardianAction.WARN,
                severity=GuardianSeverity.MEDIUM,
                message="context package contem warning relevante",
                target_ref=warning,
                safe_alternative="Revise o warning antes de reutilizar ou entregar o pacote.",
            )
            for warning in package.warnings
        ]

    def _validate_context_package_redactions(self, package: ContextPackage) -> list[GuardianRuleMatch]:
        matches: list[GuardianRuleMatch] = []
        for redaction in package.redactions:
            text = " ".join(
                str(part).lower()
                for part in (redaction.redaction_type, redaction.reason, redaction.metadata.get("status", ""), redaction.metadata.get("state", ""))
            )
            if any(marker in text for marker in ("pending", "suspect", "suspeit", "incomplete", "failed")):
                matches.append(
                    GuardianRuleMatch(
                        policy_id="context.redaction.pending_or_suspicious",
                        action=GuardianAction.REQUIRE_APPROVAL,
                        severity=GuardianSeverity.HIGH,
                        message="redaction pendente ou suspeita detectada no contexto",
                        target_ref=redaction.redaction_id,
                        safe_alternative="Conclua ou revise a redaction antes de entregar o pacote.",
                        redaction=redaction.redaction_id,
                    )
                )
        return matches

    def _validate_context_package_budget(self, package: ContextPackage) -> list[GuardianRuleMatch]:
        matches: list[GuardianRuleMatch] = []
        available = _metadata_int(package.metadata.get("available_context_tokens"))
        used = _metadata_int(package.metadata.get("used_context_tokens"))
        estimated = package.token_estimate.estimated_tokens
        model_estimated = _metadata_int(package.model_requirements.get("estimated_context_tokens"))
        minimum_window = _metadata_int(package.model_requirements.get("minimum_context_window"))

        if available is not None and estimated > available:
            matches.append(
                GuardianRuleMatch(
                    policy_id="context.budget.exceeded",
                    action=GuardianAction.BLOCK,
                    severity=GuardianSeverity.CRITICAL,
                    message="orcamento de tokens do contexto foi excedido",
                    target_ref=package.context_package_id,
                    safe_alternative="Reduza ou omita itens antes de entregar o pacote.",
                )
            )
        if used is not None and used != estimated:
            matches.append(
                GuardianRuleMatch(
                    policy_id="context.budget.inconsistent_used_tokens",
                    action=GuardianAction.WARN,
                    severity=GuardianSeverity.MEDIUM,
                    message="orcamento de tokens inconsistente com estimativa do pacote",
                    target_ref=package.context_package_id,
                    safe_alternative="Recalcule o pacote com estimativas consistentes.",
                )
            )
        if model_estimated is not None and model_estimated != estimated:
            matches.append(
                GuardianRuleMatch(
                    policy_id="context.budget.inconsistent_model_requirements",
                    action=GuardianAction.WARN,
                    severity=GuardianSeverity.MEDIUM,
                    message="requisitos de modelo divergem da estimativa de contexto",
                    target_ref=package.context_package_id,
                    safe_alternative="Sincronize model_requirements com a estimativa de tokens.",
                )
            )
        if minimum_window is not None and minimum_window < estimated + package.output_token_reservation:
            matches.append(
                GuardianRuleMatch(
                    policy_id="context.budget.minimum_window_inconsistent",
                    action=GuardianAction.REQUIRE_APPROVAL,
                    severity=GuardianSeverity.HIGH,
                    message="janela minima de contexto menor que tokens estimados e reserva de output",
                    target_ref=package.context_package_id,
                    safe_alternative="Ajuste a janela minima ou reduza o pacote antes da entrega.",
                )
            )
        return matches

    def _validate_context_package_sensitivity(
        self,
        package: ContextPackage,
        sources_by_id: dict[str, ContextSource],
    ) -> list[GuardianRuleMatch]:
        matches: list[GuardianRuleMatch] = []
        for source in package.sources:
            matches.extend(_sensitivity_match("context.source.sensitive", source.source_id, source.sensitivity))
        for item in package.items:
            matches.extend(_sensitivity_match("context.item.sensitive", item.context_item_id, item.sensitivity))
            if item.risk_level in {ContextRiskLevel.HIGH, ContextRiskLevel.CRITICAL}:
                matches.append(
                    GuardianRuleMatch(
                        policy_id="context.item.high_risk",
                        action=GuardianAction.REQUIRE_APPROVAL if item.risk_level is ContextRiskLevel.HIGH else GuardianAction.BLOCK,
                        severity=GuardianSeverity.HIGH if item.risk_level is ContextRiskLevel.HIGH else GuardianSeverity.CRITICAL,
                        message="item de contexto possui risco alto ou critico",
                        target_ref=item.context_item_id,
                        safe_alternative="Revise o item e sua necessidade antes da entrega.",
                    )
                )
            source = sources_by_id.get(item.source_ref)
            if source is not None and source.sensitivity != "public" and item.sensitivity == "public":
                matches.append(
                    GuardianRuleMatch(
                        policy_id="context.sensitivity.inconsistent",
                        action=GuardianAction.WARN,
                        severity=GuardianSeverity.MEDIUM,
                        message="sensibilidade do item diverge da sensibilidade da fonte",
                        target_ref=item.context_item_id,
                        safe_alternative="Classifique item e fonte com sensibilidade coerente.",
                    )
                )
        return matches

    def _validate_context_package_omissions(self, package: ContextPackage) -> list[GuardianRuleMatch]:
        critical_reasons = {
            ContextOmissionReason.GUARDIAN_BLOCKED: (GuardianAction.BLOCK, GuardianSeverity.CRITICAL),
            ContextOmissionReason.PROMPT_INJECTION_RISK: (GuardianAction.BLOCK, GuardianSeverity.CRITICAL),
            ContextOmissionReason.POLICY_DENIED: (GuardianAction.REQUIRE_APPROVAL, GuardianSeverity.HIGH),
            ContextOmissionReason.REQUIRES_APPROVAL: (GuardianAction.REQUIRE_APPROVAL, GuardianSeverity.HIGH),
            ContextOmissionReason.SENSITIVITY_DENIED: (GuardianAction.REQUIRE_APPROVAL, GuardianSeverity.HIGH),
            ContextOmissionReason.UNTRUSTED_SOURCE: (GuardianAction.REQUIRE_APPROVAL, GuardianSeverity.HIGH),
        }
        matches: list[GuardianRuleMatch] = []
        for omission in package.omission_reasons:
            if omission.omission_reason in critical_reasons:
                action, severity = critical_reasons[omission.omission_reason]
                matches.append(
                    GuardianRuleMatch(
                        policy_id=f"context.omission.{omission.omission_reason.value}",
                        action=action,
                        severity=severity,
                        message="context package contem omission reason critico",
                        target_ref=omission.item_ref,
                        safe_alternative="Replaneje o pacote respeitando a omissao critica registrada.",
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


def _context_item_requires_traceability(item: ContextItem) -> bool:
    return item.item_type in {ContextItemType.EXCERPT, ContextItemType.SUMMARY, ContextItemType.EVIDENCE}


def _metadata_int(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None


def _sensitivity_match(policy_id: str, target_ref: str, sensitivity: str) -> list[GuardianRuleMatch]:
    normalized = sensitivity.lower()
    if normalized in {"public", "internal", ""}:
        return []
    if normalized in {"secret", "credential", "credentials"}:
        return [
            GuardianRuleMatch(
                policy_id=policy_id,
                action=GuardianAction.BLOCK,
                severity=GuardianSeverity.CRITICAL,
                message="conteudo de contexto marcado como segredo ou credencial",
                target_ref=target_ref,
                safe_alternative="Remova, masque ou mantenha o dado fora do pacote de contexto.",
                redaction="sensitive_context",
            )
        ]
    return [
        GuardianRuleMatch(
            policy_id=policy_id,
            action=GuardianAction.REQUIRE_APPROVAL,
            severity=GuardianSeverity.HIGH,
            message="conteudo de contexto marcado como sensivel",
            target_ref=target_ref,
            safe_alternative="Revise politica de privacidade e aprove explicitamente antes da entrega.",
        )
    ]


__all__ = ["GuardianEngine"]
