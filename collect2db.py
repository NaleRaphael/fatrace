from __future__ import absolute_import, print_function, division
import glob
import json
import os
import codecs

from core import Ingredient

def read_config(fpath):
    with open(fpath, 'r') as ifile:
        parsed = json.load(ifile)
        return parsed

def collect_ingr(ingr_dir, ingr_pattern):
    sheets = glob.glob(os.path.join(ingr_dir, ingr_pattern))

    data = {}
    duplicate = []
    for fp in sheets:
        ingr = Ingredient.from_excel(fp)
        for dish in ingr.dishes:
            if dish.name in data:
                duplicate.append(dish)
            else:
                data[dish.name] = dish.ingr

    with codecs.open('db_ingr.json', 'w', encoding='utf-8') as db:
        json.dump(data, db, indent=4, ensure_ascii=False)

    with codecs.open('duplicate_ingr.json', 'w', encoding='utf-8') as dup:
        json.dump(duplicate, dup, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    config_path = r'collect2db_config.json'
    config = read_config(config_path)
    collect_ingr(config['ingr_dir'], config['ingr_pattern'])
