from cloudshell.cp.core.utils import  *
from cloudshell.cp.core.models import *

class LinkedCloneModel(object):

    __deploymentModel__ = "linkedClone"

    def __init__(self, attributes):
        """
        :param dict attributes:
        """
        self.a = dict['a']  # type: str
        self.b = (dict['b'])  # type: bool

class DriverRequestParser:

    def __init__(self):
        self.models_classes = {}

    def add_deployment_model(self, deployment_model_cls):
        self.models_classes[deployment_model_cls.__deploymentModel__] = deployment_model_cls

    def convert_driver_request_to_actions(self, driver_request):

        actions = driver_request['driverRequest'].get('actions')

        if (actions == None):
            print 'error'
            return None

        result = []

        for a in actions:
            class_name = first_letter_to_upper(a.get('type'))
            try:
                created_action = getattr(sys.modules[__name__], class_name)()
                self._convert_action(a, created_action)
                result.append(created_action)

            except Exception as e:
                print e.message
                print 'no class named ' + class_name
                pass

        return  result

    def _create_by_type(self,source):
        t = source.get('type')

        if (t == None):
            raise ValueError('source has no "type" property')

        t = first_letter_to_upper(t)
        created = getattr(sys.modules[__name__], t)()

        return created

    def _convert_action(self, source, result):

        for key, value in source.items():
            if (isinstance(value, dict)):
                created = self._create_by_type(value)
                self._set_value(result, key, created)
                self._convert_action(value, getattr(result, key))
            elif isinstance(value, (list)):
                    created_arr = []
                    self._set_value(result, key, created_arr)

                    for item in value:
                        if isinstance(item, (dict)):
                            created_item = self._create_by_type(item)
                            created_arr.append(created_item)
                            self._convert_action(item, created_item)
                        else:
                            created_arr.append(item)

            else:
                self._set_value(result, key, value)


    def _set_value(self, target, name, value):

        if isinstance(target, (list)):
            target.append(value)
        elif(name != 'type' and not try_set_attr(target, name, value)):
            raise ValueError(target.__class__.__name__ +  ' has no property named ' + name)

    def _try_set_attr(self, target, name, value):

        try:
            if (hasattr(target, name)):
                setattr(target, name, value)
                return True
        except Exception as e:
            pass

        return False



