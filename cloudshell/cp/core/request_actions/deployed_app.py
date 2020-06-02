import itertools
import json
from dataclasses import dataclass, field


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
        return cls(
            id=data["id"],
            cloud_provider_id=data["cloudProviderId"],
            uid=data["uid"],
            vm_custom_params=data["vmCustomParams"],
        )


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
    def allow_all_sandbox_traffic(self):
        return (
            self.attributes[
                f"{self.deployment_service_model}.AllowallSandboxTraffic"
            ].lower()
            == "true"
        )

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
        attributes = {
            attr["name"]: attr["value"]
            for attr in itertools.chain(
                deployed_app_data["attributes"],
                app_request_data["deploymentService"]["attributes"],
            )
        }

        return cls(
            name=deployed_app_data["name"],
            deployment_service_model=app_request_data["deploymentService"]["model"],
            private_ip=deployed_app_data["address"],
            attributes=attributes,
            vmdetails=VMDetails.from_dict(deployed_app_data["vmdetails"]),
        )

    @classmethod
    def from_remote_resource(cls, resource):
        """

        :param resource:
        :return:
        """
        return cls.from_data(
            app_request_data=json.loads(resource.app_context.app_request_json),
            deployed_app_data=json.loads(resource.app_context.deployed_app_json),
        )
