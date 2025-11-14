import asyncio
import yaml
import os
from nats_handler import NatsHandler

def load_config():
    config_file = os.getenv('CONFIG_FILE', '/app/config/config.yaml')
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

async def main():
    config = load_config()
    handler = NatsHandler(config)
    await handler.run()

if __name__ == '__main__':
    asyncio.run(main())