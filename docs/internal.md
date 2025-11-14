# swarm-vaultctl Internal Documentation

This document serves as internal knowledge for swarm-vaultctl, ensuring that if the pod is restarted, rebuilt, or redeployed, it retains a clear understanding of its function, interfaces, dependencies, assumptions, and operational state.

## Purpose and Function
swarm-vaultctl is the credential and secret authority in the multi-agent ecosystem. It holds all sensitive material and issues scoped, short-lived credentials to agents requesting access via NATS messages. No other pod stores full secrets, enforcing controlled access and limiting blast radius.

## Interfaces
- **NATS Subjects**:
  - Request: `vault.requests` (e.g., {"operation": "get", "key": "secret", "subject": "agent.requests"})
  - Reply: `vault.replies` (e.g., {"status": "success", "data": "value"})
- **Operations**: get, set, delete, list, rotate, status.
- **ACL**: Restricts operations by subject (e.g., admin.requests allows all, user.requests allows get/set).
- **Local CLI**: For debugging (not exposed externally).

## Dependencies
- **swarm-natscore**: For message routing and communication.
- **swarm-cronctl**: May send rotation triggers.
- **swarm-logger**: Records all interactions for audit.
- **Cryptography Library**: For AES-GCM encryption.

## Assumptions
- NATS is stable and available.
- Agents handle credential expiration and renewal.
- Master key is securely mounted or generated.
- No direct pod-to-pod communication outside NATS.
- Ecosystem peers follow documented patterns.

## Operational State
- Runs vault service with encrypted storage (JSON file).
- Subscribes to NATS requests, processes with ACL checks.
- Publishes responses to reply subjects.
- Maintains status/metadata for queries.
- Supports key rotation for security.

## Build and Deployment
- Base: python:3.9-slim (Debian for compatibility).
- Entrypoint: Launches vault, NATS handler, SSH (dev), cron (dev).
- Config: YAML for NATS, encryption, subjects, ACL.
- Testing: Unit/integration tests, CI/CD.

This ensures swarm-vaultctl remembers its role in the larger ecosystem and maintains interoperability.