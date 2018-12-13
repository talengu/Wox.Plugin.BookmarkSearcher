# -*- coding: utf-8 -*-
"""Description :
"""
# talen@uestc 
# 2018/12/13 
from __future__ import print_function, division, absolute_import, unicode_literals
import pyesedb
from pyesedb import column_types as DBTYPES
import struct
import uuid
import datetime

def GetOleTimeStamp(raw_timestamp):
    '''Return Datetime from raw OleTimestamp'''
    timestamp = struct.unpack(
        "d",
        raw_timestamp
    )[0]

    origDateTime = datetime.datetime(
        1899,
        12,
        30,
        0,
        0,
        0
    )
    timeDelta = datetime.timedelta(days=timestamp)
    new_datetime = origDateTime + timeDelta
    new_datetime = new_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
    return new_datetime

class esedbHandler(object):
    def __init__(self):
        EDB = "/Users/talen/github/Wox.Plugin.BookmarkSearcher/demo_datas/DBStore/spartan.edb"
        self.esedb_file = pyesedb.file()
        self.esedb_file.open(EDB)




    def get_table_value(self,table_name="Favorites"):
        table = self.esedb_file.get_table_by_name(table_name)
        column_names = {}
        for idx,column in enumerate(table.columns):
            column_names[column.name]=idx
        print(column_names)

        need_dict={'IsDeleted': 0, 'IsFolder': 1,'DateUpdated': 10,'Title': 16, 'URL': 17}

        key_list=[0,1,10,16,17]

        # {'IsDeleted': 0, 'IsFolder': 1, 'RoamDisabled': 2, 'RowId': 3, 'IsWebNotes': 4, 'DisplayMode': 5, 'IsAllowedToBeOrphan': 6, 'IsAwaitingDeletion': 7, 'IsEnterprise': 8, 'IsOrphaned': 9, 'DateUpdated': 10, 'FaviconFile': 11, 'HashedUrl': 12, 'ItemId': 13, 'OrderNumber': 14, 'ParentId': 15, 'Title': 16, 'URL': 17, 'DateSyncedWithIE': 18}


        for record in table.records:
            for index in key_list:
                self._GetColumnValueFromRecord(record, index)







    def _GetColumnValueFromRecord(self, record, index):
        '''Get enumerated value based off of column and/or type

        Args:
            record: a pyesedb record object
            index: the column index for record
        Return:
            value: The value of a column for the record
        '''
        item = {}
        value = None
        name = record.get_column_name(index)
        dtype = record.get_column_type(index)
        data = record.get_value_data(index)

        if data is None:
            item = {name: None}
            return item

        if name =='URL':
            value = data.decode('utf-16le')
            print("URL "+data.decode('utf-16le'))

        if name=='Title':

            value=data.decode('utf-16le')
            print("title " + value)
        if name =='IsDeleted': # IsFolder
            value=struct.unpack('?', data)[0]
            print('isDeleted')

        if name == '':
            value = GetOleTimeStamp(data)
            print("time ",value)


        # if dtype == DBTYPES.DOUBLE_64BIT:
        #     value = struct.unpack('d', data)[0]
        # if dtype == DBTYPES.FLOAT_32BIT:
        #     value = struct.unpack('f', data)[0]
        # if dtype == DBTYPES.BOOLEAN:
        #     value = struct.unpack('?', data)[0]
        # elif dtype == DBTYPES.INTEGER_8BIT_UNSIGNED:
        #     value = struct.unpack('B', data)[0]
        # elif dtype == DBTYPES.INTEGER_16BIT_SIGNED:
        #     value = struct.unpack('h', data)[0]
        # elif dtype == DBTYPES.INTEGER_16BIT_UNSIGNED:
        #     value = struct.unpack('H', data)[0]
        # elif dtype == DBTYPES.INTEGER_32BIT_SIGNED:
        #     value = struct.unpack('i', data)[0]
        # elif dtype == DBTYPES.INTEGER_32BIT_UNSIGNED:
        #     value = struct.unpack('I', data)[0]
        # elif dtype == DBTYPES.INTEGER_64BIT_SIGNED:
        #     value = struct.unpack('q', data)[0]
        # elif dtype == DBTYPES.GUID:
        #     value = uuid.UUID(bytes=data)
        # elif dtype == DBTYPES.LARGE_TEXT:
        #     value = data
        # elif dtype == DBTYPES.SUPER_LARGE_VALUE:
        #     value = data
        # elif dtype == DBTYPES.TEXT:
        #     value = data
        # elif dtype == DBTYPES.BINARY_DATA:
        #     value = data
        # elif dtype == DBTYPES.LARGE_BINARY_DATA:
        #     value = data
        # elif dtype == DBTYPES.DATE_TIME:
        #     value = GetOleTimeStamp(data)
        # else:
        #     msg = 'UNKNOWN TYPE {}'.format(dtype)
        #     #logging.error(msg)
        #     #raise Exception(msg)


        if value==None:
            return item

        item = {name: value}

        return item

if __name__ == '__main__':
    m=esedbHandler()
    print("---------------------------------------------------")
    print(m.get_table_value())