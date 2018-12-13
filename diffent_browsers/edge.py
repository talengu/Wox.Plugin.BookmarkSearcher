# -*- coding: utf-8 -*-
"""Description :
"""
# talen@uestc 
# 2018/12/13 
from __future__ import print_function, division, absolute_import, unicode_literals
import pyesedb
# https://github.com/libyal/libesedb
# from pyesedb import column_types as DBTYPES
import struct
import datetime


def get_microsecs(raw_timestamp):
    timestamp = struct.unpack("Q", raw_timestamp)[0]
    # 131735925139860189
    # 13189095048684753
    # 谷歌的 bookmark 要放在一起排序  time*10 (国际标准时间)
    # print(ddGetWinTimeStamp(13189168479832162*10))
    microsecs, _ = divmod(timestamp, 10)
    return microsecs


def get_edge_list(edb_path="..\\demo_datas\\DBStore\\spartan.edb"):
    lis = []
    esedb_file = pyesedb.file()
    esedb_file.open(edb_path)
    table = esedb_file.get_table_by_name("Favorites")
    # column_names = {}
    # for idx, column in enumerate(table.columns):
    #     column_names[column.name] = idx
    # print(column_names)
    #
    # need_dict = {'IsDeleted': 0, 'IsFolder': 1, 'DateUpdated': 10, 'Title': 16, 'URL': 17}
    #
    # key_list = [0, 1, 10, 16, 17]

    # {'IsDeleted': 0, 'IsFolder': 1, 'RoamDisabled': 2, 'RowId': 3, 'IsWebNotes': 4, 'DisplayMode': 5, 'IsAllowedToBeOrphan': 6, 'IsAwaitingDeletion': 7, 'IsEnterprise': 8, 'IsOrphaned': 9, 'DateUpdated': 10, 'FaviconFile': 11, 'HashedUrl': 12, 'ItemId': 13, 'OrderNumber': 14, 'ParentId': 15, 'Title': 16, 'URL': 17, 'DateSyncedWithIE': 18}

    for record in table.records:
        # IsDeleted_name = record.get_column_name(0)
        # IsDeleted_dtype = record.get_column_type(0)
        IsDeleted_data = record.get_value_data(0)

        # IsFolder_name = record.get_column_name(1)
        # IsFolder_dtype = record.get_column_type(1)
        IsFolder_data = record.get_value_data(1)

        if IsDeleted_data == b'*' and IsFolder_data == b'*':
            # DateUpdated_name = record.get_column_name(10)
            # DateUpdated_dtype = record.get_column_type(10)
            DateUpdated = get_microsecs(record.get_value_data(10))

            # Title_name = record.get_column_name(16)
            # Title_dtype = record.get_column_type(16)
            Title = record.get_value_data(16).decode('utf-16le')

            # URL_name = record.get_column_name(17)
            # URL_dtype = record.get_column_type(17)
            URL = record.get_value_data(17).decode('utf-16le')

            lis.append([Title, URL, DateUpdated, ''])
            # print([DateUpdated_data, Title_data, URL_data])
    #esedb_file.close()
    # print(lis)
    return lis


if __name__ == '__main__':
    import os

    edge_bookmark_db = os.path.join(os.path.expanduser("~"),
                                    'AppData\\Local\\Packages\\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\\AC\\MicrosoftEdge\\User\\Default\\DataStore\\Data\\nouser1\\120712-0049\\DBStore',
                              'spartan.edb')

    print(edge_bookmark_db)
    print(get_edge_list(edge_bookmark_db))
