class NotImplementedInterface(Exception):
    pass

class Interface(object):

    def __init__(self, path):
        self.path = path

    def get(self, filename):
        raise NotImplementedInterface

    def add(self, filename, filedata):
        raise NotImplementedInterface

    def modify(self, filename, filedata):
        raise NotImplementedInterface

    def lsfiles(self):
        raise NotImplementedInterface

    def search(self):
        raise NotImplementedInterface

    def delete(self):
        raise NotImplementedInterface
