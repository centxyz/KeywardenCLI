# AgentVault

AgentVault is a local encrypted credential-store CLI. It derives a Fernet encryption key from a master password with PBKDF2 and stores the encrypted vault under `~/.agentvault`.

## Install

```bash
git clone https://github.com/centxyz/AgentVault.git
cd AgentVault
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py init
python main.py add --service example --username agent
python main.py get --service example
python main.py list
python main.py delete --service example
```

Omit `--password` when adding an entry to receive a hidden password prompt. Supplying it on the command line is supported for automation but may expose it through shell history or process listings.

## Test

```bash
python -m unittest -v
```

## Security scope

AgentVault protects the vault at rest. It is not a system keychain, does not prevent compromise while unlocked, and has not received a professional security audit.

## License

MIT
