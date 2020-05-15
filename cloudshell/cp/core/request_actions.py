import json
from dataclasses import dataclass, field

from cloudshell.cp.core import models


class BaseRequestActions:
    REGISTERED_DEPLOYMENT_PATH_MODELS = {}

    @classmethod
    def from_request(cls, request, cs_api=None):
        request = json.loads(request)
        actions = cls._parse(data=request["driverRequest"].get("actions", []), cs_api=cs_api)
        return cls()

    @classmethod
    def _normalize_class_name(cls, class_name):
        """

        :param str class_name:
        :return:
        """
        return class_name[0].upper() + class_name[1:]

    @classmethod
    def _parse(cls, data, cs_api=None):
        """

        :param data:
        :return:
        """
        if isinstance(data, list):
            parsed_data = []
            for nested_data in data:
                parsed_data.append(cls._parse(data=nested_data, cs_api=cs_api))

            return parsed_data

        elif isinstance(data, dict):
            try:
                class_name = cls._normalize_class_name(data.pop("type"))
                parsed_kwargs = cls._parse(data=data, cs_api=cs_api)
                parsed_cls = getattr(models, class_name)

                if issubclass(parsed_cls, models.DeployApp):
                    parsed_cls = cls.REGISTERED_DEPLOYMENT_PATH_MODELS.get(
                        parsed_kwargs["actionParams"].deployment.deploymentPath,
                        parsed_cls,
                    )
                    parsed_obj = parsed_cls(**parsed_kwargs)
                    parsed_obj.set_cloudshell_api(api=cs_api)
                else:
                    parsed_obj = parsed_cls(**parsed_kwargs)

                return parsed_obj

            except KeyError:
                parsed_params = {}

                for param_key, param in data.items():
                    parsed_params[param_key] = cls._parse(data=param, cs_api=cs_api)

                return parsed_params

        if data.lower() in ("true", "false"):
            data = data.lower() == "true"

        return data


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
        request = json.loads(request)
        actions = cls._parse(data=request["driverRequest"].get("actions", []))
        obj = cls()

        for action in actions:
            if isinstance(action, models.PrepareCloudInfra):
                obj.prepare_cloud_infra = action
            elif isinstance(action, models.PrepareSubnet):
                obj.prepare_subnets.append(action)
            elif isinstance(action, models.CreateKeys):
                obj.create_keys = action

        return obj


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
        request = json.loads(request)
        actions = cls._parse(data=request["driverRequest"].get("actions", []), cs_api=cs_api)
        obj = cls()

        for action in actions:
            if isinstance(action, models.DeployApp):
                obj.deploy_app = action
            elif isinstance(actions, models.ConnectSubnet):
                obj.connect_subnets.append(action)

        return obj
