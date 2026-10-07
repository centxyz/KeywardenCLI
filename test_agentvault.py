import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main


class AgentVaultTests(unittest.TestCase):
    def test_encrypted_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            vault_file = Path(directory) / "vault.json"
            salt_file = Path(directory) / "salt.bin"
            with patch.object(main, "VAULT_FILE", vault_file), patch.object(main, "SALT_FILE", salt_file):
                salt = main.load_salt()
                key = main.derive_key("correct horse battery staple", salt)
                fernet = main.Fernet(key)
                expected = {"service": {"username": "agent", "password": "secret"}}
                main.save_vault(expected, fernet)
                self.assertEqual(main.load_vault(fernet), expected)
                self.assertNotIn(b"secret", vault_file.read_bytes())

    def test_parser_accepts_secure_password_prompt_flow(self):
        args = main.build_parser().parse_args(["add", "--service", "demo", "--username", "agent"])
        self.assertIsNone(args.password)


if __name__ == "__main__":
    unittest.main()
