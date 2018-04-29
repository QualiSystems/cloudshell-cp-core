

#region base

class RequestObjectBase(object):
    def __init__(self):
        pass

class RequestActionBase(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.actionId = '' # type: str

class ActionTarget(RequestObjectBase):
    def __init__(self):
        """
        :type fullAddress:  str
        :type fullName:  str
        """
        RequestObjectBase.__init__(self)
        self.fullAddress = '' # type: str
        self.fullName = ''    # type: str

class ConnectivityActionBase(RequestActionBase):
    def __init__(self):
        RequestActionBase.__init__(self)
        self.actionTarget = None           # type: ActionTarget

class ConnectivityVlanActionBase(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.connectionId = ''             # type: str
        self.connectionParams = None       # type: SetVlanParameter
        self.connectorAttributes = None    # type: dict
        self.customActionAttributes = None # type: dict

#endregion

#region Common

class Attribute(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.attributeName = ''  # type: str
        self.attributeValue = '' # type: str

# endregion
#region DeployApp

class DeployApp(RequestActionBase):
    def __init__(self):
        RequestActionBase.__init__(self)
        self.actionParams= None # type: DeployAppParams


class DeployAppParams(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.appName = ''       # type: str
        self.deployment = None  # type: DeployAppDeploymentInfo
        self.appResource = None # type: AppResourceInfo


class DeployAppDeploymentInfo(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.deploymentPath = '' # type: str
        self.attributes = None   # type: dict
        self.customModel = None  # type: object

class AppResourceInfo(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.attributes = None   # type: dict

#endregion
#region CreateKeys

class CreateKeys(RequestActionBase):
    def __init__(self):
        RequestActionBase.__init__(self)

#endregion
#region PrepareSubnet

class PrepareSubnet(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.actionParams = None # type: PrepareSubnetParams

class PrepareSubnetParams(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.cidr = ''                      # type: str
        self.isPublic = False               # type: bool
        self.alias = ''                     # type: str
        self.subnetServiceAttributes = None # type: dict

#endregion

#region CleanupNetwork

class CleanupNetwork(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)

#endregion

#region Vlan

class SetVlanParameter (RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.vlanId = ''                  # type: str
        self.mode = 0                     # type: int
        self.vlanServiceAttributes = None # type: dict

class RemoveVlan(ConnectivityVlanActionBase):
    def __init__(self):
        ConnectivityVlanActionBase.__init__(self)

class SetVlan(ConnectivityVlanActionBase):
    def __init__(self):
        ConnectivityVlanActionBase.__init__(self)

#endregion

#region ConnectSubnet

class ConnectSubnet(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.actionParams = None # type: ConnectToSubnetParams

class ConnectToSubnetParams(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.cidr = ''                      # type: str
        self.subnetId = ''                 # type: str
        self.isPublic = False              # type: bool
        self.subnetServiceAttributes = None # type: dict
        self.vnicName = ''                  # type: str

#endregion

#region PrepareCloudInfra

class PrepareCloudInfra(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.actionParams = None       # type: PrepareCloudInfraParams


class PrepareCloudInfraParams(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.cidr = ''  # type: str

#endregion

#region actions results

class ActionResultBase:
    def __init__(self, type,actionId = '',success = True ,infoMessage='',errorMessage = ''):
        self.actionId = actionId      # type: str
        self.success = success
        self.infoMessage = infoMessage
        self.errorMessage = errorMessage
        self.type = type

class DeployAppResult(ActionResultBase):
    def __init__(self,actionId = '',success = True ,infoMessage='',errorMessage = '',vm_uuid = '',vm_name = '',
                 deployed_app_address = '',deployed_app_attributes = None,deployed_app_additional_data = None,
                 vm_details_data = None):

        ActionResultBase.__init__(self, 'DeployApp',actionId,success,infoMessage,errorMessage)
        self.vmUuid = vm_uuid  # type: str
        self.vmName = vm_name  # type: str
        self.deployedAppAddress = deployed_app_address  # type: str
        self.deployedAppAttributes = deployed_app_attributes if deployed_app_attributes else [] # type: [Attribute]
        self.deployedAppAdditionalData = deployed_app_additional_data if deployed_app_additional_data else {} # type: dict
        self.vmDetailsData = vm_details_data  # type: VmDetailsData


class VmDetailsData(object):
    def __init__(self,vm_instance_data = None,vm_network_data = None):

        self.vmInstanceData =   vm_instance_data if  vm_instance_data  else  [] # type: [DeployVmDataElement]
        self.vmNetworkData  =   vm_network_data  if  vm_network_data   else  [] # type: [DeployVmNetworkInterfaceDataResponse]


class DeployVmDataElement(object):
    def __init__(self,key = '',value = '',hidden = False):
        self.key = key       # type: str
        self.value = value   # type: str
        self.hidden = hidden # type: bool

class DeployVmNetworkInterfaceDataResponse(object):
    def __init__(self,interface_id = '',network_id = '',is_primary = False,is_predefined = False,network_data = None):
        self.interfaceId = interface_id                            # type: str
        self.networkId = network_id                                # type: str
        self.isPrimary = is_primary                                # type: bool
        self.isPredefined = is_predefined                          # type: bool
        self.networkData =  network_data  if network_data  else [] # type: [DeployVmDataElement]

class PrepareCloudInfraResult(ActionResultBase):
    def __init__(self,actionId = '',success = True ,infoMessage='',errorMessage = ''):
        ActionResultBase.__init__(self, 'PrepareNetwork',actionId,success,infoMessage,errorMessage)


class PrepareSubnetActionResult(ActionResultBase):
    def __init__(self,actionId = '',success = True ,infoMessage='',errorMessage = '',subnet_id = ''):
        ActionResultBase.__init__(self, 'PrepareSubnet',actionId,success,infoMessage,errorMessage)
        self.subnetId = subnet_id


class ConnectToSubnetActionResult(ActionResultBase):
    def __init__(self,actionId = '',success = True ,infoMessage='',errorMessage = '',interface = ''):
        ActionResultBase.__init__(self, 'ConnectToSubnet',actionId,success,infoMessage,errorMessage)
        self.interface = interface


class CreateKeysActionResult(ActionResultBase):
    def __init__(self,actionId = '',success = True ,infoMessage='',errorMessage = '',access_key= '',subnet_id = ''):
        ActionResultBase.__init__(self, 'CreateKeys',actionId,success,infoMessage,errorMessage)
        self.accessKey= access_key   # type: str
        self.subnetId = subnet_id    # type: str

class SetAppSecurityGroupActionResult(ActionResultBase):
    def __init__(self,actionId = '',success = True ,infoMessage='',errorMessage = ''):
        ActionResultBase.__init__(self, 'SetAppSecurityGroup',actionId,success,infoMessage,errorMessage)

# endregion