import asyncio
import json
import yaml
from nats.aio.client import Client as NATS
from vault import Vault

class NatsHandler:
    def __init__(self, config):
        self.config = config
        self.nc = NATS()
        self.vault = None

    async def connect(self):
        await self.nc.connect(
            self.config['nats']['url'],
            user=self.config['nats'].get('user'),
            password=self.config['nats'].get('pass')
        )

    async def setup_vault(self):
        master_key_file = self.config['encryption']['master_key_file']
        with open(master_key_file, 'r') as f:
            master_key = f.read().strip()
        storage_file = self.config['storage']['file']
        self.vault = Vault(master_key, storage_file)

    async def subscribe(self):
        subject = self.config['subjects']['request']
        reply_subject = self.config['subjects']['reply']

        async def message_handler(msg):
            try:
                data = json.loads(msg.data.decode())
                operation = data.get('operation')
                key = data.get('key')
                value = data.get('value')
                requester_subject = data.get('subject')

                if not self._check_acl(requester_subject, operation):
                    response = {"status": "error", "message": "Access denied"}
                else:
                    response = self._handle_operation(operation, key, value)
            except Exception as e:
                response = {"status": "error", "message": str(e)}

            await self.nc.publish(reply_subject, json.dumps(response).encode())

        await self.nc.subscribe(subject, cb=message_handler)

    def _check_acl(self, subject, operation):
        for rule in self.config['acl']:
            if rule['subject'] == subject and operation in rule['operations']:
                return True
        return False

    def _handle_operation(self, operation, key, value):
        if operation == 'get':
            data = self.vault.get(key)
            return {"status": "success", "data": data}
        elif operation == 'set':
            self.vault.set(key, value)
            return {"status": "success"}
        elif operation == 'delete':
            success = self.vault.delete(key)
            return {"status": "success" if success else "error", "message": "Key not found"}
        elif operation == 'list':
            keys = self.vault.list_keys()
            return {"status": "success", "data": keys}
        elif operation == 'rotate':
            # For simplicity, assume new key is provided, but in practice, generate or get from secure source
            new_key = value  # Placeholder
            self.vault.rotate_key(new_key)
            return {"status": "success"}
        elif operation == 'status':
            status = self.vault.status()
            return {"status": "success", "data": status}
        else:
            return {"status": "error", "message": "Unknown operation"}

    async def run(self):
        await self.connect()
        await self.setup_vault()
        await self.subscribe()
        await asyncio.Future()  # Run forever