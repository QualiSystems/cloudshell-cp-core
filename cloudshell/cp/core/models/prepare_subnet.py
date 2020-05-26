from dataclasses import dataclass, field

from cloudshell.cp.core.models.base import BaseRequestObject
from cloudshell.cp.core.models.connectivity import BaseConnectivityAction


@dataclass
class PrepareSubnetParams(BaseRequestObject):
    cidr: str = ""
    isPublic: bool = True
    alias: str = ""
    subnetServiceAttributes: dict = field(default_factory=dict)


@dataclass
class PrepareSubnet(BaseConnectivityAction):
    actionParams: PrepareSubnetParams = None

    def get_cidr(self):
        return self.actionParams.cidr
