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
