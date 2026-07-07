import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_run_one_mission_auto_commit_uses_pt_br_default_and_custom_message():
    script = (ROOT / "scripts" / "vaf-run-one-mission.sh").read_text(encoding="utf-8")

    assert 'COMMIT_MESSAGE="${VAF_COMMIT_MESSAGE:-}"' in script
    assert 'COMMIT_MESSAGE="missão: ${NAME}"' in script
    assert 'git commit -m "$COMMIT_MESSAGE"' in script
    assert 'git commit -m "mission:' not in script


def test_background_worker_propagates_commit_message():
    script = (ROOT / "scripts" / "vaf-start-background.sh").read_text(encoding="utf-8")

    assert 'VAF_COMMIT_MESSAGE="${VAF_COMMIT_MESSAGE:-}"' in script


def test_worker_logs_custom_commit_message_when_auto_commit_is_enabled():
    script = (ROOT / "scripts" / "vaf-worker.sh").read_text(encoding="utf-8")

    assert 'echo "VAF_COMMIT_MESSAGE=${VAF_COMMIT_MESSAGE}"' in script


def test_run_next_safe_script_exists_and_is_executable():
    script_path = ROOT / "scripts" / "vaf-run-next-safe.sh"

    assert script_path.exists()
    assert script_path.stat().st_mode & 0o111


def test_run_next_safe_script_has_expected_safety_checks():
    script = (ROOT / "scripts" / "vaf-run-next-safe.sh").read_text(encoding="utf-8")

    assert "set -euo pipefail" in script
    assert "VAF_AUTO_PUSH" in script
    assert "VAF_AUTO_COMMIT" in script
    assert "pytest" in script
    assert "compileall" in script
    assert "git push" in script
    assert "git status --porcelain" in script


def test_run_next_safe_script_has_valid_bash_syntax():
    script_path = ROOT / "scripts" / "vaf-run-next-safe.sh"

    subprocess.run(["bash", "-n", str(script_path)], check=True)


def test_run_batch_safe_script_exists_and_is_executable():
    script_path = ROOT / "scripts" / "vaf-run-batch-safe.sh"

    assert script_path.exists()
    assert script_path.stat().st_mode & 0o111


def test_run_batch_safe_script_has_expected_safety_contract():
    script = (ROOT / "scripts" / "vaf-run-batch-safe.sh").read_text(encoding="utf-8")

    assert "set -euo pipefail" in script
    assert "VAF_BATCH_SIZE" in script
    assert "MAX_BATCH_SIZE=10" in script
    assert "VAF_AUTO_PUSH" in script
    assert "./scripts/vaf-run-next-safe.sh" in script
    assert "VAF_AUTO_PUSH=0 ./scripts/vaf-run-next-safe.sh" in script
    assert "exit 1" in script
    assert "pytest" in script
    assert "python3 -m compileall src" in script
    assert "require_no_failed_missions" in script
    assert "require_git_clean" in script


def test_run_batch_safe_script_has_valid_bash_syntax():
    script_path = ROOT / "scripts" / "vaf-run-batch-safe.sh"

    subprocess.run(["bash", "-n", str(script_path)], check=True)


def test_safe_runner_usage_documentation_exists_and_covers_required_commands():
    doc_path = ROOT / "docs" / "operations" / "safe-runner-usage.md"

    assert doc_path.exists()

    doc = doc_path.read_text(encoding="utf-8")

    assert "./scripts/vaf-run-next-safe.sh" in doc
    assert "VAF_AUTO_PUSH=1 ./scripts/vaf-run-next-safe.sh" in doc
    assert 'VAF_COMMIT_MESSAGE="implementação: exemplo" ./scripts/vaf-run-next-safe.sh' in doc
    assert "push automático é opt-in" in doc
    assert "não substitui revisão humana" in doc
    assert "./scripts/vaf-run-batch-safe.sh" in doc
    assert "VAF_BATCH_SIZE=3" in doc
    assert "VAF_BATCH_SIZE=10" in doc
    assert "batch para na primeira falha" in doc
    assert "commits continuam separados por missão" in doc
