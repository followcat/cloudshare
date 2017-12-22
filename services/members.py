import os
import glob

import services.member


class Members(object):

    default_member_name = 'default'

    def __init__(self, path, acc_repos, bd_repos, co_repos, cv_repos, jd_repos, mult_peo, search_engine, es_config):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.acc_repos = acc_repos
        self.bd_repos = bd_repos
        self.co_repos = co_repos
        self.cv_repos = cv_repos
        self.jd_repos = jd_repos
        self.mult_peo = mult_peo
        self.search_engine = search_engine
        self.es_config = es_config
        self.members = dict()
        for member_path in glob.glob(os.path.join(self.path, '*')):
            if os.path.isdir(member_path):
                str_name = os.path.split(member_path)[1]
                name = unicode(str_name, 'utf-8')
                member = services.member.Member(services.member.SimulationMember(member_path, name),
                                                account={'acc': acc_repos}, bidding={'bd': bd_repos},
                                                company={'co': co_repos}, curriculumvitae={'cv': cv_repos,
                                                'repo': self.cv_repos[0], 'storage': self.cv_repos[1:]},
                                                search_engine={'idx': search_engine, 'config': es_config},
                                                jobdescription={'jd': jd_repos}, people={'peo': mult_peo})
                member.setup({'storageCV':  'cloudshare',
                              'storagePEO': 'peostorage',
                              'limitPEO':   'peolimit',
                              'storageCO':  'corepo',
                              'storageJD':  'jdrepo'})
                self.members[name] = member
        self.load_default_member()
        self._defaultmember = self.members[self.default_member_name]

    def load_default_member(self):
        path = os.path.join(self.path, self.default_member_name)
        member = services.member.DefaultMember(services.member.SimulationMember(path, self.default_member_name),
                                                account={'acc': self.acc_repos}, bidding={'bd': self.bd_repos},
                                                company={'co': self.co_repos}, curriculumvitae={'cv': self.cv_repos,
                                                'repo': self.cv_repos[-1], 'storage': self.cv_repos[:-1]},
                                                search_engine={'idx': self.search_engine, 'config': self.es_config},
                                                jobdescription={'jd': self.jd_repos}, people={'peo': self.mult_peo})
        member.setup({'storageCV':  'cvindividual',
                      'storagePEO': 'peoindividual',
                      'limitPEO':   'peolimit',
                      'storageCO':  'corepo',
                      'storageJD':  'jdrepo'})
        self.members[self.default_member_name] = member

    def exists(self, name):
        return name in self.members

    def create(self, name):
        assert not self.exists(name)
        path = os.path.join(self.path, name)
        member = services.member.Member(services.member.SimulationMember(path, name),
                                                account={'acc': self.acc_repos}, bidding={'bd': self.bd_repos},
                                                company={'co': self.co_repos}, curriculumvitae={'cv': self.cv_repos,
                                                'repo': self.cv_repos[0], 'storage': self.cv_repos[1:]},
                                                search_engine={'idx': self.search_engine, 'config': self.es_config},
                                                jobdescription={'jd': self.jd_repos}, people={'peo': self.mult_peo})
        member.setup({'storageCV':  'cloudshare',
                      'storagePEO': 'peostorage',
                      'limitPEO':   'peolimit',
                      'storageCO':  'corepo',
                      'storageJD':  'jdrepo'})
        self.members[name] = member

    def get(self, name):
        return self.members[name]

    def use(self, name, id):
        result = self.members[self.default_member_name]
        if name:
            result = self.members[name].use(id)
        return result

    def names(self):
        return self.members.keys()

    def allprojects(self):
        result = dict()
        for each in self.members:
            member = self.members[each]
            for name, project in member.projects.items():
                result[project.id] = project
        return result

    def backup(self, path):
        members_path = os.path.join(path, "members")
        os.mkdir(members_path)
        for each in self.members:
            member = self.members[each]
            member.backup(members_path)

    @property
    def defaultmember(self):
        return self._defaultmember
