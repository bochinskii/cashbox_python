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


def get_price():
    cursor.execute("SELECT id, price FROM prices ORDER BY price")
    get = cursor.fetchall()

    for i in get:
        print(f"\"{i['price']}\"")


while True:
    # Выводим цену
    get_price()

    # Проверка на то, что цена - целое положительное число и существует в таблице цен
    while True:
        price = input('Ведите цену которую хотите удалить: ')
        if price:
            try:
                # Находим id цены по значению
                cursor.execute('''SELECT id FROM prices WHERE price = :price''', {'price': price})
                get_price_id = cursor.fetchall()
                price_id = int(get_price_id[0]['id'])
                break
            except IndexError:
                print('Вы ввели не существующую цену.')
        else:
            print('Вы не ввели цену')

    # Смотрим наличие выбранной цены в сеансах чтобы его не удалить если он есть
    try:
        cursor.execute('''
        SELECT price_id FROM 'sessions-hall'
        ''')
        get_result_hall = cursor.fetchall()
        for h_check in get_result_hall:
            if h_check['price_id'] == price_id:
                print('Невозможно удалить данную цену т.к. существует сеанс (для зала без цен) с такой ценой. Сперва удалите сеанс')
                exit()
    except sqlite3.OperationalError:
        # Нельзя удалять цену по-умолчанию
        if price_id == 1:
            print('Данное значение используется по-умолчанию. Его нельзя удалять.')
            exit()
        # Удаляем цену
        cursor.execute('''DELETE FROM prices WHERE id = :price ''', {'price': price_id})
        db.commit()

    cursor.execute('''
    SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'session-i-%' ORDER BY name
    ''')
    tables_i = cursor.fetchall()
    for tt in tables_i:
        table_price_id = '''
        SELECT price_id FROM {session}
        '''
        cursor.execute(table_price_id.format(session=f'\'{tt["name"]}\''))
        get_table_price_id = cursor.fetchall()
        for zz in get_table_price_id:
            if zz['price_id'] == price_id:
                print('Невозможно удалить данную цену т.к. существует сеанс (для зала без цен) с такой ценой. Сперва удалите сеанс')
                exit()

    # Нельзя удалять цену по-умолчанию
    if price_id == 1:
        print('Данное значение используется по-умолчанию. Его нельзя удалять.')
        exit()
    # Удаляем цену
    cursor.execute('''DELETE FROM prices WHERE id = :price ''', {'price': price_id})
    db.commit()

    test = input('Хотите еще удалить цену из базы данных? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if test == 'n':
        # Выводим цены
        get_price()
        db.close()
        break
