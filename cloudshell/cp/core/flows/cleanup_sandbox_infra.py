from cloudshell.cp.core.request_actions import DriverResponse
from cloudshell.cp.core.request_actions.models import CleanupNetworkResult


class AbstractCleanupSandboxInfraFlow:
    def __init__(self, logger):
        """Init command.

        :param logger:
        """
        self._logger = logger

    def cleanup_sandbox_infra(self, request_actions):
        """Cleanup Sandbox Infra.

        :param cloudshell.cp.core.request_actions.CleanupSandboxInfraRequestActions request_actions:  # noqa: E501
        :return:
        """
        raise NotImplementedError(
            f"Class {type(self)} must implement method 'cleanup_sandbox_infra'"
        )

    def _cleanup_sandbox_infra(self, request_actions):
        """Cleanup Sandbox Infra.

        :param cloudshell.cp.core.request_actions.CleanupSandboxInfraRequestActions request_actions:  # noqa: E501
        :rtype: cloudshell.cp.core.request_actions.models.CleanupNetworkResult
        """
        action = request_actions.cleanup_network
        self.cleanup_sandbox_infra(request_actions)

        return CleanupNetworkResult(actionId=action.actionId)

    def cleanup(self, request_actions):
        """Cleanup Sandbox Infra.

        :param cloudshell.cp.core.request_actions.CleanupSandboxInfraRequestActions request_actions:  # noqa: E501
        :rtype: str
        """
        cleanup_sandbox_infra_result = self._cleanup_sandbox_infra(
            request_actions=request_actions
        )

        return DriverResponse([cleanup_sandbox_infra_result]).to_driver_response_json()
