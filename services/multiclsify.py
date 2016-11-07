import os

import services.classifycv
import sources.industry_id


class MultiClassify(object):

    CLASSIFY_DIR = 'classify'

    def __init__(self, cvstorage):
        self.classifies = dict()
        self.cvstorage = cvstorage
        for name in sources.industry_id.industryID.keys():
            cls_cv = services.classifycv.ClassifyCV(name, self.CLASSIFY_DIR, cvstorage)
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
        for y in self.cvstorage.yamls():
            info = self.cvstorage.getyaml(y)
            for c in info['classify']:
                if not self.classifies[c].exists(y):
                    self.classifies[c]._add(y)
        self.save()
