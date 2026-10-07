#!/usr/bin/env python3
"""KeywardenCLI: a local encrypted credential vault."""

import argparse
import base64
import getpass
import json
import os
import secrets
import string
import tempfile
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

VERSION = 1
ITERATIONS = 600_000
DEFAULT_VAULT = Path.home() / ".keywarden" / "vault.json"


class VaultError(Exception):
    """A safe, user-facing vault error."""


def derive_key(password: str, salt: bytes, iterations: int = ITERATIONS) -> bytes:
    if not password:
        raise VaultError("Master password cannot be empty.")
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations)
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


class VaultStore:
    def __init__(self, path: Path = DEFAULT_VAULT):
        self.path = Path(path).expanduser().resolve()

    def exists(self) -> bool:
        return self.path.exists()

    def initialize(self, password: str) -> None:
        if self.exists():
            raise VaultError(f"Vault already exists: {self.path}")
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._write({}, password, os.urandom(16))

    def unlock(self, password: str) -> dict:
        if not self.exists():
            raise VaultError("Vault is not initialized. Run `keywarden init` first.")
        try:
            document = json.loads(self.path.read_text(encoding="utf-8"))
            salt = base64.urlsafe_b64decode(document["salt"])
            key = derive_key(password, salt, int(document["iterations"]))
            plaintext = Fernet(key).decrypt(document["ciphertext"].encode("ascii"))
            entries = json.loads(plaintext.decode("utf-8"))
        except (KeyError, ValueError, json.JSONDecodeError, InvalidToken) as error:
            raise VaultError("Invalid master password or corrupted vault.") from error
        if not isinstance(entries, dict):
            raise VaultError("Vault contents are invalid.")
        return entries

    def save(self, entries: dict, password: str) -> None:
        document = self._read_document()
        salt = base64.urlsafe_b64decode(document["salt"])
        self._write(entries, password, salt, int(document["iterations"]))

    def change_password(self, entries: dict, new_password: str) -> None:
        self._write(entries, new_password, os.urandom(16))

    def _read_document(self) -> dict:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise VaultError("Unable to read vault.") from error

    def _write(self, entries: dict, password: str, salt: bytes, iterations: int = ITERATIONS) -> None:
        key = derive_key(password, salt, iterations)
        ciphertext = Fernet(key).encrypt(json.dumps(entries, sort_keys=True).encode("utf-8")).decode("ascii")
        document = {"version": VERSION, "kdf": "pbkdf2-sha256", "iterations": iterations, "salt": base64.urlsafe_b64encode(salt).decode("ascii"), "ciphertext": ciphertext}
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        descriptor, temporary = tempfile.mkstemp(prefix=".vault-", dir=self.path.parent)
        try:
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                json.dump(document, handle, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
            os.chmod(self.path, 0o600)
        except Exception:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            raise


def generate_password(length: int = 24) -> str:
    if length < 12 or length > 256:
        raise VaultError("Generated password length must be between 12 and 256.")
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def master_password(prompt: str = "Master password: ") -> str:
    return getpass.getpass(prompt)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="keywarden", description="Local encrypted credential vault")
    parser.add_argument("--vault", type=Path, default=DEFAULT_VAULT, help="vault file path")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="create a new encrypted vault")
    add = commands.add_parser("add", help="add or update a credential")
    add.add_argument("service")
    add.add_argument("--username", required=True)
    add.add_argument("--password", help="credential password; hidden prompt when omitted")
    add.add_argument("--generate", type=int, metavar="LENGTH", help="generate a credential password")
    get = commands.add_parser("get", help="read a credential")
    get.add_argument("service")
    get.add_argument("--show", action="store_true", help="display the secret value")
    commands.add_parser("list", help="list stored service names")
    delete = commands.add_parser("delete", help="delete a credential")
    delete.add_argument("service")
    commands.add_parser("change-master", help="rotate the master password and salt")
    return parser


def run(args: argparse.Namespace) -> str:
    store = VaultStore(args.vault)
    if args.command == "init":
        password = master_password("New master password: ")
        if password != master_password("Confirm master password: "):
            raise VaultError("Passwords do not match.")
        store.initialize(password)
        return f"Vault initialized: {store.path}"

    password = master_password()
    entries = store.unlock(password)
    if args.command == "list":
        return "\n".join(sorted(entries)) if entries else "Vault is empty."
    if args.command == "add":
        if args.generate and args.password:
            raise VaultError("Use either --generate or --password, not both.")
        secret = generate_password(args.generate) if args.generate else (args.password or getpass.getpass("Credential password: "))
        entries[args.service] = {"username": args.username, "password": secret}
        store.save(entries, password)
        return f"Saved credential: {args.service}"
    if args.command == "get":
        if args.service not in entries:
            raise VaultError(f"Credential not found: {args.service}")
        entry = entries[args.service]
        lines = [f"Service: {args.service}", f"Username: {entry['username']}"]
        lines.append(f"Password: {entry['password']}" if args.show else "Password: [hidden; use --show]")
        return "\n".join(lines)
    if args.command == "delete":
        if args.service not in entries:
            raise VaultError(f"Credential not found: {args.service}")
        del entries[args.service]
        store.save(entries, password)
        return f"Deleted credential: {args.service}"
    if args.command == "change-master":
        new_password = master_password("New master password: ")
        if new_password != master_password("Confirm new master password: "):
            raise VaultError("Passwords do not match.")
        store.change_password(entries, new_password)
        return "Master password changed."
    raise VaultError("Unknown command.")


def main() -> int:
    try:
        print(run(build_parser().parse_args()))
        return 0
    except VaultError as error:
        print(f"keywarden: {error}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
