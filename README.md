# AgentVault

**AgentVault** is a lightweight, open‑source password vault designed for field agents and security professionals. It stores credentials securely using symmetric encryption and provides a simple command‑line interface.

## Features
- AES‑256 encryption with Fernet (cryptography library)
- Add, retrieve, list, and delete entries
- Master password‑derived key (PBKDF2)
- JSON‑based storage (encrypted on disk)
- Cross‑platform (Windows, macOS, Linux)

## Installation
```bash
git clone https://github.com/yourname/AgentVault.git
cd AgentVault
pip install -r requirements.txt
```

## Usage
```bash
# Initialize vault (creates vault.json)
python main.py init

# Add a new credential
python main.py add --service "AlphaOps" --username "agent007" --password "s3cr3t!"

# Retrieve a credential
python main.py get --service "AlphaOps"

# List all stored services
python main.py list

# Delete a credential
python main.py delete --service "AlphaOps"
```

## License
MIT License – feel free to modify and distribute.