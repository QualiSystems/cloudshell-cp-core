from dataclasses import dataclass, field


@dataclass
class VMDetails:
    id: str  # noqa: A003
    cloud_provider_id: str
    uid: str
    vm_custom_params: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data):
        """Create VMDetails from the dictionary data.

        :param dict data:
        :rtype: VMDetails
        """
        return cls(
            id=data.get("id"),
            cloud_provider_id=data.get("cloudProviderId"),
            uid=data.get("uid"),
            vm_custom_params=data.get("vmCustomParams"),
        )


@dataclass
class DeployedApp:
    DEPLOYMENT_PATH = ""
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
                f"{self.deployment_service_model}.Allow all Sandbox Traffic"
            ].lower()
            == "true"
        )

    @property
    def public_ip(self):
        return self.attributes[self.PUBLIC_IP_KEY]
