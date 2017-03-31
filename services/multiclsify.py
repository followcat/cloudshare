import os

import services.classifycv
import sources.industry_id


class MultiClassify(object):

    CLASSIFY_DIR = 'classify'

    def __init__(self, storage):
        self.classifies = dict()
        self.storage = storage
        for name in sources.industry_id.industryID.keys():
            cls_cv = services.classifycv.ClassifyCV(name, self.CLASSIFY_DIR, storage)
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
        for id in self.storage.ids:
            metadata = self.storage.getyaml(id)
            data = self.storage.getmd(id)
            for c in metadata['classify']:
                if not self.classifies[c].exists(id):
                    dataobj = core.basedata.DataObject(metadata, data)
                    self.classifies[c].add(dataobj)
        self.save()

    def updateids(self, ids=None):
        if ids is None:
            ids = self.storage.ids
        for id in ids:
            metadata = self.storage.getyaml(id)
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
        self.updateids(ids=self.storage.ids.difference(exists_ids))
