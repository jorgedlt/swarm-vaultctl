# TODO: Swarm-Vaultctl Integration Preparation

## Next Steps for SWARM Integration (Tomorrow)

1. **NATS Configuration Alignment**: Ensure NATS server URL and subjects match swarm-natscore defaults. Update config.yaml with correct swarm-natscore connection details.

2. **Network Setup**: Prepare Docker Swarm stack with overlay network for inter-pod communication. Ensure vaultctl connects to swarm-natscore on the shared network.

3. **Dependency Verification**: Confirm swarm-natscore is running and accessible. Test basic NATS connectivity from vaultctl container.

4. **Message Schema Standardization**: Review and align request/response formats with other pods (e.g., swarm-cronctl triggers, swarm-gateway requests). Document any needed adjustments.

5. **ACL Policy Updates**: Expand ACL rules to include subjects from swarm-cronctl, swarm-gateway, and future agents. Ensure proper access levels.

6. **Integration Testing**: Develop end-to-end tests with mocked swarm-natscore to simulate real NATS interactions. Test credential issuance workflows.

7. **Security Hardening**: Remove or disable SSH backdoor for production. Implement proper secret mounting for master key.

8. **Monitoring and Logging**: Integrate with swarm-logger by ensuring all interactions are logged via NATS. Add health checks.

9. **Documentation Updates**: Update README and AGENT.md with integration details, dependencies on other pods, and troubleshooting for SWARM context.

10. **Coordination Script Support**: Prepare for user-provided coordination script to orchestrate multi-pod startup and testing.

These items focus on stitching swarm-vaultctl into the broader SWARM ecosystem while maintaining its core functionality as the credential authority.