import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from ransomware.config import STATE_PATH
import hmac, hashlib

_HMAC_SECRET = b"larpcheck-solve-2026"

@dataclass
class RansomwareState:
    started_at: float = field(default_factory=time.time)
    active_problem_ids: list[str] = field(default_factory=list)
    solved_problem_ids: list[str] = field(default_factory=list)
    penalties: int = 0
    encrypted: bool = False
    round_active: bool = True
    solve_tokens: dict[str, str] = field(default_factory=dict)


def load_state() -> RansomwareState:
    if not STATE_PATH.exists():
        return RansomwareState()
    data = json.loads(STATE_PATH.read_text())
    return RansomwareState(
        started_at=data.get("started_at", time.time()),
        active_problem_ids=data.get("active_problem_ids", []),
        solved_problem_ids=data.get("solved_problem_ids", []),
        penalties=data.get("penalties", 0),
        encrypted=data.get("encrypted", False),
        round_active=data.get("round_active", True),
        solve_tokens=data.get("solve_tokens", {}),
    )


def save_state(state: RansomwareState) -> None:
    STATE_PATH.write_text(json.dumps(asdict(state), indent=2))


def clear_state() -> None:
    if STATE_PATH.exists():
        STATE_PATH.unlink()

def sign_solve(problem_id: str) -> str:
    return hmac.new(_HMAC_SECRET, problem_id.encode(), hashlib.sha256).hexdigest()

def verify_solve(problem_id: str, token: str) -> bool:
    return hmac.compare_digest(sign_solve(problem_id), token)