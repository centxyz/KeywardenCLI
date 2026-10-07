# KeywardenCLI

[![CI](https://github.com/centxyz/KeywardenCLI/actions/workflows/ci.yml/badge.svg)](https://github.com/centxyz/KeywardenCLI/actions/workflows/ci.yml)

KeywardenCLI is a local encrypted credential vault. It stores named usernames and passwords in one versioned encrypted file, derives its encryption key from a master password, writes updates atomically, and hides secrets unless they are explicitly requested.

## Security properties

- Fernet authenticated encryption
- PBKDF2-HMAC-SHA256 with 600,000 iterations and a random 128-bit salt
- Salt rotation when changing the master password
- Atomic file replacement and `0600` vault permissions
- No key, master password, or plaintext credential written to disk
- Secret output hidden unless `get --show` is used
- Cryptographically secure password generation

KeywardenCLI protects credentials at rest. It is not a system keychain, cannot protect secrets on a compromised machine, and has not received a professional security audit.

## Install

```bash
git clone https://github.com/centxyz/KeywardenCLI.git
cd KeywardenCLI
python -m venv .venv
source .venv/bin/activate
pip install .
```

## Usage

```bash
keywarden init
keywarden add github --username cent
keywarden add api-service --username agent --generate 32
keywarden list
keywarden get github
keywarden get github --show
keywarden delete github
keywarden change-master
```

Use `--vault /path/to/vault.json` before the command to select another vault. The default is `~/.keywarden/vault.json`.

Passing `--password` is useful for automation but can expose the credential through shell history or process listings. Omitting it opens a hidden prompt.

## Test

```bash
python -m unittest -v
```

The suite verifies encryption, restrictive permissions, incorrect-password handling, salt rotation, safe secret display, and password generation limits.

## License

MIT © cent

## Current limitations

- The vault cannot protect secrets on a compromised machine or from a process that captures the master password.
- It is not integrated with the operating-system keychain or hardware-backed storage.
- The project has not received a professional security audit.
