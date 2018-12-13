# -*- coding: utf-8 -*-
"""Description :
"""
# talen@uestc 2018/12/13
from __future__ import print_function, division, absolute_import, unicode_literals
import json
import os

# bookmark_name = os.path.join(os.path.expanduser("~"), 'AppData//Local//Google//Chrome//User Data//Profile 1',
#                              'Bookmarks')


def get_chrome_list(path):
    lis = []
    # title url time '' four items
    with open(path, encoding='UTF-8') as json_file:
        data = json.load(json_file)

        child_items = data['roots']['bookmark_bar']['children']
        make_list(lis, child_items)
    return lis


def make_list(lis, child_items):
    for item in child_items:
        if 'children' in item.keys():
            # print(item['name']) # 类别标签
            # print(type(item['children']))
            make_list(lis, item['children'])
        else:
            mItem = [item['name'], item['url'], item['date_added'], '']
            lis.append(mItem)
            # print(item['name'],item['url'])


# def store( data, store_name='data.json'):
#     with open(store_name, 'w') as json_file:
#         json_file.write(json.dumps(data))

if __name__ == '__main__':
    # in windows
    bookmark_name = os.path.join(os.path.expanduser("~"), 'AppData//Local//Google//Chrome//User Data//Profile 1',
                                 'Bookmarks')

    # in mac
    # bookmark_name = os.path.join(os.path.expanduser("~"), 'Library/Application Support/Google/Chrome/Default',
    #                     'Bookmarks')

    lis = get_chrome_list(bookmark_name)
    print(lis)
