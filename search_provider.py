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
                    WHERE LOWER(body)like LOWER(%s) AND deleted = false
                    OFFSET (%s-1) * %s
                    LIMIT %s;''', (f'%{searchTerm}%', page, pageSize, pageSize))
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

                return SearchResults(searchTerm, page, pageSize, questions)             
    def fetchAnswers(self, questionId: UUID) -> tuple[Answer]:
         with psycopg2.connect(self.connectionString) as conn:
            with conn.cursor() as cursor:
                id = str(questionId)
                cursor.execute(f"SELECT id, body, created_at FROM answer WHERE question_id = '{id}' AND deleted = false;")
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
