import hashlib


def md5(text):
    m = hashlib.md5()
    m.update(text)
    return unicode(m.hexdigest())
