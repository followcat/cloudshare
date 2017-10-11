import os

import services.classifycv
import sources.industry_id


class MultiClassify(object):

    def __init__(self, path, storages):
        self.path = path
        self.classifies = dict()
        self.storages = storages
        for name in sources.industry_id.industryID.keys():
            cls_cv = services.classifycv.ClassifyCV(name, self.path, storages)
            cls_cv.setup()
            self.classifies[name] = cls_cv

    def setup(self):
        updates = list()
        for classify in self.classifies.values():
            classify.setup(update=False)
        self.update()

    def save(self):
        for classify in self.classifies.values():
            classify.save()

    def update(self):
        for storage in self.storages:
            for id in storage.ids:
                metadata = storage.getyaml(id)
                data = storage.getmd(id)
                for c in metadata['classify']:
                    if not self.classifies[c].exists(id):
                        dataobj = core.basedata.DataObject(metadata, data)
                        self.classifies[c].add(dataobj)
        self.save()

    def updateids(self, ids=None):
        if ids is None:
            ids = set()
            for storage in self.storages:
                ids.update(storage.ids)
        for id in ids:
            for storage in self.storages:
                try:
                    metadata = storage.getyaml(id)
                except IOError:
                    continue
                for c in metadata['classify']:
                    if not self.classifies[c].exists(id):
                        self.classifies[c]._add(id)
        for c in self.classifies:
            self.classifies[c].curriculumvitae.saveids()
        self.save()

    def updatenewids(self):
        exists_ids = set()
        for c in self.classifies:
            exists_ids.update(self.classifies[c].curriculumvitae.ids)
        for storage in self.storages:
            self.updateids(ids=set(storage.ids).difference(exists_ids))
