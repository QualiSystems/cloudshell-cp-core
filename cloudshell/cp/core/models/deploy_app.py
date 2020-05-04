import itertools
from dataclasses import dataclass, field

from cloudshell.cp.core.models.base import BaseRequestAction, BaseRequestObject


@dataclass
class AppResourceInfo(BaseRequestObject):
    attributes: dict = field(default_factory=dict)


@dataclass
class DeployAppDeploymentInfo(BaseRequestObject):
    deploymentPath: str = ""
    attributes: dict = field(default_factory=dict)
    customModel: object = None


@dataclass
class DeployAppParams(BaseRequestObject):
    appName: str = ""
    deployment: DeployAppDeploymentInfo = None
    appResource: AppResourceInfo = None


@dataclass
class DeployApp(BaseRequestAction):
    actionParams: DeployAppParams = None
    attributes: dict = field(default_factory=dict)

    def __post_init__(self):
        for attr in itertools.chain(
            *[
                self.actionParams.appResource.attributes,
                self.actionParams.deployment.attributes,
            ]
        ):

            self.attributes[attr.attributeName] = attr.attributeValue

    @property
    def user(self):
        return ""
        # return self.attributes.get("User")

    @property
    def password(self):
        # todo: FiX THIS !!!!!!!! devrypt password by providing CS API here ?????!!!
        return ""
        # return self.attributes.get("Password")

    @property
    def encrypted_password(self):
        return self.attributes.get("Password")

    @property
    def public_ip(self):
        return self.attributes.get("Public IP")


# TODO: request_actions.deploy_app.actionParams.deployment.customModel !!!!!! handle this
#  ! seems that it is case when we have custom deployed app (like we have for the TeraVM and etc)
#  test with both TVM 1st and 2nd gen !!!!
