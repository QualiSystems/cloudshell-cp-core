from dataclasses import dataclass, field

from cloudshell.cp.core.requests.models import BaseRequestObject
from cloudshell.cp.core.requests.models import BaseConnectivityAction


@dataclass
class PrepareSubnetParams(BaseRequestObject):
    cidr: str = ""
    isPublic: bool = True
    alias: str = ""
    subnetServiceAttributes: list = field(default_factory=list)


@dataclass
class PrepareSubnet(BaseConnectivityAction):
    actionParams: PrepareSubnetParams = None
    attributes: dict = field(default_factory=dict)

    def __post_init__(self):
        for attr in self.actionParams.subnetServiceAttributes:
            self.attributes[attr.attributeName] = attr.attributeValue

    def get_cidr(self):
        return self.actionParams.cidr

    def is_private(self):
        return self.attributes.get("Public", True) is False
