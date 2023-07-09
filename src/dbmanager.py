import psycopg2

class DBManager:
    """Класс для работы с БД Postgres"""

    def __init__(self, db_name: str, params: dict) -> None:
        """Инициализация класса"""

        # подключение к БД
        self.conn = psycopg2.connect(dbname=db_name, **params)


    def get_companies_and_vacancies_count(self) -> list:
        """Получает список всех компаний и количество вакансий у каждой компании"""

        with self.conn.cursor() as cur:
            # запрос для получения необходимой информации
            cur.execute("""
                SELECT e.name, COUNT(*) FROM employers as e
                JOIN vacancies USING(employer_id)
                GROUP BY e.name;
            """)

            # список компаний
            companies = cur.fetchall()

        return companies


    def get_all_vacancies(self) -> list:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""

        with self.conn.cursor() as cur:
            # запрос для получения необходимой информации
            cur.execute("""
                SELECT e.name, v.name, v.salary_min, v.vacancy_url 
                FROM vacancies as v
                LEFT JOIN employers as e USING(employer_id)
            """)

            # список вакансий
            vacancies = cur.fetchall()

        return vacancies


    def get_avg_salary(self) -> list:
        """Получает среднюю зарплату по вакансиям"""

        with self.conn.cursor() as cur:
            # запрос для получения необходимой информации
            cur.execute("SELECT AVG((salary_max+salary_min)/2) FROM vacancies")

            # среднее значение ЗП
            salary_avg = cur.fetchone()[0]
        return salary_avg


    def get_vacancies_with_higher_salary(self) -> list:
        """Получает список вакансий с ЗП выше средней"""

        with self.conn.cursor() as cur:
            # запрос для получения необходимой информации
            cur.execute("""
                SELECT * FROM vacancies
                WHERE (salary_max+salary_min)/2 > (SELECT AVG((salary_max+salary_min)/2) FROM vacancies)
            """)

            # список вакансий
            vacancies = cur.fetchall()

        return vacancies


    def get_vacancies_with_keyword(self, key_word: str) -> list:
        """Получает список всех вакансий по ключевому слову"""

        with self.conn.cursor() as cur:
            # запрос для получения необходимой информации
            cur.execute(f"""
                SELECT * FROM vacancies
                WHERE name LIKE '%{key_word}%'
            """)

            # список вакансий
            vacancies = cur.fetchall()

        return vacancies