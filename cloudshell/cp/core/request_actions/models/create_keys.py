from dataclasses import dataclass

from cloudshell.cp.core.requests.models import BaseRequestAction


@dataclass
class CreateKeys(BaseRequestAction):
    pass
