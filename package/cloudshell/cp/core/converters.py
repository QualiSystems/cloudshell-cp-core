from cloudshell.cp.core.utils import  *
from cloudshell.cp.core.models import *

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
                self.handle_deployemnt_custom_model(created, value)
                self._set_value(result, key, created)
                self._convert_action(value, getattr(result, key))
            elif (isinstance(value, (list))):

                    if(self.try_convert_to_attributes_map(value, result, key)):
                        continue

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



    def handle_deployemnt_custom_model(self, result, item):

        if item.get('type') != 'deployAppDeploymentInfo':
            return

        atts = item.get('attributes')

        if not atts:
            return

        deployment_model_name = item.get('deploymentPath')

        model_class = self.models_classes.get(deployment_model_name)

        if not model_class:
            return

        result.customModel = model_class(convert_attributes_list_to_map(atts))

    def is_attribute(self, item):
        return  set(('attributeName','attributeValue')).issubset(item)

    def try_convert_to_attributes_map(self, arr, result, key):

        # if not All objects looks like attribute
        if not all(self.is_attribute(item) for item in arr):
            return False

        self._set_value(result, key, convert_attributes_list_to_map(arr))

        return True

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



