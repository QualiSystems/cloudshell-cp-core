import itertools
import json
from dataclasses import dataclass

from cloudshell.cp.core.request_actions import models


@dataclass
class DeployedVMActions:
    REGISTERED_DEPLOYMENT_PATH_MODELS = {}
    deployed_app: models.DeployedApp = None

    @classmethod
    def register_deployment_path(cls, deployment_path_cls):
        """Register deployment path class.

        :param cloudshell.cp.core.models.DeployedApp deployment_path_cls:
        :return:
        """
        cls.REGISTERED_DEPLOYMENT_PATH_MODELS[
            deployment_path_cls.DEPLOYMENT_PATH
        ] = deployment_path_cls

    @classmethod
    def from_data(cls, app_request_data, deployed_app_data):
        """Create DeployedApp from the dictionaries.

        :param dict app_request_data:
        :param dict deployed_app_data:
        :rtype: models.DeployedApp
        """
        attributes = {
            attr["name"]: attr["value"]
            for attr in itertools.chain(
                deployed_app_data["attributes"],
                app_request_data["deploymentService"]["attributes"],
            )
        }

        deployed_app_cls = cls.REGISTERED_DEPLOYMENT_PATH_MODELS.get(
            app_request_data["deploymentService"]["model"], models.DeployedApp
        )

        deployed_app = deployed_app_cls(
            name=deployed_app_data["name"],
            deployment_service_model=app_request_data["deploymentService"]["model"],
            private_ip=deployed_app_data["address"],
            attributes=attributes,
            vmdetails=models.VMDetails.from_dict(deployed_app_data["vmdetails"]),
        )

        return cls(deployed_app=deployed_app)

    @classmethod
    def from_remote_resource(cls, resource):
        """Create DeployedApp from the resource.

        :param cloudshell.shell.core.driver_context.ResourceContextDetails resource:
        :rtype: models.DeployedApp
        """
        return cls.from_data(
            app_request_data=json.loads(resource.app_context.app_request_json),
            deployed_app_data=json.loads(resource.app_context.deployed_app_json),
        )
