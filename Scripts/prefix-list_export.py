#! /usr/bin/env python3

from restapicalls import RestApiCalls
import json
import os
import sys


def prefix_payload_gen(file):
    pl_line = []
    dict_items_list = []
    i = 0
    k = 0

    with open(file, 'r') as f:
        data = f.read()

    for line in data.splitlines():
        if line.startswith('ip prefix-list'):
            pl_line.append(line)
            line_items = line.split(' ')
            name = line_items[line_items.index('prefix-list') + 1]
            dict_items = ({'name': name, 'entries': []})
            if dict_items not in dict_items_list:
                dict_items_list.append(dict_items)

    if not pl_line:
        print('No prefix-lists were found in the "{}" config-file'.format(file))
    else:
        for line in pl_line:
            line_items = line.split(' ')
            name = line_items[line_items.index('prefix-list') + 1]
            ipprefix = line_items[line_items.index('seq') + 3]

            if name != dict_items_list[i]['name']:
                i += 1
                k = 0

            dict_items_list[i]['entries'].insert(k, {'ipPrefix': ipprefix})
            if 'ge' in line_items:
                dict_items_list[i]['entries'][k].update({'ge': line_items[line_items.index('ge') + 1]})
            if 'le' in line_items:
                dict_items_list[i]['entries'][k].update({'le': line_items[line_items.index('le') + 1]})
            k += 1

    with open('api_call_data', 'w') as f:
        f.write(json.dumps(dict_items_list, indent=4))

    return dict_items_list


def _main():
    sdwan = RestApiCalls('10.177.28.62', 'admin', 'admin')
    for pl in prefix_payload_gen(sys.argv[1]):
        sdwan.post_request('template/policy/list/prefix', pl)
        print('Prefix-list {} parsed and exported to SD-WAN Controller'.format(pl['name']))


if __name__ == "__main__":
    _main()
