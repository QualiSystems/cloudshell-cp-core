import json
import sys


VNIC_NAME_ATTRIBUTE = "Vnic Name"

class RequestObjectBase(object):
    def __init__(self):
        pass
        # self.type = self.__class__.__name__
        # self.type = ''

class RequestActionBase(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.actionId = ''

class ActionTarget(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.fullAddress = ''
        self.fullName = ''

class ConnectivityActionBase(RequestActionBase):
    def __init__(self):
        RequestActionBase.__init__(self)
        self.actionTarget = None
        self.customActionAttributes = []

class PrepareSubnet(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.connectionParams = None

class PrepareNetwork(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.connectionParams = None

class CleanupNetwork(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.connectionParams = None

class RemoveVlan(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.connectionId = ''
        self.connectionParams = None
        self.connectorAttributes = []

class SetVlan(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.connectionId = ''
        self.connectionParams = None
        self.connectorAttributes = []

class ConnectSubnet(ConnectivityActionBase):
    def __init__(self):
        ConnectivityActionBase.__init__(self)
        self.connectionParams = None

class SetVlanParameter (RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.vlanId = ''
        self.mode = 0
        self.vlanServiceAttributes = []

class ConnectionParamsBase(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.cidr = ''  # type: str
        self.subnetServiceAttributes = []  # type: list[NetworkActionAttribute]
        self.custom_attributes = []  # type: list[NetworkActionAttribute]


class SubnetConnectionParams(ConnectionParamsBase):
    def __init__(self):
        ConnectionParamsBase.__init__(self)
        self.subnet_id = ''

class PrepareSubnetParams(ConnectionParamsBase):
    def __init__(self, cidr=None, alias='', is_public=True):
        """
        :param str cidr:
        :param str alias:
        :param bool is_public:
        """
        ConnectionParamsBase.__init__(self)
        self.cidr = cidr
        self.is_public = is_public
        self.alias = alias


class PrepareNetwork(RequestActionBase):
    def __init__(self):
        RequestActionBase.__init__(self)
        self.actionId = ''
        self.customActionAttributes = []
        self.connectionParams = None


class PrepareNetworkParams(ConnectionParamsBase):
    def __init__(self):
        ConnectionParamsBase.__init__(self)
        del self.subnetServiceAttributes


class NetworkActionAttribute(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.name = ''
        self.value = ''


class NetworkAction(RequestObjectBase):
    def __init__(self, id=None, type=None, connection_params=None):
        """
        :param str id:
        :param str type:
        :param ConnectionParamsBase connection_params:
        """
        RequestObjectBase.__init__(self)
        self.id = id or ''
        self.type = type or ''
        self.connection_params = connection_params

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


class PrepareNetworkActionResult(ConnectivityActionResult):
    def __init__(self):
        ConnectivityActionResult.__init__(self)
        self.vpcId = ''
        self.securityGroupId = ''
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

    def convert_to_json(self):
        result = {'appName': self.appName, 'error': self.error, 'success': self.success}
        return json.dumps(result)

    @staticmethod
    def to_json(results):
        if not results:
            return

        return json.dumps([r.__dict__ for r in results])


class DeployApp(RequestActionBase):
    def __init__(self):
        """
                :param str id:
                :param str type:
                :param actionParams action_params:
                """
        RequestActionBase.__init__(self)
        self.id =  ''
        self.type = ''
        self.actionParams= None



class DeployAppParams(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.appName = ''
        self.deployment = None
        self.appResource = None


class DeployAppDeploymentInfo(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.deploymentPath = ''
        self.attributes = None
        self.customModel = None


class AppResourceInfo(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.attributes = None


class Attributes(RequestObjectBase):
    def __init__(self):
        RequestObjectBase.__init__(self)
        self.attributeName = ''
        self.attributeValue = ''

class VlanServiceAttribute(Attributes):
    def __init__(self):
        Attributes.__init__(self)


class ConnectorAttribute(Attributes):
    def __init__(self):
        Attributes.__init__(self)

class CustomAttribute(Attributes):
    def __init__(self):
        Attributes.__init__(self)
