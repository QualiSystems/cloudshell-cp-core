from dataclasses import dataclass, field
from typing import Any

from cloudshell.cp.core.models.base import BaseRequestAction, BaseRequestObject


@dataclass
class SetVlanParameter(BaseRequestObject):
    vlanId: str = ""
    mode: int = 0
    vlanServiceAttributes: dict = field(default_factory=dict)


@dataclass
class ActionTarget(BaseRequestObject):
    fullAddress: str = ""
    fullName: str = ""


@dataclass
class BaseConnectivityAction(BaseRequestAction):
    actionTarget: ActionTarget = None
    actionParams: Any = None

    def is_private(self):
        public = True
        if self.actionParams.subnetServiceAttributes is not None:
            public = self.actionParams.subnetServiceAttributes.get("Public", public)

        return public is False


@dataclass
class BaseConnectivityVlanAction(BaseConnectivityAction):
    connectionId: str = ""
    connectionParams: SetVlanParameter = None
    connectorAttributes: dict = field(default_factory=dict)
    customActionAttributes: dict = field(default_factory=dict)


@dataclass
class CleanupNetwork(BaseConnectivityAction):
    customActionAttributes: list = field(default_factory=list)


@dataclass
class RemoveVlan(BaseConnectivityVlanAction):
    pass


@dataclass
class SetVlan(BaseConnectivityVlanAction):
    pass


@dataclass
class ConnectToSubnetParams(BaseRequestObject):
    cidr: str = ""
    subnetId: str = ""
    isPublic: bool = True
    subnetServiceAttributes: dict = field(default_factory=dict)
    vnicName: str = ""


@dataclass
class ConnectSubnet(BaseConnectivityAction):
    actionParams: ConnectToSubnetParams = None
