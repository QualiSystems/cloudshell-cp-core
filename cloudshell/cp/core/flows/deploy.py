from cloudshell.cp.core.request_actions import DriverResponse


class AbstractDeployFlow:
    def __init__(self, logger):
        """Init command.

        :param logging.Logger logger:
        """
        self._logger = logger

    def _deploy(self, request_actions):
        """Deploy Virtual Machine.

        :param cloudshell.cp.core.request_actions.DeployVMRequestActions request_actions:  # noqa: E501
        :rtype: cloudshell.cp.core.request_actions.models.DeployAppResult
        """
        raise NotImplementedError(f"Class {type(self)} must implement method '_deploy'")

    def deploy(self, request_actions):
        """Deploy Virtual Machine.

        :param cloudshell.cp.core.request_actions.DeployVMRequestActions request_actions:  # noqa: E501
        :rtype: str
        """
        deploy_app_result = self._deploy(request_actions=request_actions)

        return DriverResponse([deploy_app_result]).to_driver_response_json()
