import os

import interface.basefs
import interface.gitinterface


class Service(object):
    
    def __init__(self, path, name=None, iotype=None):
        if name is None:
            self.name = path.split('/')[-1]
        else:
            self.name = name
        if iotype is None:
            if os.path.exists(os.path.join(path, '.git')):
                self.interface = interface.gitinterface.GitInterface(path)
            else:
                self.interface = interface.basefs.BaseFSInterface(path)
        elif iotype == 'git':
            self.interface = interface.gitinterface.GitInterface(path)
        elif iotype == 'base':
            self.interface = interface.basefs.BaseFSInterface(path)
        else:
            raise Exception("Not support iotype.")
