import json
from dataclasses import dataclass, field

from cloudshell.cp.core.requests import models
from cloudshell.cp.core.requests.actions.base import BaseRequestActions


@dataclass
class DeployVMRequestActions(BaseRequestActions):
    deploy_app: models.DeployApp = None
    connect_subnets: list = field(default_factory=list)

    @classmethod
    def register_deployment_path(cls, deployment_path_cls):
        """

        :param deployment_path_cls:
        :return:
        """
        cls.REGISTERED_DEPLOYMENT_PATH_MODELS[
            deployment_path_cls.DEPLOYMENT_PATH
        ] = deployment_path_cls

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
            if isinstance(action, models.DeployApp):
                obj.deploy_app = action
            elif isinstance(actions, models.ConnectSubnet):
                obj.connect_subnets.append(action)

        obj.connect_subnets.sort(key=lambda x: x.device_index)

        return obj
