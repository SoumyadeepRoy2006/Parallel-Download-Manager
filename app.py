from pprint import pprint
from info_check import get_info
from partitioner import partition

PARTS = 10

#info = get_info("https://fastly.picsum.photos/id/900/5000/5000.jpg?hmac=5axe9KJd4BcFevLbLG498ymr5pknvOCw-3Htinb-iGc")
#pprint(info)

#filesize = 101*1024**2 #1602571
#
#partitions = partition(filesize, PARTS)
#print(partitions)