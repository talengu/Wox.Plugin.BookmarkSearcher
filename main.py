# encoding=utf8

"""
Wox支持使用Python进行插件的开发。Wox自带了一个打包的Python及其标准库，所以使用Python 插件的用户不必自己再安装Python环境。
同时，Wox还打包了requests和beautifulsoup4两个库， 方便用户进行网络访问与解析。
ref: http://doc.getwox.com/zh/plugin/python_plugin.html
"""

import webbrowser
from wox import Wox, WoxAPI
from  bookmark_searcher import bookmark_searcher


class BSearcher(Wox):
    # def __init__(self):
    #     # self.mSearcher = bookmark_searcher()
    #     # ToDo: 看是不是卡顿
    #     # self.start_time = time.time()
    #     self.mSearcher = bookmark_searcher()

    # 必须有一个query方法，用户执行查询的时候会自动调用query方法
    def query(self, query):
        mSearcher = bookmark_searcher()
        res_from_bookmarks = mSearcher.do_search(query)
        results = []
        if query != '':
            for item in res_from_bookmarks:
                title = item[0]
                url = item[1]
                results.append({
                    "Title": title,
                    "SubTitle": "{}".format(url),
                    "IcoPath": "Images/app.ico",
                    "JsonRPCAction": {
                        # 这里除了自已定义的方法，还可以调用Wox的API。调用格式如下：Wox.xxxx方法名
                        # 方法名字可以从这里查阅https://github.com/qianlifeng/Wox/blob/master/Wox.Plugin/IPublicAPI.cs 直接同名方法即可
                        "method": "openUrl",
                        # 参数必须以数组的形式传过去
                        "parameters": [url],
                        # 是否隐藏窗口
                        "dontHideAfterAction": True}
                })
            if results == []:
                results.append({
                    "Title": "None",
                    "SubTitle": "Query: {}".format(query),
                    "IcoPath": "Images/app.ico"
                })
        return results

    def openUrl(self, url):
        # open the browser
        webbrowser.open(url)
        # todo:doesn't work when move this line up
        WoxAPI.change_query(url)


if __name__ == "__main__":
    BSearcher()
