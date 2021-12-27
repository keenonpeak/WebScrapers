from ..engine import SearchEngine
from ..config import PROXY, TIMEOUT, FAKE_USER_AGENT
from ..utils import unquote_url


class Google(SearchEngine):
    '''Searches google.com'''
    def __init__(self, proxy=PROXY, timeout=TIMEOUT):
        super(Google, self).__init__(proxy, timeout)
        self._base_url = 'https://www.google.com/search?q=clickshare&rlz=1C1CHZN_zh-TWKR917KR917&sxsrf=AOaemvKY51v4LjBtqEXVz0PRkqvsjhpPMw:1630917705042&source=lnt&tbs=qdr:d&sa=X&ved=2ahUKEwjLut3z-enyAhWNOZQKHeCcBc0QpwV6BAgBECI&biw=1920&bih=969'
        self._delay = (2,10)
        self._current_page = 1
        self.set_headers({'User-Agent':FAKE_USER_AGENT})
    
    def _selectors(self, element):
        '''Returns the appropriate CSS selector.'''
        selectors = {
            'url': 'a[href]', 
            'title': 'a', 
            'text': 'div>span:nth-child(2)', 
            'links': 'div#search div[class=g]', 
            'next': 'a[href][aria-label="Page {page}"]'
        }
        return selectors[element]
    
    def _first_page(self):
        '''Returns the initial page and query.'''
        url = u'{}/search?q={}'.format(self._base_url, self._query)
        return {'url':url, 'data':None}

    def _next_page(self, tags):
        '''Returns the next page URL and post data (if any)'''
        self._current_page += 1
        selector = self._selectors('next').format(page=self._current_page)
        next_page = self._get_tag_item(tags.select_one(selector), 'href')
        url = None
        if next_page:
            url = self._base_url + next_page
        return {'url':url, 'data':None}

    def _get_url(self, tag, item='href'):
        '''Returns the URL of search results item.'''
        selector = self._selectors('url')
        url = self._get_tag_item(tag.select_one(selector), item)

        if url.startswith(u'/url?q='):
            url = url.replace(u'/url?q=', u'').split(u'&sa=')[0]
        return unquote_url(url)

    def _get_text(self, tag, item='text'):
        '''Returns the text of search results items.'''
        selector = self._selectors('text')
        tag = tag.select(selector) or [None]
        return self._get_tag_item(tag[-1], item)

    def _get_time(self, tag, item='text'):
        '''Returns the time of search results items.'''
        selector = self._selectors('time')
        tag = tag.select(selector) or [None]
        return self._get_tag_item(tag[-1], item)
