import itertools
from dataclasses import dataclass, field

from .base import BaseRequestAction, BaseRequestObject


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
            self.actionParams.appResource.attributes,
            self.actionParams.deployment.attributes,
        ):
            self.attributes[attr.attributeName] = attr.attributeValue

        self._cs_api = None
        self._password = None

    def set_cloudshell_api(self, api):
        """Set CloudShell API

        :param cloudshell.api.cloudshell_api.CloudShellAPISession api:
        :return:
        """
        self._cs_api = api

    def _decrypt_password(self, password):
        """Decrypt CloudShell password

        :param  password:
        :return:
        """
        if self._cs_api is None:
            raise Exception("Cannot decrypt password, CloudShell API is not defined")

        return self._cs_api.DecryptPassword(password).Value

    @property
    def user(self):
        return self.attributes.get("User")

    @property
    def password(self):
        if self._password is None:
            self._password = self._decrypt_password(
                password=self.attributes.get("Password")
            )

        return self._password

    @property
    def public_ip(self):
        return self.attributes.get("Public IP")


# TODO: request_actions.deploy_app.actionParams.deployment.customModel !!!!!! handle this
#  ! seems that it is case when we have custom deployed app (like we have for the TeraVM and etc)
#  test with both TVM 1st and 2nd gen !!!!
