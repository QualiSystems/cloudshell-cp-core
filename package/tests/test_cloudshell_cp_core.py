from unittest import TestCase

from  cloudshell.cp.core.converters import *
from cloudshell.cp.core.models import *
from cloudshell.cp.core.utils  import *

from mock import Mock, patch


class TestCloudShellCpCore(TestCase):

    def test_cleanup_connectivity(self):
        # prepare
        json_req = '{  "driverRequest": {"actions": [{"connectionId":"2e85db89-f1c9-4da2-b738-6ed57d7c8ec6","connectionParams":{"vlanId":["2"],"mode":"Access","type":"setVlanParameter"},"connectorAttributes":[{"attributeName":"Interface","attributeValue":"00:50:56:a2:3c:83","type":"connectorAttribute"}],"actionId":"27409903-4d80-4607-8be2-8140285f87e6","actionTarget":{"fullName":"VM Deployment_6693d80d","fullAddress":"N/A","type":"actionTarget"},"customActionAttributes":[{"attributeName":"VM_UUID","attributeValue":"422279ec-e35a-b63f-591a-5e748514056d","type":"customAttribute"}],"type":"removeVlan"},{"connectionId":"2e85db89-f1c9-4da2-b738-6ed57d7c8ec6","connectionParams":{"vlanId":["2"],"mode":"Access","type":"setVlanParameter"},"connectorAttributes":[{"attributeName":"Interface","attributeValue":"00:50:56:a2:4f:e2","type":"connectorAttribute"}],"actionId":"20d37283-3f90-4d5b-a949-5851629f20e6","actionTarget":{"fullName":"VM Deployment_44256851","fullAddress":"N/A","type":"actionTarget"},"customActionAttributes":[{"attributeName":"VM_UUID","attributeValue":"422217cb-1de3-1faf-bc42-401e9ecee942","type":"customAttribute"}],"type":"removeVlan"},{"actionId":"vlan1%<=>%resourceA","type":"setVlan","actionTarget":{"fullName":"Chassis1/Blade1/port1","fullAddress":"1/2/3","type":"actionTarget" },"connectionId":"vlan1%<=>%resourceA","connectionParams":{"type":"setVlanParameter","vlanId":["100-200","300"],"mode":"Trunk","vlanServiceAttributes":[{"type":"connectorAttribute","attributeName":"Mode","attributeValue":"Trunk"},{"type":"connectorAttribute","attributeName":"Allocation Ranges","attributeValue":"2-2000"}]},"connectorAttributes":[{"type":"vlanServiceAttribute","attributeName":"QNQ","attributeValue":"Enabled"}]},{"actionId":"4e3931f1-3f52-4505-b39d-0345c9839603","type":"prepareNetwork","connectionParams":{"type":"prepareNetworkParams","cidr":"10.0.5.0/24"},"customActionAttributes":[]},  {"actionParams": {  "appName": "vCenter_CVC_Support",  "deployment": {"deploymentPath": "VCenter Deploy VM From Linked Clone","attributes": [  {"attributeName": "Auto Delete","attributeValue": "True","type": "attributes"  },  {"attributeName": "Autoload","attributeValue": "True","type": "attributes"  },  {"attributeName": "IP Regex","attributeValue": "","type": "attributes"  },  {"attributeName": "Refresh IP Timeout","attributeValue": "600","type": "attributes"  },  {"attributeName": "vCenter VM","attributeValue": "Tor/Temps/ImageMonoNew","type": "attributes"  },  {"attributeName": "vCenter VM Snapshot","attributeValue": "1","type": "attributes"  },  {"attributeName": "VM Cluster","attributeValue": "","type": "attributes"  },  {"attributeName": "VM Storage","attributeValue": "","type": "attributes"  },  {"attributeName": "VM Resource Pool","attributeValue": "","type": "attributes"  },  {"attributeName": "VM Location","attributeValue": "","type": "attributes"  },  {"attributeName": "Auto Power On","attributeValue": "True","type": "attributes"  },  {"attributeName": "Auto Power Off","attributeValue": "True","type": "attributes"  },  {"attributeName": "Wait for IP","attributeValue": "True","type": "attributes"  }],"type": "deployAppDeploymentInfo"  },  "appResource": {"attributes": [  {"attributeName": "Password","attributeValue": "3M3u7nkDzxWb0aJ/IZYeWw==","type": "attributes"  },  {"attributeName": "Public IP","attributeValue": "","type": "attributes"  },  {"attributeName": "User","attributeValue": "","type": "attributes"  }],"type": "appResourceInfo"  },  "type": "deployAppParams"},"actionId": "7808cf76-b8c5-4392-b571-5da99836b84b","type": "deployApp"  }]  }}'
        req= json.loads(json_req)

        actions_mock = Mock()
        result = None

        parser = DriverRequestParser()
        actions = parser.convert_driver_request_to_actions(req)

        for a in actions:
            print json.dumps(a, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)
        # act



        # assert

        # self.assertEquals(result, '{"driverResponse": {"actionResults": [true]}}')

    def test_prepare_connectivity(self):
        # Assert
        cancellation_context = Mock()
        req = '{"driverRequest": {"actions": [{"actionId": "ba7d54a5-79c3-4b55-84c2-d7d9bdc19356","actionTarget": null, "type": "prepareNetwork", "connectionParams": {"type": "prepareNetworkParams", "cidr": "10.0.0.0/24"}}]}}'
        self.aws_shell.prepare_connectivity_operation.prepare_connectivity = Mock(return_value=True)
        res = None
        actions_mock = Mock()
        with patch('cloudshell.cp.aws.aws_shell.AwsShellContext') as shell_context:
            shell_context.return_value = self.mock_context
            with patch('cloudshell.cp.aws.aws_shell.NetworkActionsParser') as net_parser:
                net_parser.parse_network_actions_data = Mock(return_value=actions_mock)

                # Act
                res = self.aws_shell.prepare_connectivity(self.command_context, req, cancellation_context)

            # Assert
            self.aws_shell.prepare_connectivity_operation.prepare_connectivity.assert_called_with(
                    ec2_client=self.expected_shell_context.aws_api.ec2_client,
                    ec2_session=self.expected_shell_context.aws_api.ec2_session,
                    s3_session=self.expected_shell_context.aws_api.s3_session,
                    reservation=self.reservation_model,
                    aws_ec2_datamodel=self.expected_shell_context.aws_ec2_resource_model,
                    actions=actions_mock,
                    cancellation_context=cancellation_context,
                    logger=self.expected_shell_context.logger)
            self.assertEqual(res, '{"driverResponse": {"actionResults": true}}')

    def test_prepare_connectivity_invalid_req(self):
        with patch('cloudshell.cp.aws.aws_shell.AwsShellContext'):
            req = '{"aa": {"actions": [{"actionId": "ba7d54a5-79c3-4b55-84c2-d7d9bdc19356","actionTarget": null,"customActionAttributes": [{"attributeName": "Network","attributeValue": "10.0.0.0/24","type": "customAttribute"}],"type": "prepareNetwork"}]}}'
            self.aws_shell.prepare_connectivity_operation.prepare_connectivity = Mock(return_value=True)

            self.assertRaises(ValueError, self.aws_shell.prepare_connectivity, self.command_context, req, Mock())

    def test_delete_instance(self):
        deployed_model = DeployDataHolder({'vmdetails': {'uid': 'id'}})
        remote_resource = Mock()
        remote_resource.fullname = 'my ami name'
        self.command_context.remote_endpoints = [remote_resource]
        self.aws_shell.model_parser.convert_app_resource_to_deployed_app = Mock(return_value=deployed_model)
        self.aws_shell.delete_ami_operation.delete_instance = Mock(return_value=True)

        with patch('cloudshell.cp.aws.aws_shell.AwsShellContext') as shell_context:
            shell_context.return_value = self.mock_context

            # act
            self.aws_shell.delete_instance(self.command_context)

        self.aws_shell.delete_ami_operation.delete_instance.assert_called_with(
                logger=self.expected_shell_context.logger,
                ec2_session=self.expected_shell_context.aws_api.ec2_session,
                instance_id=deployed_model.vmdetails.uid)

    def test_power_on(self):
        deployed_model = DeployDataHolder({'vmdetails': {'uid': 'id'}})
        remote_resource = Mock()
        remote_resource.fullname = 'my ami name'
        self.command_context.remote_endpoints = [remote_resource]
        self.aws_shell.model_parser.convert_app_resource_to_deployed_app = Mock(return_value=deployed_model)
        self.aws_shell.power_management_operation.power_on = Mock(return_value=True)

        with patch('cloudshell.cp.aws.aws_shell.AwsShellContext') as shell_context:
            shell_context.return_value = self.mock_context

            # act
            self.aws_shell.power_on_ami(self.command_context)

        self.aws_shell.power_management_operation.power_on.assert_called_with(
                ec2_session=self.expected_shell_context.aws_api.ec2_session,
                ami_id=deployed_model.vmdetails.uid)

    def test_power_off(self):
        deployed_model = DeployDataHolder({'vmdetails': {'uid': 'id'}})
        remote_resource = Mock()
        remote_resource.fullname = 'my ami name'
        self.command_context.remote_endpoints = [remote_resource]
        self.aws_shell.model_parser.convert_app_resource_to_deployed_app = Mock(return_value=deployed_model)
        self.aws_shell.power_management_operation.power_off = Mock(return_value=True)

        with patch('cloudshell.cp.aws.aws_shell.AwsShellContext') as shell_context:
            shell_context.return_value = self.mock_context

            # act
            self.aws_shell.power_off_ami(self.command_context)

        self.aws_shell.power_management_operation.power_off.assert_called_with(
                ec2_session=self.expected_shell_context.aws_api.ec2_session,
                ami_id=deployed_model.vmdetails.uid)

    def test_get_application_ports(self):
        remote_resource = Mock()
        remote_resource.fullname = 'my ami name'
        self.command_context.remote_endpoints = [remote_resource]

        deployed_model = Mock()
        deployed_model.vmdetails = Mock()
        deployed_model.vmdetails.vmCustomParams = Mock()
        self.aws_shell.model_parser.convert_app_resource_to_deployed_app = Mock(return_value=deployed_model)

        self.aws_shell.model_parser.try_get_deployed_connected_resource_instance_id = Mock(return_value='instance_id')
        self.aws_shell.deployed_app_ports_operation.get_app_ports_from_cloud_provider = Mock(return_value='bla')

        self.aws_shell.model_parser.get_allow_all_storage_traffic_from_connected_resource_details = Mock(return_value='True')

        with patch('cloudshell.cp.aws.aws_shell.AwsShellContext') as shell_context:
            shell_context.return_value = self.mock_context

            # act
            res = self.aws_shell.get_application_ports(self.command_context)

        assert res == 'bla'
        self.aws_shell.deployed_app_ports_operation.get_app_ports_from_cloud_provider.assert_called_with(
            ec2_session=self.expected_shell_context.aws_api.ec2_session,
            instance_id='instance_id',
            resource=remote_resource,
            allow_all_storage_traffic='True'
        )

    def test_get_access_key(self):
        self.command_context.remote_reservation = Mock()
        self.command_context.remote_reservation.reservation_id = 'reservation_id'
        self.aws_shell.access_key_operation.get_access_key = Mock(return_value='access_key')

        with patch('cloudshell.cp.aws.aws_shell.AwsShellContext') as shell_context:
            shell_context.return_value = self.mock_context

            # act
            res = self.aws_shell.get_access_key(self.command_context)

        assert res == 'access_key'
        self.aws_shell.access_key_operation.get_access_key(
                s3_session=self.expected_shell_context.aws_api.ec2_session,
                aws_ec2_resource_model=self.expected_shell_context.aws_ec2_resource_model,
                reservation_id=self.command_context.remote_reservation.reservation_id)

    def test_refresh_ip(self):
        self.aws_shell.model_parser.get_private_ip_from_connected_resource_details = Mock(return_value='private_ip')
        self.aws_shell.model_parser.get_public_ip_from_connected_resource_details = Mock(return_value='public_ip')
        self.aws_shell.model_parser.try_get_deployed_connected_resource_instance_id = Mock(return_value='instance_id')
        self.aws_shell.model_parser.get_connectd_resource_fullname = Mock(return_value='resource_name')
        self.aws_shell.refresh_ip_operation.refresh_ip = Mock()

        with patch('cloudshell.cp.aws.aws_shell.AwsShellContext') as shell_context:
            shell_context.return_value = self.mock_context

            # act
            self.aws_shell.refresh_ip(self.command_context)

        self.aws_shell.refresh_ip_operation.refresh_ip(
            cloudshell_session=self.expected_shell_context.cloudshell_session,
            ec2_session=self.expected_shell_context.aws_api.ec2_session,
            deployed_instance_id='instance_id',
            private_ip_on_resource='private_ip',
            public_ip_on_resource='public_ip',
            resource_fullname='resource_name')
