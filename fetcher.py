import pycurl
import hashlib
import os


class Fetcher(object):
    def __init__(self, urls, path):
        self.urls = urls
        self.path = path
        self.m = pycurl.CurlMulti()
        if not os.path.exists(path):
            os.makedirs(path)

    def fetch(self):
        if not urls or len(urls) == 0:
            print('empty urls')
            return

        for idx, url in enumerate(urls):
            fdir = './%s/%s' % (self.path,
                                hashlib.md5(url.encode()).hexdigest())
            if os.path.exists(fdir):
                print('%s exits,skip it...' % fdir)
                continue
            f = open(fdir, 'wb')
            locals()['c' + str(idx)] = pycurl.Curl()
            locals()['c' + str(idx)].setopt(pycurl.URL, url)
            locals()['c' + str(idx)].setopt(pycurl.WRITEDATA, f)
            self.m.add_handle(locals()['c' + str(idx)])

        while 1:
            ret, num_handles = self.m.perform()
            if ret != pycurl.E_CALL_MULTI_PERFORM:
                break

        while num_handles:
            ret = self.m.select(1.0)
            if ret == -1:
                continue
            while 1:
                ret, num_handles = self.m.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break

        print('downloading complete...')


if __name__ == '__main__':
    urls = []
    with open('data', 'r') as f:
        data = f.readline().strip()
        while data:
            urls.append(data)
            data = f.readline().strip()

    fetcher = Fetcher(urls, 'download')
    fetcher.fetch()
