from config import config
from src.utils import get_vacancy_company, create_database, create_tables, insert_data
from src.dbmanager import DBManager

def main():
    # топ-10 IT компаний
    companies = ['Ланит', 'Тензор', 'VK', 'Альфа-банк', 'Aston (ex. Andersen)',
                 'АО «ГНИВЦ» ', 'Европлан', 'CarPrice', 'Solit Clouds', 'Usetech']
    # параметры для подключения к БД
    params = config()

    # создаем БД
    create_database(db_name='hh', params=params)
    # создаем таблицы employers и vacancies
    create_tables(db_name='hh', params=params)

    for company in companies:
        # через API получаем информацию о вакансиях переданной компании
        vacancies = get_vacancy_company(company)
        # заполняем таблицы employers и vacancies
        insert_data(vacancies, db_name='hh', params=params)

    # экземпляр класса DBManager
    db_manager = DBManager(db_name='hh', params=params)

    # вывод списка всех компаний и количества вакансий у компании
    print('Список всех компаний и количества вакансий у компании:')
    print(db_manager.get_companies_and_vacancies_count())
    print('_______________________________________________')

    # список всех вакансий
    print('Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию:')
    print(db_manager.get_all_vacancies())
    print('_______________________________________________')

    # средняя зарплата по вакансиям
    print('Средняя зарплата по вакансиям:')
    print(db_manager.get_avg_salary())
    print('_______________________________________________')

    # список вакансий с ЗП выше средней
    print('Список вакансий с зарплатой выше средней:')
    print(db_manager.get_vacancies_with_higher_salary())
    print('_______________________________________________')

    # список вакансий с ключевым словом
    key_word = input('Введите ключевое слово для поиска: ')
    print('Список вакансий по ключевому слову:')
    print(db_manager.get_vacancies_with_keyword(key_word))
    print('_______________________________________________')


if __name__ == '__main__':
    main()