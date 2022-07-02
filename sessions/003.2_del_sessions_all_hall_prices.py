import sqlite3

# Define path to DB Location
DB_PATH = 'E:\\TEMP_WORK\\chashbox\\cashbox_db.sqlite'


def dict_factory(cur, row):
    d = {}
    for idx, col in enumerate(cur.description):
        d[col[0]] = row[idx]
    return d


db = sqlite3.connect(DB_PATH)
db.row_factory = dict_factory
cursor = db.cursor()

while True:
    try:
        # Смотрим сеансы, которые у нас есть
        cursor.execute('''
        SELECT date, shows.name, categories.category, hall_prices."row", hall_prices.seat, hall_prices.price, \
        status.status FROM 'sessions-hall-prices'
        INNER JOIN shows ON shows_id = shows.id
        INNER JOIN hall_prices ON hall_id = hall_prices.id
        INNER JOIN status ON status_id = status.id
        INNER JOIN categories ON shows.category_id = categories.id ORDER BY date''')
        get_result_hall_prices = cursor.fetchall()

        print('Сеансы: ')
        for r_hall_prices in get_result_hall_prices:
            if r_hall_prices['row'] == 1 and r_hall_prices['seat'] == 1:
                print(f"{r_hall_prices['date']} - \"{r_hall_prices['name']}\" ({r_hall_prices['category']})")
    except sqlite3.OperationalError:
        print('Таблицы с сеансами не существует')
        exit()

    # Вводим дату проведения сеанса
    date = input('Введите дату проведения сеанса (YYYY-MM-DD hh:mm): ')

    # Проверяем существует ли сеанс по дате
    cursor.execute('''
        SELECT 'sessions-hall-prices'.date, shows.name, 'sessions-hall-prices'.shows_id, categories.category, \
        hall_prices."row", hall_prices.seat, hall_prices.price, status.status FROM 'sessions-hall-prices'
        INNER JOIN shows ON 'sessions-hall-prices'.shows_id = shows.id
        INNER JOIN hall_prices ON 'sessions-hall-prices'.hall_id = hall_prices.id
        INNER JOIN status ON 'sessions-hall-prices'.status_id = status.id
        INNER JOIN categories ON shows.category_id = categories.id
        WHERE 'sessions-hall-prices'.date = :date''', {"date": date})
    get_test = cursor.fetchall()
    if not get_test:
        print('Вы ввели данные не существующего сеанса либо данные не для группового сеанса. Попробуте еще раз')
        exit()
    for i in get_test:
        print(
            f"\"{i['date']}\" - \"{i['name']} (id - {i['shows_id']})\" - \"{i['category']}\" \
    - \"{i['row']}\"/\"{i['seat']}\" - \"{i['price']}\" - \"{i['status']}\"")

    # Удаляем сеанс
    test_del = input('Вы уверены что хотите удалить данный сеанс? \
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если "нет": ')
    if test_del != 'n':
        # удаляем данные талицы
        cursor.execute("DELETE FROM 'sessions-hall-prices' WHERE date = :date", {'date': date})
        db.commit()

    test = input('Хотите еще удалить сеансы из базы базы данных? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')

    if test == 'n':
        db.close()
        exit()