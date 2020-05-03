from threading import Thread

from cloudshell.cp.core.models import DriverResponse, PrepareCloudInfra, PrepareCloudInfraResult, PrepareSubnet, \
    PrepareSubnetActionResult, CreateKeys, CreateKeysActionResult


class AbstractPrepareSandboxInfraFlow:
    def __init__(self, resource_config, logger):
        """

        :param resource_config:
        :param logger:
        """
        self._resource_config = resource_config
        self._logger = logger

    def prepare_cloud_infra(self, request_actions):
        """

        :param PrepareSandboxInfraRequestActions request_actions:
        :return:
        """
        raise NotImplementedError(f"Class {type(self)} must implement method 'prepare_cloud_infra'")

    def prepare_subnets(self, request_actions):
        """

        :param PrepareSandboxInfraRequestActions request_actions:
        :return:
        """
        raise NotImplementedError(f"Class {type(self)} must implement method 'prepare_subnet'")

    def create_ssh_keys(self, request_actions):
        """

        :param PrepareSandboxInfraRequestActions request_actions:
        :return: SSH Access key
        :rtype: str
        """
        raise NotImplementedError(f"Class {type(self)} must implement method 'create_ssh_keys'")

    def _prepare_cloud_infra(self, request_actions):
        """

        :param PrepareSandboxInfraRequestActions request_actions:
        :return:
        """
        action = request_actions.prepare_cloud_infra
        self.prepare_cloud_infra(request_actions)

        return PrepareCloudInfraResult(actionId=action.actionId)

    def _prepare_subnets(self, request_actions):
        """

        :param PrepareSandboxInfraRequestActions request_actions:
        :return:
        """
        self.prepare_subnets(request_actions)
        return [PrepareSubnetActionResult(actionId=action.actionId) for action in request_actions.prepare_subnets]

    def _create_ssh_keys(self, request_actions):
        """

        :param PrepareSandboxInfraRequestActions request_actions:
        :return:
        """
        action = request_actions.create_keys
        access_key = self.create_ssh_keys(action)

        return CreateKeysActionResult(actionId=action.actionId, accessKey=access_key)

    def prepare(self, request_actions):
        """

        :param cloudshell.cp.core.driver_request_parser.RequestActions request_actions:
        :return:
        """
        prep_network_action_result = self._prepare_cloud_infra(request_actions=request_actions)
        prep_subnet_action_result = self._prepare_subnets(request_actions=request_actions)
        access_keys_action_results = self._create_ssh_keys(request_actions=request_actions)

        action_results = [prep_network_action_result, prep_subnet_action_result, access_keys_action_results]
        return DriverResponse(action_results).to_driver_response_json()
