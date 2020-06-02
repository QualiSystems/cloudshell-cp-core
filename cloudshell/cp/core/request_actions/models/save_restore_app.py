from dataclasses import dataclass, field

from cloudshell.cp.core.requests.models import BaseRequestAction, BaseRequestObject


@dataclass
class SaveAppParams(BaseRequestObject):
    saveDeploymentModel: str = ""
    savedSandboxId: str = ""
    sourceVmUuid: str = ""
    sourceAppName: str = ""
    deploymentPathAttributes: list = field(default_factory=list)


@dataclass
class SaveApp(BaseRequestAction):
    actionParams: SaveAppParams = None


@dataclass
class DeleteSavedAppParams(BaseRequestObject):
    saveDeploymentModel: str = ""
    savedSandboxId: str = ""
    artifacts: list = field(default_factory=list)
    savedAppName: str = ""


@dataclass
class DeleteSavedApp(BaseRequestAction):
    actionParams: DeleteSavedAppParams = None
