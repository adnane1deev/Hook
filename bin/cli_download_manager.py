__author__ = 'Asus'


import urllib2

types = {'application/zip': 'zip'}
urls = ["https://github.com/bower/registry/archive/master.zip",
        "https://github.com/bower/bower/archive/master.zip",
        "https://github.com/zendframework/ZendSkeletonApplication/archive/master.zip"]
#url = "http://nodejs.org/dist/v0.10.29/x64/node-v0.10.29-x64.msi"
print
for url in urls:
    u = urllib2.urlopen(url)
    meta = u.info()

    file_name = url.split('/')[-4]+"-"+url.split('/')[-3]+"."+types[meta.getheaders("Content-Type")[0]]

    f = open(file_name, 'wb')

    #print meta.getheaders("Content-Type")
    #print meta.dict

    file_size = int(meta.getheaders("Content-Length")[0])

    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        __buffer = u.read(block_sz)
        if not __buffer:
            break

        file_size_dl += len(__buffer)
        f.write(__buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status += chr(8)*(len(status)+1)
        print status,

    f.close()
    print "\n"