import os
import glob
import cPickle


class ReverseIndexing(object):

    indexkeys = ('names',
                 'current_places',
                 'expectation_places',
                 'education',
                 'gender',
                 'marital_status')

    def __init__(self, path, cvsvc):
        self.path = path
        self.cvs = cvsvc.svcls
        self.index = {}

    def setup(self):
        self.load()
        self.update()

    def save(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        for name in self.index:
            savepath = os.path.join(self.path, name)
            with open(savepath, 'w') as fp:
                cPickle.dump(self.index[name], fp)

    def load(self):
        for f in glob.glob(os.path.join(self.path, '*')):
            path, name = os.path.split(f)
            with open(f) as fp:
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

    def genindex(self, name, yamlinfo):
        result = {
                self.indexkeys[0]: set([name]),
                self.indexkeys[1]: self._cur_places(yamlinfo),
                self.indexkeys[2]: self._exp_places(yamlinfo),
                self.indexkeys[3]: self._education(yamlinfo),
                self.indexkeys[4]: self._gender(yamlinfo),
                self.indexkeys[5]: self._mar_status(yamlinfo),
            }
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
            #     'marital_status'
        """
        if uses is None:
            uses = self.index.keys()
        results = list()
        for use in uses:
            assert use in self.index
            parts = list()
            result = set()
            index = self.index[use]
            for key in filtedict:
                assert key in index
                for value in filtedict[key]:
                    if value in index[key]:
                        parts.append(index[key][value])
            if parts:
                result.update(parts[0])
                for part in parts[1:]:
                    result.intersection_update(part)
            results.extend(result)
        return results

    def filte(self, filtedict, selected, uses=None):
        """
            # need key and value
            # keys:
            #     'current_places',
            #     'expectation_places',
            #     'education',
            #     'gender',
            #     'marital_status'
        """
        return self.get(filtedict, uses) & selected

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
