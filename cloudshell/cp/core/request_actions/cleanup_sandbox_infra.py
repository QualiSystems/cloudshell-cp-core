from dataclasses import dataclass

from cloudshell.cp.core.request_actions import models
from cloudshell.cp.core.request_actions.base import BaseRequestActions


@dataclass
class CleanupSandboxInfraRequestActions(BaseRequestActions):
    cleanup_network: models.CleanupNetwork = None

    @classmethod
    def from_request(cls, request, cs_api=None):
        """

        :param request:
        :param cs_api:
        :return:
        """
        actions = cls._parse_request_actions(request=request, cs_api=cs_api)
        obj = cls()

        for action in actions:
            if isinstance(action, models.CleanupNetwork):
                obj.cleanup_network = action

        return obj
