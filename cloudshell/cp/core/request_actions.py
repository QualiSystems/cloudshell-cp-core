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
            except KeyError:
                parsed_params = {}
                for param_key, param in data.items():
                    parsed_params[param_key] = cls._parse(data=param, cs_api=cs_api)

                return parsed_params

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

        elif isinstance(data, str):
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

        obj.connect_subnets.sort(key=lambda x: x.device_index)

        return obj


@dataclass
class VMDetails:
    id: str
    cloud_provider_id: str
    uid: str
    vm_custom_params: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data):
        """

        :param data:
        :return:
        """
        return cls(id=data["id"],
                   cloud_provider_id=data["cloudProviderId"],
                   uid=data["uid"],
                   vm_custom_params=data["vmCustomParams"])


@dataclass
class DeployedApp:
    PUBLIC_IP_KEY = "Public IP"

    name: str
    deployment_service_model: str
    private_ip: str
    attributes: dict = field(default_factory=dict)
    vmdetails: VMDetails = None

    @property
    def user(self):
        return self.attributes["User"]

    @property
    def password(self):
        return self.attributes["Password"]

    @property
    def public_ip(self):
        return self.attributes[self.PUBLIC_IP_KEY]

    @classmethod
    def from_data(cls, app_request_data, deployed_app_data):
        """

        :param dict app_request_data:
        :param dict deployed_app_data:
        :return:
        """
        attributes = {attr["name"]: attr["value"]
                      for attr in deployed_app_data["attributes"]}

        return cls(name=deployed_app_data["name"],
                   deployment_service_model=app_request_data["deploymentService"]["model"],
                   private_ip=deployed_app_data["address"],
                   attributes=attributes,
                   vmdetails=VMDetails.from_dict(deployed_app_data["vmdetails"]))

    @classmethod
    def from_remote_resource(cls, resource):
        """

        :param resource:
        :return:
        """
        return cls.from_data(app_request_data=json.loads(resource.app_context.app_request_json),
                             deployed_app_data=json.loads(resource.app_context.deployed_app_json))


@dataclass
class GetVMDetailsRequestActions:
    deployed_apps: list = field(default_factory=list)

    @classmethod
    def from_request(cls, request):
        data = json.loads(request)
        deployed_apps = []
        for item in data["items"]:
            deployed_app = DeployedApp.from_data(app_request_data=item["appRequestJson"],
                                                 deployed_app_data=item["deployedAppJson"])
            deployed_apps.append(deployed_app)

        return cls(deployed_apps=deployed_apps)


@dataclass
class CleanupSandboxInfraRequestActions(BaseRequestActions):
    cleanup_network: models.CleanupNetwork = None

    @classmethod
    def from_request(cls, request, cs_api=None):
        request = json.loads(request)
        actions = cls._parse(data=request["driverRequest"].get("actions", []), cs_api=cs_api)
        obj = cls()

        for action in actions:
            if isinstance(action, models.CleanupNetwork):
                obj.cleanup_network = action

        return obj


@dataclass
class SetAppSecurityGroupsRequestActions(BaseRequestActions):
    @classmethod
    def from_request(cls, request, cs_api=None):
        request = json.loads(request)
        actions = cls._parse(data=request["driverRequest"].get("actions", []), cs_api=cs_api)
        obj = cls()
        cls.actions = actions
        #
        # for action in actions:
        #     if isinstance(action, models.CleanupNetwork):
        #         obj.cleanup_network = action

        return obj

        security_group_models = []

        security_groups = AzureModelsParser.get_app_security_groups_from_request(request)

        for security_group in security_groups:
            security_group_model = AppSecurityGroupModel()
            security_group_model.deployed_app = DeployedApp()
            security_group_model.deployed_app.name = security_group.deployedApp.name
            security_group_model.deployed_app.vm_details = VmDetails()
            security_group_model.deployed_app.vm_details.uid = security_group.deployedApp.vmdetails.uid
            security_group_model.security_group_configurations = SecurityGroupParser.parse_security_group_configurations(
                security_group.securityGroupsConfigurations)

            security_group_models.append(security_group_model)

        return security_group_models