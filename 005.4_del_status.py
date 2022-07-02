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


def get_status():
    cursor.execute("SELECT id, status FROM status ORDER BY id")
    get = cursor.fetchall()

    for i in get:
        print(f"\"{i['id']}\" - \"{i['status']}\"")


while True:

    # Выводим статусы которые у нас есть
    get_status()

    # Проверка на то, что id статуса - целое положительное число и существует в таблице статусов
    while True:
        try:

            status_id = int(input('Ведите id статуса который хотите удалить: '))
            if status_id > 0:
                cursor.execute("SELECT id, status FROM status ORDER BY id")
                get_status_check = cursor.fetchall()
                list_ids = []
                for c in get_status_check:
                    list_ids.append(c['id'])
                if status_id <= list_ids[-1]:
                    break
                else:
                    print('По введенному id не возможно определить статус')
            else:
                print('По введенному id не возможно определить статус')
        except ValueError:
            print('По введенному id не возможно определить статус')

    # Смотрим наличие выбранного статуса в сеансах чтобы его не удалить если он есть
    try:
        cursor.execute('''
        SELECT status_id FROM 'sessions-hall'
        ''')
        get_result_hall = cursor.fetchall()
        for h_check in get_result_hall:
            if h_check['status_id'] == status_id:
                print('Невозможно удалить данный статус т.к. существует сеанс (для зала без цен) с таким статусом. Сперва удалите сеанс')
                exit()
    except sqlite3.OperationalError:
        # Нельзя удалять статус по-умолчанию
        if status_id == 1:
            print('Данное значение используется по-умолчанию. Его нельзя удалять.')
            exit()
        # Удаляем выбранный статус
        cursor.execute('''DELETE FROM status WHERE id = :status ''', {'status': status_id})
        db.commit()

    try:
        cursor.execute('''
        SELECT status_id FROM 'sessions-hall-prices'
        ''')
        get_result_hall_prices = cursor.fetchall()
        for h_check in get_result_hall_prices:
            if h_check['status_id'] == status_id:
                print('Невозможно удалить данный статус т.к. существует сеанс (для зала с ценами) с таким статусом. Сперва удалите сеанс')
                exit()
    except sqlite3.OperationalError:
        # Нельзя удалять статус по-умолчанию
        if status_id == 1:
            print('Данное значение используется по-умолчанию. Его нельзя удалять.')
            exit()
        # Удаляем выбранный статус
        cursor.execute('''DELETE FROM status WHERE id = :status ''', {'status': status_id})
        db.commit()

    cursor.execute('''
    SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'session-i-%' ORDER BY name
    ''')
    tables_i = cursor.fetchall()
    for tt in tables_i:
        table_show_id = '''
        SELECT status_id FROM {session}
        '''
        cursor.execute(table_show_id.format(session=f'\'{tt["name"]}\''))
        get_table_status_id = cursor.fetchall()
        for zz in get_table_status_id:
            if zz['status_id'] == status_id:
                print('Невозможно удалить данный статус т.к. существует сеанс (для зала без цен) с таким статусом. Сперва удалите сеанс')
                exit()

    cursor.execute('''
    SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'session-g-%' ORDER BY name
    ''')
    tables_i = cursor.fetchall()
    for tt in tables_i:
        table_status_id = '''
        SELECT status_id FROM {session}
        '''
        cursor.execute(table_status_id.format(session=f'\'{tt["name"]}\''))
        get_table_status_id = cursor.fetchall()
        for zz in get_table_status_id:
            if zz['status_id'] == status_id:
                print('Невозможно удалить данный статус т.к. существует сеанс (для зала с ценами) с таким статусом. Сперва удалите сеанс')
                exit()

    # Нельзя удалять статус по-умолчанию
    if status_id == 1:
        print('Данное значение используется по-умолчанию. Его нельзя удалять.')
        exit()
    # Удаляем выбранный статус
    cursor.execute('''DELETE FROM status WHERE id = :status ''', {'status': status_id})
    db.commit()

    test = input('Хотите еще удалить категорию из базы данных? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if test == 'n':
        # Выводим статусы
        get_status()
        db.close()
        break
