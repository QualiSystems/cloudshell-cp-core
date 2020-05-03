from dataclasses import dataclass

from cloudshell.cp.core.models.base import BaseRequestObject
from cloudshell.cp.core.models.connectivity import BaseConnectivityAction


@dataclass
class PrepareCloudInfraParams(BaseRequestObject):
    cidr: str = ""


@dataclass
class PrepareCloudInfra(BaseConnectivityAction):
    actionParams: PrepareCloudInfraParams = None

    def get_sandbox_cidr(self):
        return self.actionParams.cidr
