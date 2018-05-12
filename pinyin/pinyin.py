#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    Author:cleverdeng
    E-mail:clverdeng@gmail.com
"""

__version__ = '0.9'
__all__ = ["PinYin"]

import os.path


class PinYin(object):
    def __init__(self, dict_file='word.data'):
        self.word_dict = {}
        self.dict_file = dict_file


    def load_word(self):
        if not os.path.exists(self.dict_file):
            raise IOError("NotFoundFile")

        with open(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                try:
                    line = f_line.split('    ')
                    self.word_dict[line[0]] = line[1]
                except:
                    line = f_line.split('   ')
                    self.word_dict[line[0]] = line[1]


    def hanzi2pinyin(self, string=""):
        result = []
        if not isinstance(string, str):
            string = string.decode("utf-8")
        
        for char in string:
            key = '%X' % ord(char)
            split_result = self.word_dict.get(key, char).split()
            if len(split_result) > 0:
                result.append(split_result[0][:-1].lower())
            else:
                result.append("")

        return result


    def hanzi2pinyin_split(self, string="", split=""):
        result = self.hanzi2pinyin(string=string)
        if split == "":
            return result
        else:
            return split.join(result)


if __name__ == "__main__":
    test = PinYin()
    test.load_word()
    string = "好的,./好的yinwen"
    print("in: %s" % string)
    print("out: %s" % str(test.hanzi2pinyin(string=string)))
    print("out: %s" % test.hanzi2pinyin_split(string=string, split=" "))
