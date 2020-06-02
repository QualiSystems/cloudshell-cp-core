import concurrent

from cloudshell.cp.core.request_actions import DriverResponse
from cloudshell.cp.core.request_actions.models import (
    CreateKeysActionResult,
    PrepareCloudInfraResult,
    PrepareSubnetActionResult,
)


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
        raise NotImplementedError(
            f"Class {type(self)} must implement method 'prepare_cloud_infra'"
        )

    def prepare_subnets(self, request_actions):
        """

        :param PrepareSandboxInfraRequestActions request_actions:
        :return dictionary PrepareSubnet.actionId: subnet_id
        :rtype: dict[str, str]
        """
        raise NotImplementedError(
            f"Class {type(self)} must implement method 'prepare_subnet'"
        )

    def create_ssh_keys(self, request_actions):
        """

        :param PrepareSandboxInfraRequestActions request_actions:
        :return: SSH Access key
        :rtype: str
        """
        raise NotImplementedError(
            f"Class {type(self)} must implement method 'create_ssh_keys'"
        )

    def prepare_common_objects(self, request_actions):
        """

        :param request_actions:
        :return:
        """
        pass

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
        subnet_ids = self.prepare_subnets(request_actions)

        return [
            PrepareSubnetActionResult(
                actionId=action.actionId, subnetId=subnet_ids.get(action.actionId)
            )
            for action in request_actions.prepare_subnets
        ]

    def _create_ssh_keys(self, request_actions):
        """

        :param PrepareSandboxInfraRequestActions request_actions:
        :return:
        """
        action = request_actions.create_keys
        access_key = self.create_ssh_keys(action)

        return CreateKeysActionResult(actionId=action.actionId, accessKey=access_key)

    def prepare(self, request_actions):
        """ss

        :param cloudshell.cp.core.request_actions.PrepareSandboxInfraRequestActions request_actions:  # noqa: E501
        :return:
        """
        self.prepare_common_objects(request_actions=request_actions)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            prepare_cloud_infra_task = executor.submit(
                self._prepare_cloud_infra, request_actions=request_actions
            )
            prepare_subnets_task = executor.submit(
                self._prepare_subnets, request_actions=request_actions
            )
            create_ssh_keys_task = executor.submit(
                self._create_ssh_keys, request_actions=request_actions
            )

            concurrent.futures.wait(
                [prepare_cloud_infra_task, prepare_subnets_task, create_ssh_keys_task]
            )

            action_results = [
                prepare_cloud_infra_task.result(),
                create_ssh_keys_task.result(),
                *prepare_subnets_task.result(),
            ]

        return DriverResponse(action_results).to_driver_response_json()
