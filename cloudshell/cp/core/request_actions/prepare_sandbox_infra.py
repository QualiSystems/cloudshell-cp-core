import json
from dataclasses import dataclass, field

from cloudshell.cp.core.requests import models
from cloudshell.cp.core.requests.actions.base import BaseRequestActions


@dataclass
class PrepareSandboxInfraRequestActions(BaseRequestActions):
    prepare_cloud_infra: models.PrepareCloudInfra = None
    prepare_subnets: list = field(default_factory=list)
    create_keys: models.CreateKeys = None

    @property
    def sandbox_cidr(self):
        return self.prepare_cloud_infra.get_sandbox_cidr()

    @property
    def prepare_private_subnets(self):
        return [
            subnet_action
            for subnet_action in self.prepare_subnets
            if subnet_action.is_private()
        ]

    @classmethod
    def from_request(cls, request, cs_api=None):
        """

        :param request:
        :param cs_api:
        :return:
        """
        actions = cls._parse_request_actions(request=request, cs_api=cs_api)
        obj = cls()

        for action in actions:
            if isinstance(action, models.PrepareCloudInfra):
                obj.prepare_cloud_infra = action
            elif isinstance(action, models.PrepareSubnet):
                obj.prepare_subnets.append(action)
            elif isinstance(action, models.CreateKeys):
                obj.create_keys = action

        return obj
