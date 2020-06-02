from dataclasses import dataclass

from cloudshell.cp.core.request_actions.base import BaseRequestActions


@dataclass
class SetAppSecurityGroupsRequestActions(BaseRequestActions):
    @classmethod
    def from_request(cls, request, cs_api=None):
        """Create SetAppSecurityGroupsRequestActions object from the string request.

        :param str request:
        :param cloudshell.api.cloudshell_api.CloudShellAPISession cs_api:
        :rtype: SetAppSecurityGroupsRequestActions
        """
        actions = cls._parse_request_actions(request=request, cs_api=cs_api)
        obj = cls()
        cls.actions = actions

        return obj
