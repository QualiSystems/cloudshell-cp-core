from cloudshell.cp.core.requests.models import DriverResponse


class AbstractDeployFlow:
    def __init__(self, resource_config, logger):
        """

        :param resource_config:
        :param logger:
        """
        self._resource_config = resource_config
        self._logger = logger

    def _deploy(self, request_actions):
        """

        :param CleanupSandboxInfraRequestActions request_actions:
        :rtype: cloudshell.cp.core.models.DeployAppResult
        """
        raise NotImplementedError(
            f"Class {type(self)} must implement method '_deploy'"
        )

    def deploy(self, request_actions):
        """

        :param cloudshell.cp.core.driver_request_parser.RequestActions request_actions:
        :return:
        """
        deploy_app_result = self._deploy(
            request_actions=request_actions
        )

        return DriverResponse([deploy_app_result]).to_driver_response_json()
