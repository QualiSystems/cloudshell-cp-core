# region base
import json


class RequestObjectBase(object):
    def __init__(self):
        pass


class RequestActionBase(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.actionId = ''  # type: str

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class ActionTarget(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.fullAddress = ''  # type: str
        self.fullName = ''  # type: str


class ConnectivityActionBase(RequestActionBase):
    def __init__(self):
        RequestActionBase.__init__(self)
        self.actionTarget = None  # type: ActionTarget


class ConnectivityVlanActionBase(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.connectionId = ''  # type: str
        self.connectionParams = None  # type: SetVlanParameter
        self.connectorAttributes = None  # type: dict
        self.customActionAttributes = None  # type: dict


# endregion

# region Common

class Attribute(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.attributeName = ''  # type: str
        self.attributeValue = ''  # type: str


# endregion
# region DeployApp

class DeployApp(RequestActionBase):
    def __init__(self):
        RequestActionBase.__init__(self)
        self.actionParams = None  # type: DeployAppParams


class DeployAppParams(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.appName = ''  # type: str
        self.deployment = None  # type: DeployAppDeploymentInfo
        self.appResource = None  # type: AppResourceInfo


class DeployAppDeploymentInfo(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.deploymentPath = ''  # type: str
        self.attributes = None  # type: dict
        self.customModel = None  # type: object


class AppResourceInfo(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.attributes = None  # type: dict


# endregion
# region CreateKeys

class CreateKeys(RequestActionBase):
    def __init__(self):
        RequestActionBase.__init__(self)


# endregion
# region PrepareSubnet

class PrepareSubnet(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.actionParams = None  # type: PrepareSubnetParams


class PrepareSubnetParams(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.cidr = ''  # type: str
        self.isPublic = False  # type: bool
        self.alias = ''  # type: str
        self.subnetServiceAttributes = None  # type: dict


# endregion

# region CleanupNetwork

class CleanupNetwork(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)


# endregion

# region Vlan

class SetVlanParameter(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.vlanId = ''  # type: str
        self.mode = 0  # type: int
        self.vlanServiceAttributes = None  # type: dict


class RemoveVlan(ConnectivityVlanActionBase):
    def __init__(self):
        ConnectivityVlanActionBase.__init__(self)


class SetVlan(ConnectivityVlanActionBase):
    def __init__(self):
        ConnectivityVlanActionBase.__init__(self)


# endregion

# region ConnectSubnet

class ConnectSubnet(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.actionParams = None  # type: ConnectToSubnetParams


class ConnectToSubnetParams(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.cidr = ''  # type: str
        self.subnetId = ''  # type: str
        self.isPublic = False  # type: bool
        self.subnetServiceAttributes = None  # type: dict
        self.vnicName = ''  # type: str


# endregion

# region PrepareCloudInfra

class PrepareCloudInfra(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.actionParams = None  # type: PrepareCloudInfraParams


class PrepareCloudInfraParams(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.cidr = ''  # type: str


# endregion

# region actions results

class ActionResultBase:
    def __init__(self, type, actionId='', success=True, infoMessage='', errorMessage=''):
        """
        :param type:         str
        :param actionId:     str
        :param success:      bool
        :param infoMessage:  str
        :param errorMessage: str
        """
        self.actionId = actionId  # type: str
        self.success = success
        self.infoMessage = infoMessage
        self.errorMessage = errorMessage
        self.type = type


class DeployAppResult(ActionResultBase):
    def __init__(self, actionId='', success=True, infoMessage='', errorMessage='', vmUuid='', vmName='',
                 deployedAppAddress='', deployedAppAttributes=None, deployedAppAdditionalData=None,
                 vmDetailsData=None):
        """
        :param actionId:                  str
        :param success:                   bool
        :param infoMessage:               str
        :param errorMessage:              str
        :param vmUuid:                    str
        :param vmName:                    str
        :param deployedAppAddress:        str
        :param deployedAppAttributes:     [Attribute]
        :param deployedAppAdditionalData: dict
        :param vmDetailsData:             VmDetailsData
        """
        ActionResultBase.__init__(self, 'DeployApp', actionId, success, infoMessage, errorMessage)
        self.vmUuid = vmUuid  # type: str
        self.vmName = vmName  # type: str
        self.deployedAppAddress = deployedAppAddress  # type: str
        self.deployedAppAttributes = deployedAppAttributes if deployedAppAttributes else []  # type: [Attribute]
        self.deployedAppAdditionalData = deployedAppAdditionalData if deployedAppAdditionalData else {}  # type: dict
        self.vmDetailsData = vmDetailsData  # type: VmDetailsData


class VmDetailsData(object):
    def __init__(self, vmInstanceData=None, vmNetworkData=None):
        """
        :param vmInstanceData: [DeployVmDataElement]
        :param vmNetworkData:  [DeployVmNetworkInterfaceDataResponse]
        """

        self.vmInstanceData = vmInstanceData if vmInstanceData else []  # type: [DeployVmDataElement]
        self.vmNetworkData = vmNetworkData if vmNetworkData else []  # type: [DeployVmNetworkInterfaceDataResponse]


class DeployVmDataElement(object):
    def __init__(self, key='', value='', hidden=False):
        """
        :param key:    str
        :param value:  str
        :param hidden: bool
        """
        self.key = key  # type: str
        self.value = value  # type: str
        self.hidden = hidden  # type: bool


class DeployVmNetworkInterfaceDataResponse(object):
    def __init__(self, interfaceId='', networkId='', isPrimary=False, isPredefined=False, networkData=None):
        """
        :param interfaceId:  str
        :param networkId:    str
        :param isPrimary:    bool
        :param isPredefined: bool
        :param networkData:  [DeployVmDataElement]
        """
        self.interfaceId = interfaceId  # type: str
        self.networkId = networkId  # type: str
        self.isPrimary = isPrimary  # type: bool
        self.isPredefined = isPredefined  # type: bool
        self.networkData = networkData if networkData else []  # type: [DeployVmDataElement]


class PrepareCloudInfraResult(ActionResultBase):
    def __init__(self, actionId='', success=True, infoMessage='', errorMessage=''):
        ActionResultBase.__init__(self, 'PrepareNetwork', actionId, success, infoMessage, errorMessage)


class PrepareSubnetActionResult(ActionResultBase):
    def __init__(self, actionId='', success=True, infoMessage='', errorMessage='', subnet_id=''):
        ActionResultBase.__init__(self, 'PrepareSubnet', actionId, success, infoMessage, errorMessage)
        self.subnetId = subnet_id


class ConnectToSubnetActionResult(ActionResultBase):
    def __init__(self, actionId='', success=True, infoMessage='', errorMessage='', interface=''):
        ActionResultBase.__init__(self, 'ConnectToSubnet', actionId, success, infoMessage, errorMessage)
        self.interface = interface


class CreateKeysActionResult(ActionResultBase):
    def __init__(self, actionId='', success=True, infoMessage='', errorMessage='', accessKey=''):
        """
        :param accessKey: str
        """
        ActionResultBase.__init__(self, 'CreateKeys', actionId, success, infoMessage, errorMessage)
        self.accessKey = accessKey  # type: str


class SetAppSecurityGroupActionResult(ActionResultBase):
    def __init__(self, actionId='', success=True, infoMessage='', errorMessage=''):
        ActionResultBase.__init__(self, 'SetAppSecurityGroup', actionId, success, infoMessage, errorMessage)

# endregion
