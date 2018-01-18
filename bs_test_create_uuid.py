from  bookmark_searcher import bookmark_searcher
import time
n = bookmark_searcher()

key = '开源'
res = n.do_search(key)
print(res)
print(len(res))

start_time=time.time()
time.sleep(2)
end_time=time.time()
print('%0.2f'%(end_time-start_time))

import uuid

name = "test_name"
namespace = "test_namespace"

print(uuid.uuid1())  # 带参的方法参见Python Doc
# 0d5efc38-fc09-11e7-9d57-38d547a9452b