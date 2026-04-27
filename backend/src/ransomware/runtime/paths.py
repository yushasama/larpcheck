import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuntimePaths:
    package_path: Path
    src_path: Path
    backend_path: Path
    repo_root: Path
    bundle_root: Path
    app_root: Path
    resources_path: Path
    testcases_path: Path
    sandbox_backup_path: Path
    sandbox_path: Path
    problems_path: Path
    state_path: Path


def _resolve_backup_path(*candidates: Path) -> Path:
    for candidate in candidates:
        if candidate.exists() and any(candidate.iterdir()):
            return candidate
    return candidates[-1]


def resolve_runtime_paths() -> RuntimePaths:
    runtime_path = Path(__file__).resolve().parent
    package_path = runtime_path.parent
    src_path = package_path.parent
    backend_path = src_path.parent
    repo_root = package_path.parents[2]

    if getattr(sys, "frozen", False):
        bundle_root = Path(getattr(sys, "_MEIPASS", package_path))
        app_root = Path(sys.executable).resolve().parent
        resources_path = bundle_root / "resources"
        testcases_path = bundle_root / "testcases"
        bundled_backup_path = bundle_root / "sandbox_backup"
        external_backup_path = app_root / "sandbox_backup"
        sandbox_backup_path = _resolve_backup_path(external_backup_path, bundled_backup_path)
    else:
        bundle_root = repo_root
        app_root = repo_root
        resources_path = package_path / "resources"
        testcases_path = src_path / "problem_bank" / "testcases"
        sandbox_backup_path = _resolve_backup_path(repo_root / "sandbox_backup")

    sandbox_path = app_root / "sandbox"
    problems_path = resources_path / "problems"
    state_path = app_root / ".larpcheck_state.json"

    return RuntimePaths(
        package_path=package_path,
        src_path=src_path,
        backend_path=backend_path,
        repo_root=repo_root,
        bundle_root=bundle_root,
        app_root=app_root,
        resources_path=resources_path,
        testcases_path=testcases_path,
        sandbox_backup_path=sandbox_backup_path,
        sandbox_path=sandbox_path,
        problems_path=problems_path,
        state_path=state_path,
    )


RUNTIME_PATHS = resolve_runtime_paths()

PACKAGE_PATH = RUNTIME_PATHS.package_path
SRC_PATH = RUNTIME_PATHS.src_path
BACKEND_PATH = RUNTIME_PATHS.backend_path
REPO_ROOT = RUNTIME_PATHS.repo_root
BUNDLE_ROOT = RUNTIME_PATHS.bundle_root
APP_ROOT = RUNTIME_PATHS.app_root
RESOURCES_PATH = RUNTIME_PATHS.resources_path
TESTCASES_PATH = RUNTIME_PATHS.testcases_path
SANDBOX_BACKUP_PATH = RUNTIME_PATHS.sandbox_backup_path
SANDBOX_PATH = RUNTIME_PATHS.sandbox_path
PROBLEMS_PATH = RUNTIME_PATHS.problems_path
STATE_PATH = RUNTIME_PATHS.state_path
