from pyramid.view import view_config
from search_provider import SearchProvider
from models import populateTestData

class SearchController:
    def __init__(self, provider: SearchProvider):
        self.provider = provider
    @view_config(renderer='json')
    def HandleSearch(self, request):
        return self.provider.search()