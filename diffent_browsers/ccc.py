# -*- coding: utf-8 -*-
"""Description :
"""
# talen@uestc 
# 2018/12/13 
from __future__ import print_function, division, absolute_import, unicode_literals

'''Create Functions that can be called from SQLite'''
import os


def RegisterFunctions(dbh):
    '''Register your created functions here'''
    dbh.create_function('basename', 1, Basename)


def Basename(filename):
    '''Get the base name of a fullname string'''
    try:
        value = os.path.basename(filename)
    except:
        value = filename

    return value