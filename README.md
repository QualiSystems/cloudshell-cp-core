# cloudshell-cp-core


A repository for projects providing out of the box capabilities within CloudShell to parse and convert cloushell driver request to well defined python objects.
One cloudshell-cp-core For All cloudshell cloud provider shells.

### Installing

$ python -m pip install cloudshell-cp-core

### Example

Parsing a driver request

```
    def test_deploy_app_action(self):
        # prepare
        json_req = '{"driverRequest":{"actions":[{"actionParams":{"appName":"vCenter_CVC_Support","deployment":{"deploymentPath":"VCenter Deploy VM From Linked Clone","attributes":[{"attributeName":"vCenter VM","attributeValue":"Tor/Temps/ImageMonoNew","type":"attribute"},{"attributeName":"vCenter VM Snapshot","attributeValue":"1","type":"attribute"},{"attributeName":"VM Cluster","attributeValue":"","type":"attribute"},{"attributeName":"VM Storage","attributeValue":"","type":"attribute"},{"attributeName":"VM Resource Pool","attributeValue":"","type":"attribute"},{"attributeName":"VM Location","attributeValue":"","type":"attribute"},{"attributeName":"Auto Power On","attributeValue":"True","type":"attribute"},{"attributeName":"Auto Power Off","attributeValue":"True","type":"attribute"},{"attributeName":"Wait for IP","attributeValue":"True","type":"attribute"},{"attributeName":"Auto Delete","attributeValue":"True","type":"attribute"},{"attributeName":"Autoload","attributeValue":"True","type":"attribute"},{"attributeName":"IP Regex","attributeValue":"","type":"attribute"},{"attributeName":"Refresh IP Timeout","attributeValue":"600","type":"attribute"}],"type":"deployAppDeploymentInfo"},"appResource":{"attributes":[{"attributeName":"Password","attributeValue":"3M3u7nkDzxWb0aJ/IZYeWw==","type":"attribute"},{"attributeName":"Public IP","attributeValue":"","type":"attribute"},{"attributeName":"User","attributeValue":"","type":"attribute"}],"type":"appResourceInfo"},"type":"deployAppParams"},"actionId":"ad3561c1-45a5-445a-9b5f-4021879a0b0c","type":"deployApp"}]}}'

        # act
        parser = DriverRequestParser()
        deploy_action = parser.convert_driver_request_to_actions(json_req)[0]

        # assert
        self.assertIsInstance(deploy_action, DeployApp)
        self.assertEqual(deploy_action.actionParams.appName, 'vCenter_CVC_Support')
        self.assertEqual(deploy_action.actionParams.deployment.deploymentPath, "VCenter Deploy VM From Linked Clone")
        self.assertEqual(deploy_action.actionParams.deployment.attributes["vCenter VM Snapshot"], "1")
```

Parsing a driver request with custom deployment model

```
    def test_custom_deployment_model(self):
        class CustomModel(object):
            __deploymentModel__ = "VCenter Deploy VM From Linked Clone"

            def __init__(self, attributes):
                self.auto_power_off = attributes['Auto Power Off']
                self.autoload = attributes['Autoload']

        atts_json = '[{"attributeName":"Auto Delete","attributeValue":"True","type":"attributes"},{"attributeName":"Autoload","attributeValue":"True","type":"attributes"},{"attributeName":"IP Regex","attributeValue":"","type":"attributes"},{"attributeName":"Refresh IP Timeout","attributeValue":"600","type":"attributes"},{"attributeName":"vCenter VM","attributeValue":"Tor/Temps/ImageMonoNew","type":"attributes"},{"attributeName":"vCenter VM Snapshot","attributeValue":"1","type":"attributes"},{"attributeName":"VM Cluster","attributeValue":"","type":"attributes"},{"attributeName":"VM Storage","attributeValue":"","type":"attributes"},{"attributeName":"VM Resource Pool","attributeValue":"","type":"attributes"},{"attributeName":"VM Location","attributeValue":"","type":"attributes"},{"attributeName":"Auto Power On","attributeValue":"True","type":"attributes"},{"attributeName":"Auto Power Off","attributeValue":"True","type":"attributes"},{"attributeName":"Wait for IP","attributeValue":"True","type":"attributes"}]'
        deploy_req_json = '{"driverRequest":{"actions":[{"actionParams":{"appName":"vCenter_CVC_Support","deployment":{"deploymentPath":"VCenter Deploy VM From Linked Clone","attributes": ' + atts_json + ' ,"type":"deployAppDeploymentInfo"},"appResource":{"attributes":[{"attributeName":"Password","attributeValue":"3M3u7nkDzxWb0aJ/IZYeWw==","type":"attributes"},{"attributeName":"Public IP","attributeValue":"","type":"attributes"},{"attributeName":"User","attributeValue":"","type":"attributes"}],"type":"appResourceInfo"},"type":"deployAppParams"},"actionId":"7808cf76-b8c5-4392-b571-5da99836b84b","type":"deployApp"}]}}'

        parser = DriverRequestParser()
        parser.add_deployment_model(CustomModel)

        action = parser.convert_driver_request_to_actions(deploy_req_json)[0]

        self.assertTrue(action.actionParams.deployment.customModel.autoload, 'True')
        self.assertTrue(action.actionParams.deployment.customModel.auto_power_off, 'True')
```
Same but slicker

