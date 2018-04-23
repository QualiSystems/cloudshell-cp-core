
def set_value(target, name, value, raise_exeception = False):

    if isinstance(target, (list)):
        target.append(value)
    elif(not try_set_attr(target, name, value) and raise_exeception):
        raise ValueError(target.__class__.__name__ +  ' has no property named ' + name)

def try_set_attr(target, name, value):

    try:
        if (hasattr(target, name)):
            setattr(target, name, value)
            return True
    except Exception as e:
        pass

    return False

def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m

def first_letter_to_upper(str):
    return str[:1].upper() + str[1:]

def to_snake_case(str):
    return  str.lower().replace(' ','_' )

def convert_attributes_list_to_map(attributes):

    attributes_map = {}

    # so we shall convert it to attributes map{key : attribute name,value : attribute value }
    for item in attributes:
        attributes_map[item.get('attributeName')] = item.get('attributeValue')

    return attributes_map