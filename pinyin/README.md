pinyin.py
=========

汉字转拼音,With Python


Example:

    from pinyin import PinYin
    
    test = PinYin()
    test.load_word()
    test.hanzi2pinyin(string='你好世界')


Out:

    test.hanzi2pinyin(string='你好世界')
    ['diao', 'yu', 'dao', 'shi', 'zhong', 'guo', 'de']    
    test.hanzi2pinyin_split(string='你好世界', split="-")
    diao-yu-dao-shi-zhong-guo-de

ref: http://www.jb51.net/article/65496.htm