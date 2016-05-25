class Service(object):
    
    def __init__(self, interface, name=None):
        if name is None:
            self.name = interface.path.split('/')[-1]
        else:
            self.name = name
        self.interface = interface
