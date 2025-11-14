import pytest
from click.testing import CliRunner
from src.cli import cli
import tempfile
import os
import yaml

class TestCLI:
    def setup_method(self):
        self.runner = CliRunner()
        self.config = {
            'encryption': {'master_key_file': '/tmp/master.key'},
            'storage': {'file': '/tmp/vault.db'}
        }
        self.config_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(self.config, self.config_file)
        self.config_file.close()
        self.master_key_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.master_key_file.write('test_master_key')
        self.master_key_file.close()
        # Update config
        self.config['encryption']['master_key_file'] = self.master_key_file.name
        with open(self.config_file.name, 'w') as f:
            yaml.dump(self.config, f)

    def teardown_method(self):
        os.unlink(self.config_file.name)
        os.unlink(self.master_key_file.name)

    def test_get_command(self):
        result = self.runner.invoke(cli, ['--config', self.config_file.name, 'set', 'key1', 'value1'])
        assert result.exit_code == 0
        result = self.runner.invoke(cli, ['--config', self.config_file.name, 'get', 'key1'])
        assert result.exit_code == 0
        assert result.output.strip() == 'value1'

    def test_list_command(self):
        self.runner.invoke(cli, ['--config', self.config_file.name, 'set', 'key1', 'value1'])
        result = self.runner.invoke(cli, ['--config', self.config_file.name, 'list'])
        assert result.exit_code == 0
        assert 'key1' in result.output