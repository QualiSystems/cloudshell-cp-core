from unittest import TestCase

from  cloudshell.cp.core.converters import *
from cloudshell.cp.core.models import *
from cloudshell.cp.core.utils  import *

from mock import Mock, patch


class CustomModel():
    __deploymentModel__ = "VCenter Deploy VM From Linked Clone"

    def __init__(self, attributes):
        self.auto_power_off = ''
        self.autoload = ''

        for k,v in attributes.iteritems():
                try_set_attr(self, to_snake_case(k), v)


class TestCloudShellCpCore(TestCase):

    def test_custom_deployment_model(self):

        atts_json  = '[{"attributeName":"Auto Delete","attributeValue":"True","type":"attributes"},{"attributeName":"Autoload","attributeValue":"True","type":"attributes"},{"attributeName":"IP Regex","attributeValue":"","type":"attributes"},{"attributeName":"Refresh IP Timeout","attributeValue":"600","type":"attributes"},{"attributeName":"vCenter VM","attributeValue":"Tor/Temps/ImageMonoNew","type":"attributes"},{"attributeName":"vCenter VM Snapshot","attributeValue":"1","type":"attributes"},{"attributeName":"VM Cluster","attributeValue":"","type":"attributes"},{"attributeName":"VM Storage","attributeValue":"","type":"attributes"},{"attributeName":"VM Resource Pool","attributeValue":"","type":"attributes"},{"attributeName":"VM Location","attributeValue":"","type":"attributes"},{"attributeName":"Auto Power On","attributeValue":"True","type":"attributes"},{"attributeName":"Auto Power Off","attributeValue":"True","type":"attributes"},{"attributeName":"Wait for IP","attributeValue":"True","type":"attributes"}]'
        deploy_req_json = '{"driverRequest":{"actions":[{"actionParams":{"appName":"vCenter_CVC_Support","deployment":{"deploymentPath":"VCenter Deploy VM From Linked Clone","attributes": ' + atts_json +' ,"type":"deployAppDeploymentInfo"},"appResource":{"attributes":[{"attributeName":"Password","attributeValue":"3M3u7nkDzxWb0aJ/IZYeWw==","type":"attributes"},{"attributeName":"Public IP","attributeValue":"","type":"attributes"},{"attributeName":"User","attributeValue":"","type":"attributes"}],"type":"appResourceInfo"},"type":"deployAppParams"},"actionId":"7808cf76-b8c5-4392-b571-5da99836b84b","type":"deployApp"}]}}'
        deploy_req = json.loads(deploy_req_json)

        parser = DriverRequestParser()
        parser.add_deployment_model(CustomModel)

        action = parser.convert_driver_request_to_actions(deploy_req)[0]

        # for k,v in atts_map:
        #     k = to_snake_case(k)
        #     attr_value = getattr(action.actionParams.deployment.customModel,k)
        #     self.assertTrue(attr_value,v)

        self.assertTrue(action.actionParams.deployment.customModel.autoload, 'True')
        self.assertTrue(action.actionParams.deployment.customModel.auto_power_off , 'True')

    def test_deploy_request(self):
        # prepare
        json_req = '{  "driverRequest": {"actions": [{"connectionId":"2e85db89-f1c9-4da2-b738-6ed57d7c8ec6","connectionParams":{"vlanId":["2"],"mode":"Access","type":"setVlanParameter"},"connectorAttributes":[{"attributeName":"Interface","attributeValue":"00:50:56:a2:3c:83","type":"connectorAttribute"}],"actionId":"27409903-4d80-4607-8be2-8140285f87e6","actionTarget":{"fullName":"VM Deployment_6693d80d","fullAddress":"N/A","type":"actionTarget"},"customActionAttributes":[{"attributeName":"VM_UUID","attributeValue":"422279ec-e35a-b63f-591a-5e748514056d","type":"customAttribute"}],"type":"removeVlan"},{"connectionId":"2e85db89-f1c9-4da2-b738-6ed57d7c8ec6","connectionParams":{"vlanId":["2"],"mode":"Access","type":"setVlanParameter"},"connectorAttributes":[{"attributeName":"Interface","attributeValue":"00:50:56:a2:4f:e2","type":"connectorAttribute"}],"actionId":"20d37283-3f90-4d5b-a949-5851629f20e6","actionTarget":{"fullName":"VM Deployment_44256851","fullAddress":"N/A","type":"actionTarget"},"customActionAttributes":[{"attributeName":"VM_UUID","attributeValue":"422217cb-1de3-1faf-bc42-401e9ecee942","type":"customAttribute"}],"type":"removeVlan"},{"actionId":"vlan1%<=>%resourceA","type":"setVlan","actionTarget":{"fullName":"Chassis1/Blade1/port1","fullAddress":"1/2/3","type":"actionTarget" },"connectionId":"vlan1%<=>%resourceA","connectionParams":{"type":"setVlanParameter","vlanId":["100-200","300"],"mode":"Trunk","vlanServiceAttributes":[{"type":"connectorAttribute","attributeName":"Mode","attributeValue":"Trunk"},{"type":"connectorAttribute","attributeName":"Allocation Ranges","attributeValue":"2-2000"}]},"connectorAttributes":[{"type":"vlanServiceAttribute","attributeName":"QNQ","attributeValue":"Enabled"}]},{"actionId":"4e3931f1-3f52-4505-b39d-0345c9839603","type":"prepareNetwork","connectionParams":{"type":"prepareNetworkParams","cidr":"10.0.5.0/24"},"customActionAttributes":[]},  {"actionParams": {  "appName": "vCenter_CVC_Support",  "deployment": {"deploymentPath": "VCenter Deploy VM From Linked Clone","attributes": [  {"attributeName": "Auto Delete","attributeValue": "True","type": "attributes"  },  {"attributeName": "Autoload","attributeValue": "True","type": "attributes"  },  {"attributeName": "IP Regex","attributeValue": "","type": "attributes"  },  {"attributeName": "Refresh IP Timeout","attributeValue": "600","type": "attributes"  },  {"attributeName": "vCenter VM","attributeValue": "Tor/Temps/ImageMonoNew","type": "attributes"  },  {"attributeName": "vCenter VM Snapshot","attributeValue": "1","type": "attributes"  },  {"attributeName": "VM Cluster","attributeValue": "","type": "attributes"  },  {"attributeName": "VM Storage","attributeValue": "","type": "attributes"  },  {"attributeName": "VM Resource Pool","attributeValue": "","type": "attributes"  },  {"attributeName": "VM Location","attributeValue": "","type": "attributes"  },  {"attributeName": "Auto Power On","attributeValue": "True","type": "attributes"  },  {"attributeName": "Auto Power Off","attributeValue": "True","type": "attributes"  },  {"attributeName": "Wait for IP","attributeValue": "True","type": "attributes"  }],"type": "deployAppDeploymentInfo"  },  "appResource": {"attributes": [  {"attributeName": "Password","attributeValue": "3M3u7nkDzxWb0aJ/IZYeWw==","type": "attributes"  },  {"attributeName": "Public IP","attributeValue": "","type": "attributes"  },  {"attributeName": "User","attributeValue": "","type": "attributes"  }],"type": "appResourceInfo"  },  "type": "deployAppParams"},"actionId": "7808cf76-b8c5-4392-b571-5da99836b84b","type": "deployApp"  }]  }}'
        req= json.loads(json_req)

        actions_mock = Mock()
        result = None

        parser = DriverRequestParser()
        parser.add_deployment_model(CustomModel)

        actions = parser.convert_driver_request_to_actions(req)


        print json.dumps(actions, default=lambda o: o.__dict__,sort_keys=True, indent=4)

    def test_remove_vlan_action(self):

        # prepare
        json_req = '{  "driverRequest": {"actions": [{"connectionId":"2e85db89-f1c9-4da2-b738-6ed57d7c8ec6","connectionParams":{"vlanId":["2"],"mode":"Access","type":"setVlanParameter"},"connectorAttributes":[{"attributeName":"Interface","attributeValue":"00:50:56:a2:3c:83","type":"connectorAttribute"}],"actionId":"27409903-4d80-4607-8be2-8140285f87e6","actionTarget":{"fullName":"VM Deployment_6693d80d","fullAddress":"N/A","type":"actionTarget"},"customActionAttributes":[{"attributeName":"VM_UUID","attributeValue":"422279ec-e35a-b63f-591a-5e748514056d","type":"customAttribute"}],"type":"removeVlan"}]  }}'
        req= json.loads(json_req)

        parser = DriverRequestParser()

        # act
        action = parser.convert_driver_request_to_actions(req)[0]

        # assert
        self.assertTrue(isinstance(action,RemoveVlan))
        self.assertEqual(action.connectionId,"2e85db89-f1c9-4da2-b738-6ed57d7c8ec6")
        self.assertEqual(action.actionId, "27409903-4d80-4607-8be2-8140285f87e6")

        print json.dumps(action, default=lambda o: o.__dict__,sort_keys=True, indent=4)
