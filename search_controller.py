from pyramid.view import view_config
from search_provider import SearchProvider

class SearchController:
    def __init__(self, provider: SearchProvider):
        self.provider = provider
    @view_config(renderer='json')
    def HandleSearch(self, request):
        return self.provider.search(
            searchTerm=request.GET['search-term'],
            page=int(request.GET['page']),
            pageSize=(int(request.GET['page-size'])),
        )