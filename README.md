# swarm-vaultctl

swarm-vaultctl is a Docker container designed to run as a secure, centralized vault service inside a Docker Swarm cluster, part of a coordinated ecosystem of autonomous service pods. It provides a portable vault for storing and retrieving secrets, tokens, small encrypted documents, and structured secure data, serving as the credential authority for AI agents. All operational communication to and from the vault occurs exclusively through a NATS messaging bus (swarm-natscore). Human programmers may access a local programming interface for debugging or administrative use, but AI agents and automated components interact only through NATS subjects.

## How It Works

The container runs a vault service that manages encrypted storage using a small embedded key-value store with strong encryption. All external interactions use NATS messaging: the vault subscribes to request subjects and publishes responses to reply subjects.

Supported operations via NATS:
- `get <key>`: Retrieve a secret by key
- `set <key> <value>`: Set or update a secret
- `delete <key>`: Delete a secret
- `list`: List all keys
- `rotate`: Rotate the master encryption key
- `status`: Return metadata or status

All stored data is encrypted at rest with a master key. An ACL mechanism restricts which request subjects can perform operations.

## Deployment in Swarm Stack

To deploy in a Docker Swarm:

1. Build the image:
   ```
   docker build -t swarm-vaultctl .
   ```

2. Deploy as a service in your Swarm stack:
   ```
   docker service create --name vaultctl --network my-nats-network swarm-vaultctl
   ```

Ensure the NATS server is accessible on the same network.

## Configuration

Configure via environment variables or config files in `/app/config/`:
- NATS server URL and authentication
- Encryption master key source
- Default subjects for requests and replies
- Access policy definitions

Example config.yaml:
```yaml
nats:
  url: nats://nats-server:4222
  user: vault
  pass: secret

encryption:
  master_key: /app/config/master.key

subjects:
  request: vault.requests
  reply: vault.replies

acl:
  - subject: admin.requests
    operations: [get, set, delete, list, rotate, status]
  - subject: user.requests
    operations: [get, set]
```

## Key Generation and Rotation

Generate a master key:
```
python scripts/generate_key.py > config/master.key
```

Rotate the key via NATS: send a `rotate` request.

## Local Programming Interface

Access the CLI inside the container for debugging:
```
docker exec -it <container_id> python src/cli.py <command>
```

Commands mirror NATS operations: get, set, delete, list, rotate, status.

## Example NATS Messages

Request:
```json
{
  "operation": "set",
  "key": "mysecret",
  "value": "secretvalue",
  "subject": "admin.requests"
}
```

Response:
```json
{
  "status": "success",
  "data": null
}
```

## Testing

This repository includes an automated testing plan with unit tests, integration tests, and CI/CD.

### Unit Tests
Unit tests cover individual components:
- `tests/unit/test_vault.py`: Tests the Vault class for encryption, storage, and operations.
- `tests/unit/test_nats_handler.py`: Tests the NatsHandler for message handling and ACL.
- `tests/unit/test_cli.py`: Tests the CLI commands.

Run unit tests with:
```
pytest tests/unit/
```

### Integration Tests
Integration tests verify the full system interaction:
- `tests/integration/test_integration.py`: Tests end-to-end message processing with mocked NATS.

Run integration tests with:
```
pytest tests/integration/
```

### CI/CD
GitHub Actions runs tests on every push and pull request to main/master branches.
- Installs dependencies
- Runs unit and integration tests
- Lints code with flake8

## Developer Backdoor (Development Only)

**WARNING: This is for DEVELOPMENT ONLY. DO NOT use in production.**

The container includes an SSH server for debugging purposes. It allows SSH access to load cron tasks and inspect the container.

- SSH is exposed on port 22.
- Root login with password `devpassword`.
- Cron is running for task scheduling.

To access:
```
ssh root@<container_ip> -p 22
# Password: devpassword
```

**Security Risks:**
- SSH exposes the container to potential attacks.
- Root access allows full control.
- Disable SSH in production by modifying the Dockerfile or entrypoint.

## Ecosystem Integration

swarm-vaultctl is part of a coordinated ecosystem of autonomous service pods in a Docker Swarm environment, forming a multi-agent platform that AIs can use as a toolbox. Each pod has a single purpose but relies on others for functionality, communicating exclusively through a central NATS messaging fabric (swarm-natscore).

### Pod Responsibilities
- **swarm-natscore**: Central NATS server for message routing, subject hierarchies, and stable communication.
- **swarm-logger**: Subscribes to NATS messages for observability, auditability, and traceability.
- **swarm-cronctl**: Sends timed triggers for AI agent activation and workflows.
- **swarm-vaultctl**: Manages sensitive material, issues scoped short-lived credentials via NATS.
- **swarm-gateway**: Translates HTTP requests to NATS messages and responses back.

### swarm-vaultctl's Role
As the credential authority, swarm-vaultctl holds all secrets and provides controlled access. It ensures no other pod stores full secrets, limiting blast radius. Agents request credentials through defined NATS messages, receiving clear responses with lifecycles.

### Message Patterns and Interfaces
- **Request Subjects**: vault.requests (e.g., {"operation": "get", "key": "secret", "subject": "agent.requests"})
- **Response Subjects**: vault.replies (e.g., {"status": "success", "data": "value"} or {"status": "error", "message": "Access denied"})
- **Operations**: get, set, delete, list, rotate, status.
- **ACL Enforcement**: Restricts operations by requesting subject.
- **Dependencies**: Relies on swarm-natscore for communication; swarm-cronctl may trigger rotations; swarm-logger records interactions.
- **Assumptions**: NATS is stable; agents handle credential expiration; no direct pod-to-pod communication outside NATS.

### Operational Principles
- **Focus**: Exclusive on secret storage and credential issuance.
- **Interoperability**: Clear message schemas, consistent formats, documented error states.
- **Stability**: Reliable encryption, predictable responses, no message interpretation.
- **Documentation**: This README serves as internal knowledge for rebuilds/restarts, ensuring awareness of ecosystem fit.

By maintaining this holistic view, swarm-vaultctl ensures compatibility, clarity, and long-term stability in the multi-agent environment.

## Security Considerations

- Store master key securely, e.g., via Docker secrets.
- Use TLS for NATS if possible.
- Limit ACLs to necessary operations.
- Regularly rotate keys.
- Do not expose the CLI externally.
- Remove SSH backdoor for production deployments.