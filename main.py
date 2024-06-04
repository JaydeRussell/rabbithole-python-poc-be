from waitress import serve
from pyramid.config import Configurator
from wsgicors import CORS
from yoyo import read_migrations, get_backend
from constants import DB_CONNECTION_STRING, MIGRATION_PATH
from search_controller import SearchController
from search_provider import SearchProvider

def runMigrations():
   backend = get_backend(DB_CONNECTION_STRING)
   migrations = read_migrations(MIGRATION_PATH)

   with backend.lock():
    # Apply any outstanding migrations
    backend.apply_migrations(backend.to_apply(migrations))

def main():
      runMigrations()
      searchProvider = SearchProvider(DB_CONNECTION_STRING)
      searchController = SearchController(searchProvider)
      with Configurator() as config:
        config.add_route('search', '/search')
        config.add_view(searchController.HandleSearch, route_name='search', renderer='json')
        app = CORS(config.make_wsgi_app(), origin='*', headers='*', methods='*')
        serve(app, host='0.0.0.0', port=9001)

if __name__ == '__main__':
   main()