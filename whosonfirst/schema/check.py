# -*-python-*-

import json
import os.path
from collections import OrderedDict

class PropertiesChecker(object):
    PROPERTIES_DIR = 'properties'
    JSON_SUFFIX = '.json'


    def __init__(self, **kwargs):
        self.data_types = ['dictionary', 'float', 'integer', 'list', 'string']

    def check_properties(self, path, options):
        if not os.path.isdir(path):
            return False

        path = os.path.join(path, self.PROPERTIES_DIR)
        if not os.path.isdir(path):
            return False

        types = { 'missing': 0, 'unknown': 0 }
        for type in self.data_types:
            types[type] = 0

        for dir_name, sub_dirs, file_list in os.walk(path):
            for file_name in file_list:
                if file_name.lower().endswith(self.JSON_SUFFIX):
                    fh = open(os.path.join(dir_name, file_name), 'r')
                    doc = json.load(fh, object_pairs_hook=OrderedDict)
                    fh.close()

                    if not doc['type']:
                        if options.datatype:
                            doc['type'] = options.datatype
                            types[doc['type']] += 1
                            fh = open(os.path.join(dir_name, file_name), 'w')
                            json.dump(doc, fh, indent=2)
                            fh.close()
                            print('{} added default data type {}'.format(os.path.join(dir_name, file_name), options.datatype))

                        else:
                            types['missing'] += 1
                            if options.verbose:
                                print('{} missing or empty type'.format(os.path.join(dir_name, file_name)))

                    elif not doc['type'] in self.data_types:
                        print('{} unknown type {}'.format(os.path.join(dir_name, file_name), doc['type']))

                    else:
                        types[doc['type']] += 1

        return types
