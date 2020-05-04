from cloudshell.cp.core.models import DeployAppResult, DriverResponse


class AbstractDeployVMFlow:
    def __init__(self, resource_config, logger):
        """

        :param resource_config:
        :param logger:
        """
        self._resource_config = resource_config
        self._logger = logger

    def deploy_vm(self, action):
        """

        :param cloudshell.cp.core.models.DeployApp action:
        :return:
        :rtype: tuple[str, str, dict, dict]
        """
        raise NotImplementedError(
            f"Class {type(self)} must implement method 'deploy_vm'"
        )

    def _deploy_vm(self, action):
        """

        :param cloudshell.cp.core.models.PrepareCloudInfra action:
        :return:
        """
        vm_uuid, vm_name, vm_details_data, deployedAppAdditionalData = self.deploy_vm(
            action
        )
        return DeployAppResult(
            action.actionId,
            vmUuid="",
            vmName="",
            vmDetailsData=None,
            deployedAppAdditionalData={},
        )

    def deploy(self, request_actions):
        """

        :param cloudshell.cp.core.driver_request_parser.RequestActions request_actions:
        :return:
        """
        deploy_result = self._deploy_vm(request_actions)
        return DriverResponse([deploy_result]).to_driver_response_json()
