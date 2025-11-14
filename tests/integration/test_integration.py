import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
import json
from src.nats_handler import NatsHandler

@pytest.mark.asyncio
async def test_full_operation():
    config = {
        'nats': {'url': 'nats://localhost:4222'},
        'encryption': {'master_key_file': '/tmp/master.key'},
        'storage': {'file': '/tmp/vault.db'},
        'subjects': {'request': 'vault.requests', 'reply': 'vault.replies'},
        'acl': [{'subject': 'admin.requests', 'operations': ['get', 'set']}]
    }
    handler = NatsHandler(config)
    handler.nc = MagicMock()
    handler.nc.connect = AsyncMock()
    handler.nc.subscribe = AsyncMock()
    handler.nc.publish = AsyncMock()

    # Mock vault
    handler.vault = MagicMock()
    handler.vault.get.return_value = 'test_value'

    # Mock message
    msg = MagicMock()
    msg.data = json.dumps({
        'operation': 'get',
        'key': 'test_key',
        'subject': 'admin.requests'
    }).encode()

    # Call message handler
    await handler.subscribe()
    # Get the callback
    call_args = handler.nc.subscribe.call_args
    callback = call_args[1]['cb']
    await callback(msg)

    # Check publish called with correct response
    handler.nc.publish.assert_called_once()
    published_data = json.loads(handler.nc.publish.call_args[0][1].decode())
    assert published_data['status'] == 'success'
    assert published_data['data'] == 'test_value'