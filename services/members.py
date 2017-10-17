import os
import glob

import services.member


class Members(object):

    default_member_name = 'default'

    def __init__(self, path, acc_repos, cv_repos, jd_repos, mult_peo):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.acc_repos = acc_repos
        self.cv_repos = cv_repos
        self.jd_repos = jd_repos
        self.mult_peo = mult_peo
        self.members = dict()
        for member_path in glob.glob(os.path.join(self.path, '*')):
            if os.path.isdir(member_path):
                str_name = os.path.split(member_path)[1]
                name = unicode(str_name, 'utf-8')
                member = services.member.Member(acc_repos, cv_repos, jd_repos,
                                                mult_peo, member_path, name)
                member.setup({'storageCV':  'cloudshare',
                              'storagePEO': 'peostorage',
                              'storageJD':  'jdstorage'})
                self.members[name] = member
        self.load_default_member()

    def load_default_member(self):
        path = os.path.join(self.path, self.default_member_name)
        member = services.member.DefaultMember(self.acc_repos, self.cv_repos, self.jd_repos,
                                               self.mult_peo, path, self.default_member_name)
        member.setup({'storageCV':  'cvindividual',
                      'storagePEO': 'peoindividual',
                      'storageJD':  'jdstorage'})
        self.members[self.default_member_name] = member

    def exists(self, name):
        return name in self.members

    def create(self, name):
        assert not self.exists(name)
        path = os.path.join(self.path, name)
        member = services.member.Member(self.acc_repos, self.cv_repos, jd_repos,
                                        self.mult_peo, path, name)
        member.setup({'storageCV':  'cloudshare',
                      'storagePEO': 'peostorage',
                      'storageJD':  'jdstorage'})
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
            result.update(member.projects)
        return result

    def backup(self, path):
        members_path = os.path.join(path, "members")
        os.mkdir(members_path)
        for each in self.members:
            member = self.members[each]
            member.backup(members_path)
