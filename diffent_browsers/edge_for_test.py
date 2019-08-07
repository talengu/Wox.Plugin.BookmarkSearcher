# -*- coding: utf-8 -*-
"""Description :
参考一个 ese 到 sqlite格式转化的项目
ref: https://github.com/libyal/libesedb
ref: https://programtalk.com/vs2/python/3146/SrumMonkey/SrumMonkey.py/
"""
# talen@uestc 
# 2018/12/13 
from __future__ import print_function, division, absolute_import, unicode_literals

import pyesedb

# EDB = "/Users/talen/github/Wox.Plugin.BookmarkSearcher/demo_datas/DBStore/spartan.edb"
# esedb_file = pyesedb.file()
# esedb_file.open(EDB)

# MSysObjects
# MSysObjectsShadow
# MSysObjids
# MSysLocales
# RowId
# FolderStash
# FileCleanup
# Favorites
# Folder
# ReadingList
# OpenedBooks
# Bookmarks
# CARules
# ExtensionsList
# BhxActionsTable
# BhxContentScriptTable
# BhxHostTable
# Library
# TopSites
# UriToAppIdMapping
# SweptTabs
# PageSettings
# PackagedExtensionsStorage
# SideLoadedExtensionsStorage
# ExtensionIdsList
# AutoFormFillStorage
# BookAnnotations
# CloudLibrary
# BookPushOperations
# FreeFormInks
# AutoFormFillAddressStorage
# AutoFormFillPaymentStorage
# UrlHistory
# UrlVisit
# EdgeScenarioLogger
# TypedUrls

# for table in esedb_file.tables:
#     table_name = table.name
#     print(table_name)
from pyesedb import column_types as DBTYPES

import struct
import uuid

import datetime
import logging


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
    # new_datetime = new_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
    return new_datetime


def GetWinTimeStamp(raw_timestamp):
    '''Return Datetime from raw Win32Timestamp'''
    timestamp = struct.unpack("Q", raw_timestamp)[0]

    microsecs, _ = divmod(timestamp, 10)
    timeDelta = datetime.timedelta(microseconds=microsecs)

    origDateTime = datetime.datetime(1601, 1, 1)

    new_datetime = origDateTime + timeDelta
    # new_datetime = new_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
    return new_datetime


class esedbHandler(object):
    def __init__(self,EDB):

        self.esedb_file = pyesedb.file()
        self.esedb_file.open(EDB)
        for table in self.esedb_file.tables:
            if len(table.records) > 0:
                print(table.name +" "+ str(len(table.records))+"--------------------------------------------------talen")
                print(self.get_table_value(table.name))
        #TABLE = pyesedb.table()


    def get_table_value(self,table_name="Favorites"):
        table = self.esedb_file.get_table_by_name(table_name)
        column_names = []
        for column in table.columns:
            column_names.append(column.name)
        print(column_names)

        num_of_columns = table.get_number_of_columns()
        items_to_insert = []
        for record in table.records:
            enum_record = self._EnumerateRecord(
                num_of_columns,
                record
            )
            items_to_insert.append(enum_record)
        return items_to_insert

    def _EnumerateRecord(self, num_of_columns, record):
        '''Enumerate vales for a record

        Args:
            num_of_columns: The number of columns in the record
            record: a pyesedb record object

        Returns:
            values: the record as a dictionary'''
        values = {}
        for index in range(0, num_of_columns):
            self.CURRENT_VALUES = values
            data = self._GetColumnValueFromRecord(
                record,
                index
            )

            values.update(data)

        return values

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
            print("URL "+data.decode('utf-16le'))
            # value = self._GetCustomValue(
            #     SrumHandler.CUSTOM_COLUMNS[name],
            #     data
            # )
            # item = {name: value}
            # return item
        if name=='Title':
            print("title " + data.decode('utf-16le'))


        if dtype == DBTYPES.DOUBLE_64BIT:
            value = struct.unpack('d', data)[0]
        if dtype == DBTYPES.FLOAT_32BIT:
            value = struct.unpack('f', data)[0]
        if dtype == DBTYPES.BOOLEAN:
            value = struct.unpack('?', data)[0]
        elif dtype == DBTYPES.INTEGER_8BIT_UNSIGNED:
            value = struct.unpack('B', data)[0]
        elif dtype == DBTYPES.INTEGER_16BIT_SIGNED:
            value = struct.unpack('h', data)[0]
        elif dtype == DBTYPES.INTEGER_16BIT_UNSIGNED:
            value = struct.unpack('H', data)[0]
        elif dtype == DBTYPES.INTEGER_32BIT_SIGNED:
            value = struct.unpack('i', data)[0]
        elif dtype == DBTYPES.INTEGER_32BIT_UNSIGNED:
            value = struct.unpack('I', data)[0]
        elif dtype == DBTYPES.INTEGER_64BIT_SIGNED:
            value = struct.unpack('q', data)[0]
        elif dtype == DBTYPES.GUID:
            value = uuid.UUID(bytes=data)
        elif dtype == DBTYPES.LARGE_TEXT:
            value = data
        elif dtype == DBTYPES.SUPER_LARGE_VALUE:
            value = data
        elif dtype == DBTYPES.TEXT:
            value = data
        elif dtype == DBTYPES.BINARY_DATA:
            value = data
        elif dtype == DBTYPES.LARGE_BINARY_DATA:
            value = data
        elif dtype == DBTYPES.DATE_TIME:
            value = GetOleTimeStamp(data)
        else:
            msg = 'UNKNOWN TYPE {}'.format(dtype)
            #logging.error(msg)
            #raise Exception(msg)

        item = {name: value}

        return item

if __name__ == '__main__':
    import os
    edge_bookmark_db = os.path.join(os.path.expanduser("~"),
                                    'AppData\\Local\\Packages\\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\\AC\\MicrosoftEdge\\User\\Default\\DataStore\\Data\\nouser1\\120712-0049\\DBStore',
                              'spartan.edb')
    EDB = "..\\demo_datas\\DBStore\\spartan.edb"
    m=esedbHandler(edge_bookmark_db)
    print("---------------------------------------------------")
    print(m.get_table_value())




    # TABLE = pyesedb.table()
    # table = esedb_file.get_table_by_name("Bookmarks")