```
    def test_custom_deployment_model_slicker(self):
        class CustomModel(object):
            __deploymentModel__ = "VCenter Deploy VM From Linked Clone"

            def __init__(self, attributes):
                self.auto_power_off = ''
                self.autoload = ''

                # slicker since we are using utils.py functions: try_set_attr, to_snake_case.
                # this way we scan all deployment attributes and if there is a corresponding named member in
                # custom model e.g: auto_power_off corresponds 'Auto Power Off'
                # that attribute value will be assigned to the corresponding member
                for k, v in attributes.iteritems():
                    try_set_attr(self, to_snake_case(k), v)

        atts_json = '[{"attributeName":"Auto Delete","attributeValue":"True","type":"attributes"},{"attributeName":"Autoload","attributeValue":"True","type":"attributes"},{"attributeName":"IP Regex","attributeValue":"","type":"attributes"},{"attributeName":"Refresh IP Timeout","attributeValue":"600","type":"attributes"},{"attributeName":"vCenter VM","attributeValue":"Tor/Temps/ImageMonoNew","type":"attributes"},{"attributeName":"vCenter VM Snapshot","attributeValue":"1","type":"attributes"},{"attributeName":"VM Cluster","attributeValue":"","type":"attributes"},{"attributeName":"VM Storage","attributeValue":"","type":"attributes"},{"attributeName":"VM Resource Pool","attributeValue":"","type":"attributes"},{"attributeName":"VM Location","attributeValue":"","type":"attributes"},{"attributeName":"Auto Power On","attributeValue":"True","type":"attributes"},{"attributeName":"Auto Power Off","attributeValue":"True","type":"attributes"},{"attributeName":"Wait for IP","attributeValue":"True","type":"attributes"}]'
        deploy_req_json = '{"driverRequest":{"actions":[{"actionParams":{"appName":"vCenter_CVC_Support","deployment":{"deploymentPath":"VCenter Deploy VM From Linked Clone","attributes": ' + atts_json + ' ,"type":"deployAppDeploymentInfo"},"appResource":{"attributes":[{"attributeName":"Password","attributeValue":"3M3u7nkDzxWb0aJ/IZYeWw==","type":"attributes"},{"attributeName":"Public IP","attributeValue":"","type":"attributes"},{"attributeName":"User","attributeValue":"","type":"attributes"}],"type":"appResourceInfo"},"type":"deployAppParams"},"actionId":"7808cf76-b8c5-4392-b571-5da99836b84b","type":"deployApp"}]}}'

        parser = DriverRequestParser()
        parser.add_deployment_model(CustomModel)

        action = parser.convert_driver_request_to_actions(deploy_req_json)[0]

        self.assertTrue(action.actionParams.deployment.customModel.autoload, 'True')
        self.assertTrue(action.actionParams.deployment.customModel.auto_power_off, 'True')

