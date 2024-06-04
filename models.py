from datetime import datetime, UTC
from uuid import UUID, uuid4

class Answer(object):
    def __init__(self, id:UUID = None, body: str = '', createdAt: datetime = None):
        self.id = uuid4() if not id else id
        self.body = body
        self.createdAt = datetime.now(UTC) if not createdAt else createdAt
    def __json__(self, request):
        return {
            'id': str(self.id),
            'body': self.body,
            'createdAt':  self.createdAt.strftime('%d/%m/%Y, %H:%M:%S'),
        }


class Question(object):
    def __init__(self, id: UUID = None, body: str = '', createdAt: datetime = None, answers: tuple[Answer] = {}):
        self.id = uuid4() if not id else id 
        self.body = body
        self.createdAt = datetime.now(UTC) if not createdAt else createdAt
        self.answers = answers
    def __json__(self, request):
        return {
            'id': str(self.id),
            'body': self.body,
            'createdAt': self.createdAt.strftime('%d/%m/%Y, %H:%M:%S'),
            'answers': list(map(lambda x: x.__json__(request), self.answers)),
        }
    
class SearchResults:
    def __init__(self, searchTerm: str = '', page: int = 1, pageSize:int = 24, results: list[Question] = [], totalFound: int = 0): 
        self.searchTerm = searchTerm
        self.page = page
        self.pageSize = pageSize
        self.results = results
        self.totalFound = totalFound

    def __json__(self, request):
        return {
            'searchTerm': self.searchTerm,
            'page': self.page,
            'pageSize': self.pageSize,
            'results': list(map(lambda x: x.__json__(request), self.results)),
            'totalFound': self.totalFound,
        }