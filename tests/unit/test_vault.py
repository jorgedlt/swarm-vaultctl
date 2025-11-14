import pytest
import tempfile
import os
from src.vault import Vault

class TestVault:
    def setup_method(self):
        self.master_key = "test_master_key"
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.vault = Vault(self.master_key, self.temp_file.name)

    def teardown_method(self):
        os.unlink(self.temp_file.name)

    def test_set_and_get(self):
        self.vault.set("key1", "value1")
        assert self.vault.get("key1") == "value1"

    def test_delete(self):
        self.vault.set("key1", "value1")
        assert self.vault.delete("key1") == True
        assert self.vault.get("key1") is None
        assert self.vault.delete("key1") == False

    def test_list_keys(self):
        self.vault.set("key1", "value1")
        self.vault.set("key2", "value2")
        keys = self.vault.list_keys()
        assert set(keys) == {"key1", "key2"}

    def test_rotate_key(self):
        self.vault.set("key1", "value1")
        new_key = "new_master_key"
        self.vault.rotate_key(new_key)
        # After rotation, should still get the value
        assert self.vault.get("key1") == "value1"

    def test_status(self):
        self.vault.set("key1", "value1")
        status = self.vault.status()
        assert status["keys_count"] == 1
        assert status["storage_file"] == self.temp_file.name