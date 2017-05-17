# encoding=utf-8
import gevent
from gevent import monkey
import requests
import uuid
import sys
import time

monkey.patch_all()

reload(sys)
sys.setdefaultencoding('utf8')


def write_file(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    if resp.status_code == 200:
        with open('./download/' + str(uuid.uuid1()), 'w') as f:
            f.write(resp.text)


urls = []
with open('xaa', 'r') as f:
    data = f.readline()
    while data and data.strip():
        urls.append(data.strip())
        data = f.readline()

print '%s start...' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

jobs = [gevent.spawn(write_file, url)
        for url in urls]
gevent.joinall(jobs)


#for url in urls:
#   write_file(url)

print '%s end...' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
