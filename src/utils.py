import psycopg2
import requests
def get_company_hh(key_word: str) -> list[dict]:
    url = f"https://api.hh.ru/employers?text={key_word}"
    response = requests.get(url)
    if response.status_code == 200:
        employers = response.json()
        return employers
    else:
        print('Ошибка при получении данных')


def get_vacancy_company(id):
    """Получение данных о вакансиях"""
    # url = f"https://api.hh.ru/employers/{id}"
    url = f"https://api.hh.ru/vacancies?employer_id={id}"
    response_v = requests.get(url)
    if response_v.status_code == 200:
        vacancy = response_v.json()
        return vacancy
    else:
        print('Ошибка при получении данных')

def create_database(db_name: str, params: dict) -> None:
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()


def create_tables(db_name: str, params: dict):
    """Создание таблицы в БД"""
    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employeers (
                employee_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                employeer_url TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employee_id INT REFERENCES employeers(employee_id),
                name VARCHAR(255) NOT NULL,
                salary INT,
                city VARCHAR(100),
                vacancy_url TEXT
            )
        """)

    conn.commit()
    conn.close()


def insert_data():
    """Заполнение данных таблицы"""
    pass

