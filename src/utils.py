import psycopg2
import requests

def get_vacancy_company(company_name: str) -> None:
    """Получение данных о вакансиях"""

    url = f"https://api.hh.ru/vacancies?employer={company_name}"
    response_v = requests.get(url)
    if response_v.status_code == 200:
        vacancies = response_v.json()
        return vacancies
    else:
        print('Ошибка при получении данных')


def create_database(db_name: str, params: dict) -> None:
    """Создание БД"""

    # подключение к БД
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    # удаление существующей и создание новой БД
    cur.execute(f"DROP DATABASE {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")
    # завершение сеанса подключения
    cur.close()
    conn.close()


def create_tables(db_name: str, params: dict) -> None:
    """Создание таблицы в БД"""

    # подключение к БД
    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        # создание таблицы
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                employer_url TEXT
            )
        """)

    with conn.cursor() as cur:
        # создание таблицы
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                name VARCHAR(255) NOT NULL,
                salary_min INT,
                salary_max INT,
                vacancy_url TEXT
            )
        """)
    # завершение сеанса подключения
    conn.commit()
    conn.close()


def insert_data(vacancies: list[dict], db_name: str, params: dict) -> None:
    """Заполнение данных таблицы"""

    # подключение к БД
    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        for vacancy in vacancies['items']:
            # проверка существования записи
            cur.execute(
                """
                SELECT employer_id FROM employers WHERE name = %s
                """,
                (vacancy['employer']['name'],)
            )
            employer_id = cur.fetchone()

            if employer_id:
                # Если employer нет в таблице, генерируем новый id
                employer_id = employer_id[0]
            else:
                # Если employer есть в таблице, используем существующий id
                cur.execute(
                    """
                    INSERT INTO employers (name, employer_url)
                    VALUES (%s, %s)
                    RETURNING employer_id
                    """,
                    (vacancy['employer']['name'], vacancy['employer']['alternate_url'])
                )
                employer_id = cur.fetchone()[0]

            # добавляем данные в таблицу vacancies
            cur.execute(
                """
                INSERT INTO vacancies (employer_id, name, salary_min, salary_max, vacancy_url)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (employer_id, vacancy['name'], vacancy['salary']['from'] if vacancy['salary'] else None,
                 vacancy['salary']['to'] if vacancy['salary'] else None, vacancy['alternate_url'])
            )

        # завершение сеанса подключения
        conn.commit()
        conn.close()