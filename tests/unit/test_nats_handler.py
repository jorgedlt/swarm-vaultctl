import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from src.nats_handler import NatsHandler

class TestNatsHandler:
    def setup_method(self):
        self.config = {
            'nats': {'url': 'nats://localhost:4222'},
            'encryption': {'master_key_file': '/tmp/master.key'},
            'storage': {'file': '/tmp/vault.db'},
            'subjects': {'request': 'vault.requests', 'reply': 'vault.replies'},
            'acl': [{'subject': 'admin.requests', 'operations': ['get', 'set']}]
        }
        self.handler = NatsHandler(self.config)

    @pytest.mark.asyncio
    async def test_connect(self):
        self.handler.nc.connect = AsyncMock()
        await self.handler.connect()
        self.handler.nc.connect.assert_called_once_with(
            'nats://localhost:4222', user=None, password=None
        )

    def test_check_acl(self):
        assert self.handler._check_acl('admin.requests', 'get') == True
        assert self.handler._check_acl('admin.requests', 'delete') == False
        assert self.handler._check_acl('user.requests', 'get') == False

    def test_handle_operation_get(self):
        self.handler.vault = MagicMock()
        self.handler.vault.get.return_value = 'value'
        response = self.handler._handle_operation('get', 'key', None)
        assert response == {"status": "success", "data": "value"}

    def test_handle_operation_set(self):
        self.handler.vault = MagicMock()
        response = self.handler._handle_operation('set', 'key', 'value')
        self.handler.vault.set.assert_called_once_with('key', 'value')
        assert response == {"status": "success"}

    def test_handle_operation_unknown(self):
        self.handler.vault = MagicMock()
        response = self.handler._handle_operation('unknown', 'key', 'value')
        assert response == {"status": "error", "message": "Unknown operation"}