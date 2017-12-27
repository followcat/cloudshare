import time

import services.base.kv_storage


class ListFrameStorage(services.base.kv_storage.KeyValueStorage):
    """"""
    list_frame = {
        'author':   str,
        'content':  str,
        'date':     str,
        }

    def build_frame(self, **kwargs):
        """
            >>> import services.base.frame_storage
            >>> lf = services.base.frame_storage.ListFrameStorage('datas', 'lfs')
            >>> lf.build_frame(author='VCR', content='comment')
            {'content': 'comment', 'date': '2017-12-26 18:42:14', 'author': 'VCR'}
        """
        info = {}
        for each in self.list_frame.items():
            if each[0] in kwargs:
                info[each[0]] = kwargs[each[0]]
            else:
                info[each[0]] = each[1]()
        if not info['date']:
            info['date'] = time.strftime('%Y-%m-%d %H:%M:%S')
        return info

