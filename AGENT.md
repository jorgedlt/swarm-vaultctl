# AGENT.md for swarm-vaultctl

## AI Agent Role
This repository is managed by an AI agent focused on building and maintaining swarm-vaultctl, a secure vault service for Docker Swarm clusters. The agent handles code development, testing, documentation, and repository management.

## Directory Structure
- `config/`: Configuration templates (YAML files for NATS, encryption, ACL).
- `docs/`: Internal documentation (internal.md for rebuild knowledge).
- `scripts/`: Helper scripts (key generation).
- `src/`: Core source code (vault.py, nats_handler.py, cli.py, main.py).
- `tests/`: Automated tests (unit/ and integration/).
- `.github/workflows/`: CI/CD pipelines.
- `Dockerfile`: Container build instructions.
- `entrypoint.sh`: Service startup script.
- `README.md`: Project documentation.
- `requirements.txt`: Python dependencies.
- `.gitignore`: Excludes secrets, logs, etc.

## Operational Notes
- Base image: python:3.9-slim (Debian) for compatibility.
- Communication: Exclusive via NATS messaging.
- Security: Encrypted storage, ACLs, no exposed secrets.
- Testing: Pytest for unit/integration, GitHub Actions for CI.
- Deployment: Docker Swarm stack with NATS network.
- Development: SSH backdoor (dev-only) for debugging.
- Ecosystem: Part of multi-agent platform (natscore, logger, cronctl, gateway).

## Maintenance
- Run tests before commits: `pytest tests/`
- Update docs for changes.
- Use gh for repo management.
- Never commit secrets; use .gitignore and Docker secrets.