# Copyright (c) 2022 Pericles Telemachou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import yaml, os

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

def append_to_file(msg, pth='./dat/found'):
    with open(pth, 'a+') as out:
        out.write(msg)

def read_lines_to_list(pth='./dat/found'):
    ret = []
    if (os.path.isfile(pth)):
        with open(pth, 'r') as inp:
            ret = inp.readlines()
    return ret