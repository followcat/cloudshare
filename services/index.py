import os
import glob
import cPickle
import collections

import utils.builtin


class ReverseIndexing(object):

    indexkeys = ('names',
                 'current_places',
                 'expectation_places',
                 'education',
                 'gender',
                 'marital_status',
                 'business')

    def __init__(self, path, cvsvc):
        self.path = path
        self.cvs = cvsvc.svcls
        self.index = {}

    def setup(self):
        self.load()
        # self.update()

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        for name in self.index:
            industrypath = utils.builtin.industrytopath(name)
            savepath = os.path.join(self.path, industrypath)
            with open(savepath, 'w') as fp:
                cPickle.dump(self.index[name], fp)

    def load(self):
        for cv in self.cvs:
            name = cv.name
            loadpath = os.path.join(self.path, utils.builtin.industrytopath(name))
            if not os.path.exists(loadpath):
                continue
            with open(loadpath) as fp:
                index = cPickle.load(fp)
                self.index[name] = index

    def update(self):
        for svc in self.cvs:
            self.updatecv(svc)
        self.save()

    def updatecv(self, svc):
        assert svc.name
        svc_name = svc.name
        cv_index = {
                self.indexkeys[0]: set(),
                self.indexkeys[1]: dict(),
                self.indexkeys[2]: dict(),
                self.indexkeys[3]: dict(),
                self.indexkeys[4]: dict(),
                self.indexkeys[5]: dict(),
        }
        if svc_name in self.index:
            cv_index = self.index[svc_name]
        for name in svc.names():
            if name not in cv_index['names']:
                yamlinfo = svc.getyaml(name)
                index = self.genindex(name, yamlinfo)
                self.merge(cv_index, index)
        self.index[svc_name] = cv_index

    def upgrade(self, selected):
        assert set(selected).issubset(set(self.indexkeys))
        for svc in self.cvs:
            self.upgradecv(svc, selected)
        self.save()

    def upgradecv(self, svc, selected):
        assert svc.name
        svc_name = svc.name
        if svc_name in self.index:
            cv_index = self.index[svc_name]
        for name in svc.names():
            if name in cv_index['names']:
                yamlinfo = svc.getyaml(name)
                index = self.genindex(name, yamlinfo, selected)
                self.merge(cv_index, index)
        self.index[svc_name] = cv_index
        self.save()

    def genindex(self, name, yamlinfo, selected=None):
        if selected is None:
            selected = self.indexkeys
        index_map = {
                self.indexkeys[0]: set([name]),
                self.indexkeys[1]: self._cur_places(yamlinfo),
                self.indexkeys[2]: self._exp_places(yamlinfo),
                self.indexkeys[3]: self._education(yamlinfo),
                self.indexkeys[4]: self._gender(yamlinfo),
                self.indexkeys[5]: self._mar_status(yamlinfo),
                self.indexkeys[6]: self._business(yamlinfo),
            }
        result = dict()
        for each in selected:
            result[each] = index_map[each]
        return result

    def merge(self, left, right):
        for key in right:
            if isinstance(right[key], set):
                if key not in left:
                    left[key] = set()
                left[key].update(right[key])
            if isinstance(right[key], dict):
                if key not in left:
                    left[key] = dict()
                self.merge(left[key], right[key])
        return True

    def get(self, filtedict, uses=None):
        """
            # need key and value
            # keys:
            #     'current_places',
            #     'expectation_places',
            #     'education',
            #     'gender',
            #     'marital_status',
            #     'business'
        """
        if uses is None:
            uses = self.index.keys()
        results = set()
        for use in uses:
            assert use in self.index
            parts = collections.defaultdict(set)
            result = set()
            index = self.index[use]
            for key in filtedict:
                assert key in index
                for value in filtedict[key]:
                    if value in index[key]:
                        parts[key].update(index[key][value])
            for key in parts:
                if not result:
                    result.update(parts[key])
                result.intersection_update(parts[key])
            results.update(result)
        return results

    def filte(self, filtedict, selected, uses=None):
        """
            # need key and value
            # keys:
            #     'current_places',
            #     'expectation_places',
            #     'education',
            #     'gender',
            #     'marital_status',
            #     'business'
        """
        return self.get(filtedict, uses) & selected

    def get_indexkeys(self, selected, keywords, uses=None):
        assert set(selected).issubset(set(self.indexkeys))
        if uses is None:
            uses = self.index.keys()
        results = set()
        for use in uses:
            index = self.index[use]
            for selecte in selected:
                result = filter(lambda w: [kw for kw in keywords if kw in w],
                                index[selecte])
                results.update(result)
        return results

    def _cur_places(self, yamlinfo):
        result = dict()
        if 'current' in yamlinfo and 'places' in yamlinfo['current']:
            for place in yamlinfo['current']['places']:
                result[place] = set([yamlinfo['id']])
        return result

    def _exp_places(self, yamlinfo):
        result = dict()
        if 'expectation' in yamlinfo and 'places' in yamlinfo['expectation']:
            for place in yamlinfo['expectation']['places']:
                result[place] = set([yamlinfo['id']])
        return result

    def _education(self, yamlinfo):
        result = dict()
        if 'education' in yamlinfo and yamlinfo['education']:
            education = yamlinfo['education']
            result[education] = set([yamlinfo['id']])
        return result

    def _gender(self, yamlinfo):
        result = dict()
        if 'gender' in yamlinfo and yamlinfo['gender']:
            gender = yamlinfo['gender']
            result[gender] = set([yamlinfo['id']])
        return result

    def _mar_status(self, yamlinfo):
        result = dict()
        if 'marital_status' in yamlinfo and yamlinfo['marital_status']:
            marital_status = yamlinfo['marital_status']
            result[marital_status] = set([yamlinfo['id']])
        return result

    def _business(self, yamlinfo):
        result = collections.defaultdict(set)
        if 'company' in yamlinfo['experience'] and yamlinfo['experience']['company']:
            for c in yamlinfo['experience']['company']:
                if 'business' in c:
                    result[c['business']].add(yamlinfo['id'])
        return result
