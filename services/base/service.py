import os

import interface.basefs
import interface.gitinterface


class Service(object):
    
    def __init__(self, path, name=None, iotype=None):
        if name is None:
            self._name = path.split('/')[-1]
        else:
            self._name = name
        if iotype is None:
            if os.path.exists(os.path.join(path, '.git')):
                self.interface = interface.gitinterface.GitInterface(path, name)
            else:
                self.interface = interface.basefs.BaseFSInterface(path, name)
        elif iotype == 'git':
            self.interface = interface.gitinterface.GitInterface(path, name)
        elif iotype == 'base':
            self.interface = interface.basefs.BaseFSInterface(path, name)
        else:
            raise Exception("Not support iotype.")

    def backup(self, path, bare=False):
        self.interface.backup(path, bare=bare)

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._name
    
