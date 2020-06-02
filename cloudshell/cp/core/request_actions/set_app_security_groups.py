import json
from dataclasses import dataclass

from cloudshell.cp.core.requests.actions.base import BaseRequestActions


@dataclass
class SetAppSecurityGroupsRequestActions(BaseRequestActions):
    @classmethod
    def from_request(cls, request, cs_api=None):
        actions = cls._parse_request_actions(request=request, cs_api=cs_api)
        obj = cls()
        cls.actions = actions
        #
        # for action in actions:
        #     if isinstance(action, models.CleanupNetwork):
        #         obj.cleanup_network = action

        return obj
        #
        # security_group_models = []
        #
        # security_groups = AzureModelsParser.get_app_security_groups_from_request(request)
        #
        # for security_group in security_groups:
        #     security_group_model = AppSecurityGroupModel()
        #     security_group_model.deployed_app = DeployedApp()
        #     security_group_model.deployed_app.name = security_group.deployedApp.name
        #     security_group_model.deployed_app.vm_details = VmDetails()
        #     security_group_model.deployed_app.vm_details.uid = security_group.deployedApp.vmdetails.uid
        #     security_group_model.security_group_configurations = SecurityGroupParser.parse_security_group_configurations(
        #         security_group.securityGroupsConfigurations)
        #
        #     security_group_models.append(security_group_model)
        #
        # return security_group_models