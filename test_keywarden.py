import json
import stat
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

import keywarden


class KeywardenTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.path = Path(self.temporary.name) / "vault.json"
        self.store = keywarden.VaultStore(self.path)
        self.store.initialize("correct horse battery staple")

    def tearDown(self):
        self.temporary.cleanup()

    def test_encrypted_round_trip_and_permissions(self):
        entries = {"example": {"username": "cent", "password": "secret"}}
        self.store.save(entries, "correct horse battery staple")
        self.assertEqual(self.store.unlock("correct horse battery staple"), entries)
        self.assertNotIn("secret", self.path.read_text())
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o600)

    def test_wrong_password_is_rejected(self):
        with self.assertRaisesRegex(keywarden.VaultError, "Invalid master password"):
            self.store.unlock("wrong")

    def test_change_password_rotates_salt(self):
        old_salt = json.loads(self.path.read_text())["salt"]
        entries = self.store.unlock("correct horse battery staple")
        self.store.change_password(entries, "different strong password")
        self.assertNotEqual(json.loads(self.path.read_text())["salt"], old_salt)
        self.assertEqual(self.store.unlock("different strong password"), entries)

    def test_get_hides_secret_unless_explicitly_requested(self):
        self.store.save({"example": {"username": "cent", "password": "secret"}}, "correct horse battery staple")
        base = dict(vault=self.path, command="get", service="example")
        with patch.object(keywarden, "master_password", return_value="correct horse battery staple"):
            self.assertNotIn("secret", keywarden.run(Namespace(**base, show=False)))
            self.assertIn("secret", keywarden.run(Namespace(**base, show=True)))

    def test_generated_password_length_and_bounds(self):
        self.assertEqual(len(keywarden.generate_password(32)), 32)
        with self.assertRaises(keywarden.VaultError):
            keywarden.generate_password(8)


if __name__ == "__main__":
    unittest.main()
