import psycopg2
from models import SearchResults, Question, Answer
from uuid import UUID

class SearchProvider:
    def __init__(self, databaseConnectionString: str):
        self.connectionString = databaseConnectionString
    def search(self, searchTerm:str = "", page: int = 1, pageSize: int = 24) -> SearchResults:
        if page < 1:
            page = 1
        if pageSize < 1:
            pageSize = 24

        with psycopg2.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT id, body, created_at FROM question
                    WHERE LOWER(body)like LOWER(%s) AND deleted = %s
                    OFFSET (%s-1) * %s
                    LIMIT %s;''', (f'%{searchTerm}%', False, page, pageSize, pageSize))
                results = cursor.fetchall()

                questions = list[Question]()
                for row in results:
                    questionId = UUID(row[0])
                    questions.append(Question(
                        id = questionId,
                        body = row[1],
                        createdAt = row[2],
                        answers = self.fetchAnswers(questionId),
                    ))

        return SearchResults(
            searchTerm=searchTerm, 
            page=page, 
            pageSize=pageSize, 
            results=questions, 
            totalFound=self.fetchTotalCount(searchTerm),
        ) 
    def fetchTotalCount(self, searchTerm: str) -> int:
        with psycopg2.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT count(*) FROM question
                    WHERE LOWER(body)like LOWER(%s) AND deleted = %s;''', 
                    (f'%{searchTerm}%', False))
                return cursor.fetchall()[0][0]
    def fetchAnswers(self, questionId: UUID) -> tuple[Answer]:
         with psycopg2.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                id = str(questionId)
                cursor.execute('SELECT id, body, created_at FROM answer WHERE question_id = %s AND deleted = %s;', (id, False))
                results = cursor.fetchall()

                answers = list[Question]()
                for row in results:
                    answerId = UUID(row[0])
                    answers.append(Answer(
                        id=answerId,
                        body=row[1],
                        createdAt=row[2],
                    ))
                
                return tuple(answers)
