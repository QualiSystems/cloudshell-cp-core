from dataclasses import dataclass

from cloudshell.cp.core.requests.models import BaseConnectivityAction, BaseRequestObject


@dataclass
class PrepareCloudInfraParams(BaseRequestObject):
    cidr: str = ""


@dataclass
class PrepareCloudInfra(BaseConnectivityAction):
    actionParams: PrepareCloudInfraParams = None

    def get_sandbox_cidr(self):
        return self.actionParams.cidr
