#!/usr/bin/env python3
"""
AgentVault - a simple encrypted credential store for agents.
"""

import os
import json
import argparse
import getpass
import base64
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken

# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
VAULT_FILE = Path.home() / ".agentvault" / "vault.json"
SALT_FILE = Path.home() / ".agentvault" / "salt.bin"
ITERATIONS = 100_000

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def ensure_vault_dir():
    """Create vault directory if it does not exist."""
    VAULT_FILE.parent.mkdir(parents=True, exist_ok=True)

def generate_salt():
    """Create a new random salt and save it."""
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt

def load_salt():
    """Load existing salt or generate a new one."""
    if not SALT_FILE.exists():
        return generate_salt()
    with open(SALT_FILE, "rb") as f:
        return f.read()

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet key from the master password."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def load_vault(fernet: Fernet) -> dict:
    """Decrypt and return the vault contents."""
    if not VAULT_FILE.exists():
        return {}
    with open(VAULT_FILE, "rb") as f:
        encrypted = f.read()
    try:
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except InvalidToken:
        raise SystemExit("Invalid master password or corrupted vault.")

def save_vault(vault: dict, fernet: Fernet):
    """Encrypt and write the vault to disk."""
    data = json.dumps(vault).encode()
    encrypted = fernet.encrypt(data)
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)

# ----------------------------------------------------------------------
# Command implementations
# ----------------------------------------------------------------------
def cmd_init(args):
    """Initialize a new vault."""
    ensure_vault_dir()
    if VAULT_FILE.exists():
        print("Vault already exists.")
        return
    password = getpass.getpass("Set master password: ")
    confirm = getpass.getpass("Confirm master password: ")
    if password != confirm:
        print("Passwords do not match.")
        return
    salt = load_salt()
    key = derive_key(password, salt)
    fernet = Fernet(key)
    save_vault({}, fernet)
    print("Vault initialized successfully.")

def cmd_add(args):
    """Add a new credential entry."""
    password = getpass.getpass("Master password: ")
    salt = load_salt()
    key = derive_key(password, salt)
    fernet = Fernet(key)
    vault = load_vault(fernet)

    entry_password = args.password or getpass.getpass("Credential password: ")
    entry = {
        "username": args.username,
        "password": entry_password,
    }
    vault[args.service] = entry
    save_vault(vault, fernet)
    print(f"Credential for '{args.service}' added.")

def cmd_get(args):
    """Retrieve a credential."""
    password = getpass.getpass("Master password: ")
    salt = load_salt()
    key = derive_key(password, salt)
    fernet = Fernet(key)
    vault = load_vault(fernet)

    entry = vault.get(args.service)
    if not entry:
        print(f"No entry found for service '{args.service}'.")
        return
    print(f"Service: {args.service}")
    print(f"Username: {entry['username']}")
    print(f"Password: {entry['password']}")

def cmd_list(_):
    """List all stored services."""
    password = getpass.getpass("Master password: ")
    salt = load_salt()
    key = derive_key(password, salt)
    fernet = Fernet(key)
    vault = load_vault(fernet)

    if not vault:
        print("Vault is empty.")
        return
    print("Stored services:")
    for service in vault.keys():
        print(f" - {service}")

def cmd_delete(args):
    """Delete a credential."""
    password = getpass.getpass("Master password: ")
    salt = load_salt()
    key = derive_key(password, salt)
    fernet = Fernet(key)
    vault = load_vault(fernet)

    if args.service not in vault:
        print(f"No entry for '{args.service}'.")
        return
    del vault[args.service]
    save_vault(vault, fernet)
    print(f"Entry for '{args.service}' removed.")

# ----------------------------------------------------------------------
# Argument parser setup
# ----------------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(prog="agentvault", description="AgentVault - Secure credential manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize a new vault")

    add_parser = subparsers.add_parser("add", help="Add a credential")
    add_parser.add_argument("--service", required=True, help="Service identifier")
    add_parser.add_argument("--username", required=True, help="Username for the service")
    add_parser.add_argument("--password", help="Password for the service (prompted securely when omitted)")

    get_parser = subparsers.add_parser("get", help="Retrieve a credential")
    get_parser.add_argument("--service", required=True, help="Service identifier")

    subparsers.add_parser("list", help="List all stored services")

    del_parser = subparsers.add_parser("delete", help="Delete a credential")
    del_parser.add_argument("--service", required=True, help="Service identifier")

    return parser

# ----------------------------------------------------------------------
# Main entry point
# ----------------------------------------------------------------------
def main():
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "init": cmd_init,
        "add": cmd_add,
        "get": cmd_get,
        "list": cmd_list,
        "delete": cmd_delete,
    }

    commands[args.command](args)

if __name__ == "__main__":
    main()
