
from base64 import b64encode

if __name__ == '__main__':
    a = 'Basic {}'.format(b64encode("{}:{}".format("qgs", "cxu@vSqI!PhBgoWqSD").encode("utf-8")))
    print(a)







