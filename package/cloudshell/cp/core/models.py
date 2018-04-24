

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
        self.customActionAttributes = None # type: dict

class ConnectivityVlanActionBase(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.connectionId = ''          # type: str
        self.connectionParams = None    # type: SetVlanParameter
        self.connectorAttributes = None # type: dict

#endregion

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

#region PrepareSubnet

class PrepareSubnet(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.actionParams = None # type: PrepareSubnetParams

class PrepareSubnetParams(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.cidr = ''                    # type: str
        self.is_public = False            # type: bool
        self.alias = ''                   # type: str
        self.attributes = None            # type: dict

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
        self.subnet_id = ''                 # type: str
        self.is_public = False              # type: bool
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

class DeployNetworkingResultModel(object):
    def __init__(self, action_id):
        self.action_id = action_id  # type: str
        self.interface_id = ''  # type: str
        self.device_index = None  # type: int
        self.private_ip = ''  # type: str
        self.public_ip = ''  # type: str
        self.mac_address = ''  # type: str
        self.is_elastic_ip = False  # type: bool


class ConnectivityActionResult(object):
    def __init__(self):
        self.actionId = ''
        self.success = True
        self.infoMessage = ''
        self.errorMessage = ''


class PrepareCloudInfraResult(ConnectivityActionResult):
    def __init__(self):
        ConnectivityActionResult.__init__(self)
        self.type = 'PrepareNetwork'


class PrepareSubnetActionResult(ConnectivityActionResult):
    def __init__(self):
        ConnectivityActionResult.__init__(self)
        self.subnetId = ''


class ConnectToSubnetActionResult(ConnectivityActionResult):
    def __init__(self, action_id, success, interface_data, info='', error=''):
        ConnectivityActionResult.__init__(self)
        self.actionId = action_id  # type: str
        self.type = 'connectToSubnet'
        self.success = success
        self.interface = interface_data
        self.infoMessage = info
        self.errorMessage = error


class SetAppSecurityGroupActionResult(object):
    def __init__(self):
        self.appName = ''
        self.success = True
        self.error = ''

    #
    # def convert_to_json(self):
    #     result = {'appName': self.appName, 'error': self.error, 'success': self.success}
    #     return json.dumps(result)
    #
    # @staticmethod
    # def to_json(results):
    #     if not results:
    #         return
    #
    #     return json.dumps([r.__dict__ for r in results])



# endregion