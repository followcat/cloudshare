import services.operator.multiple


class MultiPeople(services.operator.multiple.Multiple):
    """"""
    combine_all = ('names', 'yamls', 'getmd', 'getinfo')
    match_any = ('search', 'exists', 'getmd_en', 'gethtml', 'getyaml', 'getuniqueid', 'private_keys', 'add')

    def getyaml(self, id):
        result = None
        for people in self.services:
            try:
                info = people.getyaml(id)
            except IOError:
                continue
            if result is None:
                result = info
            else:
                for cv in info['cv']:
                    result['cv'].append(cv)
        return result
