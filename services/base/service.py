import os

import interface.basefs
import interface.gitinterface


class Service(object):
    
    def __init__(self, path, name=None, searchengine=None, iotype=None):
        if name is None:
            self.name = path.split('/')[-1]
        else:
            self.name = name
        if iotype is None:
            if os.path.exists(os.path.join(path, '.git')):
                self.interface = interface.gitinterface.GitInterface(path, searchengine=searchengine)
            else:
                self.interface = interface.basefs.BaseFSInterface(path, searchengine=searchengine)
        elif iotype == 'git':
            self.interface = interface.gitinterface.GitInterface(path, searchengine=searchengine)
        elif iotype == 'base':
            self.interface = interface.basefs.BaseFSInterface(path, searchengine=searchengine)
        else:
            raise Exception("Not support iotype.")

    def backup(self, path, bare=False):
        self.interface.backup(path, bare=bare)
