from __future__ import absolute_import, print_function, division

import codecs
import json


class JsonWriter(object):
    @classmethod
    def export(clz, dict_data, fpath, encoding='utf-8', indent=4):
        with codecs.open(fpath, 'w', encoding=encoding) as f:
            json.dump(dict_data, f, indent=indent, ensure_ascii=False)
