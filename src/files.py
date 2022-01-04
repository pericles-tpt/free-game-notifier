import yaml

def load_yaml(directory='cfg/creds.yml'):
    ret = {}
    try:
        fp = open(directory, 'r')
        ret = yaml.safe_load(fp)
    except FileNotFoundError:
        fp = open(directory, 'w+')
        fp.close()
    return ret

def retrieve_from_yaml(keys=None, return_list=False):
    yaml_data = load_yaml()

    # Return as dict
    if not return_list:
        ret = {}
        try:    
            for i in keys:
                ret[i] = yaml_data[i]
        except:
            print('Invalid Config Key: One of the supplied keys is NOT a valid config property')
            quit()

    # Return as list
    else:
        ret = []
        try:
            for i in keys:
                ret.append(yaml_data[i])
        except:
            print('Invalid Config Key: One of the supplied keys is NOT a valid config property')
            quit()

    return ret