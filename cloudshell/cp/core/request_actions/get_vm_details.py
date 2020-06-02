import json
from dataclasses import dataclass, field

from cloudshell.cp.core.requests.actions.deployed_app import DeployedApp


@dataclass
class GetVMDetailsRequestActions:
    deployed_apps: list = field(default_factory=list)

    @classmethod
    def from_request(cls, request):
        data = json.loads(request)
        deployed_apps = []
        for item in data["items"]:
            deployed_app = DeployedApp.from_data(app_request_data=item["appRequestJson"],
                                                 deployed_app_data=item["deployedAppJson"])
            deployed_apps.append(deployed_app)

        return cls(deployed_apps=deployed_apps)
