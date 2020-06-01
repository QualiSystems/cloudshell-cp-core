import jsonpickle as jsonpickle


class AbstractVMDetailsFlow:
    def __init__(self, resource_config, logger):
        """

        :param resource_config:
        :param logger:
        """
        self._resource_config = resource_config
        self._logger = logger

    def _get_vm_details(self, deployed_app):
        """

        :param cloudshell.cp.core.request_actions.DeployedApp deployed_app:
        :rtype: cloudshell.cp.core.models.VmDetailsData
        """
        raise NotImplementedError(
            f"Class {type(self)} must implement method '_get_vm_details'"
        )

    def get_vm_details(self, request_actions):
        """

        :param cloudshell.cp.core.driver_request_parser.RequestActions request_actions:
        :return:
        """
        results = []

        for deployed_app in request_actions.deployed_apps:
            vm_details_data = self._get_vm_details(deployed_app=deployed_app)
            results.append(vm_details_data)

        return jsonpickle.encode(results)
