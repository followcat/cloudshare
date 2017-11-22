import services.operator.multiple


class MultiPeople(services.operator.multiple.Multiple):
    """"""
    combine_all = ('getmd', 'getinfo')
    match_any = ('exists', 'getmd_en', 'gethtml', 'getyaml', 'getuniqueid')

    def getyaml(self, id):
        result = None
        for people in self.services:
            if not people.exists(id):
                continue
            info = people.getyaml(id)
            if result is None:
                result = info
            else:
                for cv in info['cv']:
                    result['cv'].append(cv)
        return result
