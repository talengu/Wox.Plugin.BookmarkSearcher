from  bookmark_searcher import bookmark_searcher
import time
n = bookmark_searcher()

key = 'ban'
res = n.do_search(key)
print(res)
print(len(res))

start_time=time.time()
time.sleep(2)
end_time=time.time()
print('%0.2f'%(end_time-start_time))