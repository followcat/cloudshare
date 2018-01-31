import os.path

import services.operator.facade
import core.mining.valuable
import core.mining.lsisimilarity

from utils.builtin import industrytopath


class Similarity(services.operator.facade.Application):
    """"""
    SIMS_PATH = 'all'

    def __init__(self, data_service, operator_service):
        super(Similarity, self).__init__(data_service, operator_service)
        self.sim = dict()
        self.path = operator_service.path

    def setup(self, modelname, simnames):
        self.modelname = modelname
        result = True
        result = self.operator_service.setup(modelname)
        if result is True:
            model = self.operator_service.lsi_model[modelname]
            if model.names:
                if modelname not in self.sim:
                    self.sim[modelname] = dict()
                for simname in simnames:
                    if simname in self.sim[modelname]:
                        continue
                    self.init_sim(modelname, simname)
        return result

    def init_sim(self, modelname, svc_name, gen=None):
        model = self.operator_service.lsi_model[modelname]
        save_path = os.path.join(self.path, modelname, self.SIMS_PATH)
        industrypath = industrytopath(svc_name)
        index = core.mining.lsisimilarity.LSIsimilarity(svc_name,
                                                        os.path.join(save_path,
                                                        industrypath), model)
        try:
            index.load()
        except IOError:
            if gen is None:
                gen = list()
            index.build(gen)
            index.save()
        self.sim[modelname][svc_name] = index

    def add(self, cvobj, *args, **kwargs):
        simname = kwargs['simname']
        result = super(Similarity, self).add(cvobj, *args, **kwargs)
        if result:
            self.add_documents(simname, [cvobj.ID], [cvobj.data])
        return result

    def add_documents(self, simname, names, documents):
        self.sim[self.modelname][simname].add_documents(names, documents)
        self.sim[self.modelname][simname].save()

    def getsims(self, basemodel, uses=None):
        sims = []
        if uses is None:
            try:
                uses = self.sim[basemodel].keys()
            except KeyError:
                return sims
        for each in uses:
            try:
                sim = self.sim[basemodel][each]
            except KeyError:
                continue
            sims.append(sim)
        return sims

    def probability(self, doc, uses=None, top=None, minimum=None, **kwargs):
        result = []
        try:
            basemodel = kwargs['basemodel']
        except KeyError:
            basemodel = self.modelname
        sims = self.getsims(basemodel, uses=uses)
        for sim in sims:
            result.extend(sim.probability(doc, top=top, minimum=minimum))
        results_set = set(result)
        return sorted(results_set, key=lambda x:float(x[1]), reverse=True)

    def probability_by_id(self, doc, id, uses=None, **kwargs):
        result = tuple()
        try:
            basemodel = kwargs['basemodel']
        except KeyError:
            basemodel = self.modelname
        sims = self.getsims(basemodel, uses=uses)
        for sim in sims:
            probability = sim.probability_by_id(doc, id)
            if probability is not None:
                result = probability
                break
        return result

    def probability_by_ids(self, doc, ids, uses=None, top=10000, **kwargs):
        result = []
        try:
            basemodel = kwargs['basemodel']
        except KeyError:
            basemodel = self.modelname
        sims = self.getsims(basemodel, uses=uses)
        for sim in sims:
            result.extend(sim.probability_by_ids(doc, ids, top=top))
        return sorted(result, key=lambda x: x[1], reverse=True)

    def valuable_rate(self, name_list, member, doc, top, **kwargs):
        try:
            basemodel = kwargs['basemodel']
        except KeyError:
            basemodel = self.modelname
        return core.mining.valuable.rate(name_list, self, basemodel, member, doc, top)

    def idsims(self, modelname, ids):
        results = list()
        for id in ids:
            for sim in self.sim[modelname].values():
                if id in sim.names:
                    results.append(sim.name)
                    break
        return results

    def minelist(self, doc, ids, basemodel, uses=None):
        return self.probability_by_ids(doc, ids, uses=uses, basemodel=basemodel)

    def minelistrank(self, doc, lists, basemodel, uses=None, top=None, minimum=None):
        if uses is None:
            uses = list()
            for name, value in lists:
                for sim in self.sim[basemodel].values():
                    if sim.exists(name):
                        uses.append(sim.name)
        probalist = set(self.probability(doc, uses=uses, basemodel=basemodel, 
                                         top=top, minimum=minimum))
        probalist.update(set(lists))
        ranklist = sorted(probalist, key=lambda x:float(x[1]), reverse=True)
        return len(ranklist), map(lambda x: (x[0], ranklist.index(x)), lists)

