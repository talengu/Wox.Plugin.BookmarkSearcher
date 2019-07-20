import json
import os
from pinyin.pinyin import PinYin


class bookmark_searcher(object):
    # in windows
    bookmark_name = os.path.join(os.path.expanduser("~"), 'AppData//Local//Google//Chrome//User Data//Default',
                                 'Bookmarks')
    # in mac
    #bookmark_name = os.path.join(os.path.expanduser("~"), 'Library/Application Support/Google/Chrome/Default',
            #                     'Bookmarks')

    def __init__(self, in_name=bookmark_name):
        self.lis = []
        data = self.load(in_name)
        child_items = data['roots']['bookmark_bar']['children'] + data['roots']['other']['children']
        self.make_list(child_items)  # 将数据准备好
        self.pinyin_item()  # 将pinyin准备好


    def store(self, data, store_name='data.json'):
        with open(store_name, 'w') as json_file:
            json_file.write(json.dumps(data))

    def load(self, load_name):
        with open(load_name, encoding='UTF-8') as json_file:
            data = json.load(json_file)
            return data

    def make_list(self, child_items):
        for item in child_items:
            if 'children' in item.keys():
                # print(item['name']) # 类别标签
                # print(type(item['children']))
                self.make_list(item['children'])
            else:
                mItem = [item['name'], item['url'], item['date_added'], '']
                self.lis.append(mItem)
                # print(item['name'],item['url'])

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
        for item in self.lis:
            # 将单词变为low 方便索引
            if item[0].lower().find(key) != -1 or item[0].lower().find(key.lower()) != -1\
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

    key = 'ban'
    res = n.do_search(key)
    print(res)
    print(len(res))
