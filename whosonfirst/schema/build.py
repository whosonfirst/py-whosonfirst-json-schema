# -*-python-*-

import os.path
import sys
import json
from collections import OrderedDict
import re

class PropertiesBuilder(object):
    PROPERTIES_DIR = 'properties'
    WOF_PREFIX = 'wof'
    JSON_SUFFIX = '.json'

    def __init__(self, **kwargs):
        self.wof_properties = OrderedDict()
        self.properties = OrderedDict()
        self.wildcard_name = re.compile('\{(.*)\}(.*)')
        self.types = {
            'integer': 'integer',
            'float': 'number',
            'string': 'string',
            'dictionary': 'object',
            'list': 'array',
            'null': 'null'
        }
        self.template = OrderedDict()
        self.template['$schema']  = 'http://json-schema.org/draft-06/schema#'
        self.template['$id'] = 'properties.json'
        self.template['definitions'] = OrderedDict()
        self.template['definitions']['properties'] = OrderedDict()
        self.template['definitions']['properties']['description'] = 'The properties that can exist in a WOF document'
        self.template['definitions']['properties']['type'] = 'object'
        self.template['definitions']['properties']['properties'] = OrderedDict()
        self.template['definitions']['properties']['patternProperties'] = OrderedDict()

    def encode_properties(self, path, fh=sys.stdout):
        if not os.path.isdir(path):
            return False

        path = os.path.join(path, self.PROPERTIES_DIR)
        if not os.path.isdir(path):
            return False

        self._gather_properties(path, fh)

    def _gather_properties(self, path, outh):
        wof_props = {}
        other_props = {}
        pattern_props = {}

        for dir_name, sub_dirs, file_list in os.walk(path):
            for file_name in file_list:
                if file_name.lower().endswith(self.JSON_SUFFIX):
                    fh = open(os.path.join(dir_name, file_name), 'r')
                    doc = json.load(fh)

                    prefix = doc['prefix']

                    if not doc['type']:
                        doc['type'] = 'string'

                    if isinstance(doc['type'], list):
                        types = []
                        for t in doc['type']:
                            types.append(self.types[t])

                        doc['type'] = types

                    else:
                        doc['type'] = self.types[doc['type']]

                    key = '{}:{}'.format(prefix, doc['name'])
                    prop_def = OrderedDict()
                    prop_def['type'] = doc['type']

                    if doc['type'] == 'array' and 'items' in doc:
                        prop_def['items'] = doc['items']
                        if 'type' in prop_def['items']:
                            prop_def['items']['type'] = self.types[prop_def['items']['type']]
                            if 'patterns' in doc and 'value' in doc['patterns']:
                                prop_def['items']['pattern'] = doc['patterns']['value']

                    if doc['type'] == 'object':
                        if 'additionalProperties' in doc:
                            prop_def['additionalProperties'] = doc['additionalProperties']

                        if 'properties' in doc:
                            prop_def['properties'] = doc['properties']

                    if 'patterns' in doc and 'value' in doc['patterns'] and doc['type'] != 'array':
                        prop_def['pattern'] = doc['patterns']['value']


                    if 'patterns' in doc and 'name' in doc['patterns']:
                        key = '^{}:{}$'.format(prefix, doc['patterns']['name'])
                        pattern_props[key] = prop_def

                    else:
                        if prefix == self.WOF_PREFIX:
                            wof_props[key] = prop_def

                        else:
                            other_props[key] = prop_def

        properties = OrderedDict()
        properties.update(self.template)

        if wof_props:
            wofs = OrderedDict(sorted(wof_props.items(), key=lambda t: t[0]))
            properties['definitions']['properties']['properties'].update(wofs)

        if other_props:
            props = OrderedDict(sorted(other_props.items(), key=lambda t: t[0].lower()))
            properties['definitions']['properties']['properties'].update(props)

        if pattern_props:
            patterns = OrderedDict(sorted(pattern_props.items(), key=lambda t: t[0].lower()))
            properties['definitions']['properties']['patternProperties'].update(patterns)

        else:
            del properties['definitions']['properties']['patternProperties']

        json.dump(properties, outh, indent=2)
