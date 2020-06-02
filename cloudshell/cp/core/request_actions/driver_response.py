import json


# todo: refactor this !!!!
class DriverResponseRoot:
    def __init__(self, driver_response=None):
        """

        :param driver_response:
        """
        self.driverResponse = driver_response

    def _default_json_dump(self, obj):
        if isinstance(obj, bytes):
            return str(obj)

        return obj.__dict__

    def to_json(self):
        return json.dumps(self, default=self._default_json_dump)


class DriverResponse:
    def __init__(self, action_results=None):
        """

        :param action_results:
        """
        self.action_results = action_results or []

    def to_driver_response_json(self):
        """
        Wrap this object with DriverResponseRoot and converts it to json.
        :return:
        """
        return DriverResponseRoot(driver_response=self).to_json()
