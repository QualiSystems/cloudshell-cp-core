import json


# todo: refactor this !!!!
class DriverResponseRoot(object):
    def __init__(self, driverResponse=None):
        """
        :param driverResponse:  DriverResponse
        """
        self.driverResponse = driverResponse

    def _default_json_dump(self, obj):
        if isinstance(obj, bytes):
            return str(obj)

        return obj.__dict__

    def to_json(self):
        return json.dumps(self, default=self._default_json_dump)


class DriverResponse(object):
    def __init__(self,actionResults = None):
        """
        :param actionResults: [ActionResultBase]
        """
        self.actionResults = actionResults if actionResults else [] # type: [ActionResultBase]

    def to_driver_response_json(self):
        """
        Wrap this object with DriverResponseRoot and converts it to json.
        :return:
        """
        return DriverResponseRoot(driverResponse=self).to_json()
