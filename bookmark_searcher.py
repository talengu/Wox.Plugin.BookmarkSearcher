# -*- coding: utf-8 -*-
"""Description :
"""
import os
from pinyin.pinyin import PinYin
from diffent_browsers import chrome, edge


class bookmark_searcher(object):

    def __init__(self):

        this_file_path = os.path.realpath(__file__)
        self.cfg_path = os.path.join(os.path.dirname(this_file_path), "setting.txt")

        self.cfg_dict = self.get_cfg()

        self.lis = [["设置 settings txt", self.cfg_path, 13289095048684753, '']]

        chrome_bookmark = os.path.join(os.path.expanduser("~"),
                                       self.cfg_dict['chrome'],
                                       'Bookmarks')
        chromium_bookmark = os.path.join(os.path.expanduser("~"),
                                         self.cfg_dict['chromium'],
                                         'Bookmarks')

        self.edge_bookmark_db = os.path.join(os.path.expanduser("~"),
                                             self.cfg_dict['edge'],
                                             'spartan.edb')

        use_list = self.cfg_dict['use'].split(',')
        if "chrome" in use_list:
            self.lis += chrome.get_chrome_list(chrome_bookmark)
        # if "chromium" in use_list:
        #     self.lis += chrome.get_chrome_list(chromium_bookmark)

        if "edge" in use_list:
            self.lis += edge.update_edge(self.edge_bookmark_db)

        self.pinyin_item()  # 将pinyin准备好

    def get_cfg(self):
        cfg_dict = {}
        with open(self.cfg_path, 'r') as ffile:
            for line in ffile.readlines():
                items = line.split('=')
                cfg_dict[items[0]] = items[1][:-1]

        return cfg_dict

    def pinyin_item(self):
        # pinyin dict
        self.py = PinYin('pinyin/word.data')
        self.py.load_word()
        for i, item in enumerate(self.lis):
            # 拼音化
            han_item = ''
            all_pin = first_pin = ''
            for x in item[0].split(' '):
                han_item += x
            item_pinyin = self.py.hanzi2pinyin_split(string=han_item, split=" ")
            for x in item_pinyin.split(' '):
                if x != '':
                    all_pin += x
                    first_pin += x[0]
            res_pin = item_pinyin + ' ' + all_pin + ' ' + first_pin
            self.lis[i][3] = res_pin

    def do_search(self, key):
        result_lis = []
        if key == "update edge":  # update edge的bookmarks 因为当edge打开的时候关闭了。
            #edge.update_edge(self.edge_bookmark_db, isUpdate=True)
            import shutil
            shutil.rmtree('cache')
            return [["update edge It will closing Edge", '']]

        for item in self.lis:
            # 将单词变为low 方便索引
            if item[0].lower().find(key) != -1 or item[0].lower().find(key.lower()) != -1 \
                    or item[1].lower().find(key) != -1 \
                    or item[3].find(key) != -1:
                result_lis.append(item)

        # 按照时间进行排序
        search_result = sorted(result_lis, key=lambda x: x[2], reverse=True)
        return [x[:2] for x in search_result]


# start = time.time()
# ....code
# end = time.time()
# print('Runs %0.2f seconds.' % (end - start))


if __name__ == "__main__":
    n = bookmark_searcher()

    key = 'up'
    res = n.do_search(key)
    print(res)
    print(len(res))
