from dataclasses import dataclass, field

from cloudshell.cp.core.models.base import BaseRequestAction, BaseRequestObject

# TODO: move models to the corresponding modules !!!


@dataclass
class BaseActionResult(BaseRequestAction):
    type: str = ""
    actionId: str = ""
    success: bool = True
    infoMessage: str = ""
    errorMessage: str = ""


@dataclass
class VmDetailsData:
    vmInstanceData: list = field(default_factory=list)
    vmNetworkData: list = field(default_factory=list)
    appName: str = ""
    errorMessage: str = ""


@dataclass
class DeployAppResult(BaseActionResult):
    type: str = "DeployApp"
    vmUuid: str = ""
    vmName: str = ""
    deployedAppAddress: str = ""
    deployedAppAttributes: list = field(default_factory=list)
    deployedAppAdditionalData: dict = field(default_factory=dict)
    vmDetailsData: VmDetailsData = None


@dataclass
class VmDetailsProperty(object):
    key: str = ""
    value: str = ""
    hidden: bool = False


@dataclass
class VmDetailsNetworkInterface(BaseRequestObject):
    interfaceId: str = ""
    networkId: str = ""
    isPrimary: bool = False
    isPredefined: bool = False
    networkData: list = field(default_factory=list)
    privateIpAddress: str = ""
    publicIpAddress: str = ""


@dataclass
class PrepareCloudInfraResult(BaseActionResult):
    type: str = "PrepareNetwork"


@dataclass
class PrepareSubnetActionResult(BaseActionResult):
    type: str = "PrepareSubnet"
    subnetId: str = ""


@dataclass
class ConnectToSubnetActionResult(BaseActionResult):
    type: str = "ConnectToSubnet"
    interface: str = ""


@dataclass
class CreateKeysActionResult(BaseActionResult):
    type: str = "CreateKeys"
    accessKey: str = ""


@dataclass
class SetAppSecurityGroupActionResult(BaseActionResult):
    type: str = "SetAppSecurityGroup"


@dataclass
class SaveAppResult(BaseActionResult):
    artifacts: list = field(default_factory=list)
    savedEntityAttributes: list = field(default_factory=list)
    additionalData: list = field(default_factory=list)


@dataclass
class SetVlanResult(BaseActionResult):
    type: str = "setVlan"
    updatedInterface: str = ""


@dataclass
class RemoveVlanResult(BaseActionResult):
    type: str = "removeVlan"


@dataclass
class CleanupNetworkResult(BaseActionResult):
    type: str = "CleanupNetwork"


@dataclass
class TrafficMirroringResult(BaseActionResult):
    type: str = "CreateTrafficMirroring"
    sessionId: str = ""


@dataclass
class RemoveTrafficMirroringResult(BaseActionResult):
    type: str = "RemoveTrafficMirroring"


@dataclass
class Artifact(BaseRequestObject):
    artifactRef: str = ""
    artifactName: str = ""


@dataclass
class DataElement:
    name: str
    value: str
