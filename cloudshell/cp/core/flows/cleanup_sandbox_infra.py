from cloudshell.cp.core.request_actions import DriverResponse
from cloudshell.cp.core.request_actions.models import CleanupNetworkResult


class AbstractCleanupSandboxInfraFlow:
    def __init__(self, resource_config, logger):
        """

        :param resource_config:
        :param logger:
        """
        self._resource_config = resource_config
        self._logger = logger

    def cleanup_sandbox_infra(self, request_actions):
        """

        :param CleanupSandboxInfraRequestActions request_actions:
        :return:
        """
        raise NotImplementedError(
            f"Class {type(self)} must implement method 'cleanup_sandbox_infra'"
        )

    def _cleanup_sandbox_infra(self, request_actions):
        """

        :param PrepareSandboxInfraRequestActions request_actions:
        :return:
        """
        action = request_actions.cleanup_network
        self.cleanup_sandbox_infra(request_actions)

        return CleanupNetworkResult(actionId=action.actionId)

    def cleanup(self, request_actions):
        """

        :param cloudshell.cp.core.driver_request_parser.RequestActions request_actions:
        :return:
        """
        cleanup_sandbox_infra_result = self._cleanup_sandbox_infra(
            request_actions=request_actions
        )

        return DriverResponse([cleanup_sandbox_infra_result]).to_driver_response_json()
