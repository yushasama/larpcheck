import shutil
from dataclasses import dataclass
from pathlib import Path

from ransomware.config import SANDBOX_BACKUP_PATH, SANDBOX_PATH
from ransomware.crypto import decrypt_all, encrypt_all, sandbox_file_counts
from ransomware.state import RansomwareState


@dataclass(frozen=True)
class SandboxSyncResult:
    restored_from_backup: bool = False
    decrypted_count: int = 0
    encrypted_count: int = 0
    state_changed: bool = False
    backup_available: bool = True


class SandboxManager:
    def __init__(
        self,
        sandbox_path: Path = SANDBOX_PATH,
        backup_path: Path = SANDBOX_BACKUP_PATH,
    ) -> None:
        self.sandbox_path = sandbox_path
        self.backup_path = backup_path

    def is_empty(self) -> bool:
        return not self.sandbox_path.exists() or not any(self.sandbox_path.iterdir())

    def has_backup(self) -> bool:
        return self.backup_path.exists() and any(self.backup_path.iterdir())

    def restore_from_backup(self) -> bool:
        if not self.has_backup():
            return False

        self.sandbox_path.mkdir(parents=True, exist_ok=True)
        for child in self.sandbox_path.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

        for source in self.backup_path.rglob("*"):
            target = self.sandbox_path / source.relative_to(self.backup_path)
            if source.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
        return True

    def encrypt(self) -> int:
        return encrypt_all(self.sandbox_path)

    def decrypt(self) -> int:
        return decrypt_all(self.sandbox_path)

    def reconcile(self, state: RansomwareState) -> SandboxSyncResult:
        self.sandbox_path.mkdir(parents=True, exist_ok=True)
        total_files, encrypted_files = sandbox_file_counts(self.sandbox_path)
        if total_files == 0:
            return SandboxSyncResult(
                restored_from_backup=self.restore_from_backup(),
                backup_available=self.has_backup(),
            )

        state_changed = False
        decrypted_count = 0
        encrypted_count = 0

        if encrypted_files and (not state.round_active or not state.encrypted):
            decrypted_count = self.decrypt()
            if state.encrypted:
                state.encrypted = False
                state_changed = True
            total_files, encrypted_files = sandbox_file_counts(self.sandbox_path)

        if state.round_active and state.encrypted and encrypted_files < total_files:
            encrypted_count = self.encrypt()
            total_files, encrypted_files = sandbox_file_counts(self.sandbox_path)

        if not encrypted_files and state.encrypted:
            state.encrypted = False
            state_changed = True

        return SandboxSyncResult(
            decrypted_count=decrypted_count,
            encrypted_count=encrypted_count,
            state_changed=state_changed,
            backup_available=self.has_backup(),
        )
