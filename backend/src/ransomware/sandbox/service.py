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

        # Copy the backup tree over fresh so a reset never mixes old and new files.
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
        encrypted_count = 0
        restored_from_backup = False

        if not state.round_active and encrypted_files:
            # Once the round is over, put the demo files back instead of leaving ciphertext around.
            restored_from_backup = self.restore_from_backup()
            if state.encrypted:
                state.encrypted = False
                state_changed = True

            return SandboxSyncResult(
                restored_from_backup=restored_from_backup,
                state_changed=state_changed,
                backup_available=self.has_backup(),
            )

        if encrypted_files and not state.encrypted:
            state.encrypted = True
            state_changed = True

        if state.round_active and state.encrypted and encrypted_files < total_files:
            # Re-encrypt anything that got manually restored mid-round.
            encrypted_count = self.encrypt()
            total_files, encrypted_files = sandbox_file_counts(self.sandbox_path)

        if not encrypted_files and state.encrypted:
            state.encrypted = False
            state_changed = True

        return SandboxSyncResult(
            encrypted_count=encrypted_count,
            state_changed=state_changed,
            backup_available=self.has_backup(),
        )
