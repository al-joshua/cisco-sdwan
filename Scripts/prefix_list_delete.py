#! /usr/bin/env python3

from restapicalls import RestApiCalls
import json
import os


def free_prefix_delete(sdwan_obj):
    unused_pl = []
    configured_pl = json.loads(sdwan_obj.get_request('template/policy/list/prefix'))['data']
    for pl in configured_pl:
        if pl['referenceCount'] == 0:
            unused_pl.append(pl['listId'])

    if not unused_pl:
        print('No unused prefix-lists')

    for _ in unused_pl:
        sdwan_obj.delete_request('template/policy/list/prefix/', _)

    return unused_pl


def _main():
    sdwan = RestApiCalls('10.177.28.62', 'admin', 'admin')
    for pl in free_prefix_delete(sdwan):
        sdwan.delete_request('template/policy/list/prefix/', pl)
        print('Unused prefix-list {} was removed from SD-WAN Controller'.format(pl))


if __name__ == "__main__":
    _main()
