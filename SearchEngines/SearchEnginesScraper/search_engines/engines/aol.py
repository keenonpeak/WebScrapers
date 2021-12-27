from .yahoo import Yahoo
from ..config import PROXY, TIMEOUT


class Aol(Yahoo):
    '''Seaches aol.com'''
    def __init__(self, proxy=PROXY, timeout=TIMEOUT):
        super(Aol, self).__init__(proxy, timeout)
        self._base_url = u'https://search.aol.com/aol/search;_ylt=Awr9Dtw71DVh5HQAZgZpCWVH;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA2ZpbHRlcg--?q=clickshare&ei=UTF-8&age=1d&v_t=comsearch&s_chn=prt_bon&fr2=time&btf=d'

    def _first_page(self):
        '''Returns the initial page and query.'''
        url_str = u'{}/aol/search?q={}&ei=UTF-8&nojs=1'
        url = url_str.format(self._base_url, self._query)
        self._http_client.get(self._base_url)
        return {'url':url, 'data':None}

