import jsonpickle as jsonpickle


class AbstractVMDetailsFlow:
    def __init__(self, logger):
        """Init command.

        :param logging.Logger logger:
        """
        self._logger = logger

    def _get_vm_details(self, deployed_app):
        """Get VM Details.

        :param cloudshell.cp.core.request_actions.DeployedApp deployed_app:
        :rtype: cloudshell.cp.core.request_actions.models.VmDetailsData
        """
        raise NotImplementedError(
            f"Class {type(self)} must implement method '_get_vm_details'"
        )

    def get_vm_details(self, request_actions):
        """Get VM Details.

        :param cloudshell.cp.core.request_actions.GetVMDetailsRequestActions request_actions:  # noqa: E501
        :rtype: str
        """
        results = []

        for deployed_app in request_actions.deployed_apps:
            vm_details_data = self._get_vm_details(deployed_app=deployed_app)
            results.append(vm_details_data)

        return jsonpickle.encode(results)
