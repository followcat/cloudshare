import os
import glob

import services.member
import services.base.kv_storage
import services.base.name_storage
import services.operator.search
import services.operator.multiple


class Members(object):

    default_member_name = 'default'

    def __init__(self, path, matching, bd_repos, co_repos, cv_repos, jd_repos, mult_peo, search_engine, es_config):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.matching = matching
        self.bd_repos = bd_repos
        self.co_repos = co_repos
        self.cv_repos = cv_repos
        self.jd_repos = jd_repos
        self.mult_peo = mult_peo
        self.search_engine = search_engine
        self.es_config = es_config
        self.members = dict()
        self.cv_storage = services.curriculumvitae.SearchIndex(
                            services.operator.multiple.Multiple(self.cv_repos[1:]))
        self.active_members = services.base.name_storage.NameStorage(self.path, 'memlist')
        self.member_details = services.member.SimulationMember(os.path.join(self.path, 'config'), 'memconfig')
        for member_id in self.active_members.ids:
            member_info = self.member_details.getyaml(member_id)
            if member_info['name'] == 'default':
                self.load_default_member(member_id)
                self._defaultmember = self.members[self.default_member_name]
                continue
            member_path = os.path.join(self.path, member_info['name'])
            if os.path.isdir(member_path):
                name = unicode(member_info['name'], 'utf-8')
                member = services.member.Member(self.member_details, matching={'mch': matching},
                                                bidding={'bd': bd_repos}, company={'co': co_repos},
                                                curriculumvitae={'cv': cv_repos, 'repo': self.cv_repos[0],
                                                                 'storage': self.cv_storage},
                                                search_engine={'idx': search_engine, 'config': es_config},
                                                jobdescription={'jd': jd_repos}, people={'peo': mult_peo})
                member.setup({'id':         member_id,
                              'name':       name,
                              'storageCV':  'cloudshare',
                              'storagePEO': 'peostorage',
                              'limitPEO':   'peolimit',
                              'storageCO':  'corepo',
                              'storageJD':  'jdrepo'})
                self.members[name] = member
        self.idx_setup()

    def load_default_member(self, member_id):
        member_info = self.member_details.getyaml(member_id)
        path = os.path.join(self.path, self.default_member_name)
        member = services.member.DefaultMember(self.member_details,
                                                company={'co': self.co_repos}, matching={'mch': self.matching},
                                                curriculumvitae={'cv': self.cv_repos, 'repo': self.cv_repos[0],
                                                                 'storage': self.cv_storage},
                                                search_engine={'idx': self.search_engine, 'config': self.es_config},
                                                jobdescription={'jd': self.jd_repos}, people={'peo': self.mult_peo})
        member.setup({'name':       self.default_member_name,
                      'id':         member_id,
                      'storageCV':  'cvindividual',
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
        member = services.member.Member(self.member_details, matching={'mch': self.matching},
                                                bidding={'bd': self.bd_repos}, company={'co': self.co_repos},
                                                curriculumvitae={'cv': self.cv_repos, 'repo': self.cv_repos[0],
                                                                 'storage': self.cv_storage},
                                                search_engine={'idx': self.search_engine, 'config': self.es_config},
                                                jobdescription={'jd': self.jd_repos}, people={'peo': self.mult_peo})
        member.setup({'name':       name,
                      'storageCV':  'cloudshare',
                      'storagePEO': 'peostorage',
                      'limitPEO':   'peolimit',
                      'storageCO':  'corepo',
                      'storageJD':  'jdrepo'})
        self.active_members.add(core.basedata.DataObject(metadata=member.config, data=''))
        self.members[name] = member

    def idx_setup(self):
        self.cv_storage.setup(self.search_engine, self.es_config['CV_STO'])

    def idx_updatesvc(self):
        self.cv_storage.updatesvc(self.es_config['CV_STO'], self.cv_storage.data_service.services[0].name, numbers=1000)

    def get(self, name):
        return self.members[name]

    def use(self, name, id):
        result = None
        if name:
            result = self.members[name].use(id)
        if not result:
            result = self.members[self.default_member_name]
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
