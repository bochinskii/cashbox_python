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


def get_shows():
    cursor.execute('''
        SELECT shows.id, shows.name, categories.category FROM shows
        INNER JOIN categories ON shows.category_id = categories.id ORDER BY categories.id
        ''')
    get = cursor.fetchall()

    for i in get:
        print(f"\"{i['id']}\" - \"{i['name']}\" - \"{i['category']}\"")


while True:

    print('Шоу в наличии:')
    # Смотрим шоу, которые у нас есть
    get_shows()

    # Проверка на то, что id шоу - целое положительное число и существует в таблице категорий
    while True:
        try:
            # Выбираем шоу по id
            show_id = int(input('Введите id шоу, которое хотите удалить: '))
            if show_id > 0:
                cursor.execute("SELECT id, name FROM shows ORDER BY id")
                get_shows_check = cursor.fetchall()
                list_ids = []
                for c in get_shows_check:
                    list_ids.append(c['id'])
                if show_id <= list_ids[-1]:
                    break
                else:
                    print('По введенному id не возможно определить шоу')
            else:
                print('По введенному id не возможно определить шоу')
        except ValueError:
            print('По введенному id не возможно определить шоу')
        except IndexError:
            print('Таблица с шоу пуста')
            exit()

    # Смотрим наличие выбранного шоу в сеансах чтобы его не удалить если оно есть
    try:
        cursor.execute('''
        SELECT shows_id FROM 'sessions-hall'
        ''')
        get_result_hall = cursor.fetchall()
        for h_check in get_result_hall:
            if h_check['shows_id'] == show_id:
                print('Невозможно удалить данное шоу т.к. существует сеанс (для зала без цен) с таким шоу. Сперва удалите сеанс')
                exit()
    except sqlite3.OperationalError:
        cursor.execute('''DELETE FROM shows WHERE id = :show ''', {'show': show_id})
        db.commit()

    try:
        cursor.execute('''
        SELECT shows_id FROM 'sessions-hall-prices'
        ''')
        get_result_hall_prices = cursor.fetchall()
        for h_check in get_result_hall_prices:
            if h_check['shows_id'] == show_id:
                print('Невозможно удалить данное шоу т.к. существует сеанс (для зала с ценами) с таким шоу. Сперва удалите сеанс')
                exit()
    except sqlite3.OperationalError:
        cursor.execute('''DELETE FROM shows WHERE id = :show ''', {'show': show_id})
        db.commit()

    cursor.execute('''
    SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'session-i-%' ORDER BY name
    ''')
    tables_i = cursor.fetchall()
    for tt in tables_i:
        table_show_id = '''
        SELECT shows_id FROM {session}
        '''
        cursor.execute(table_show_id.format(session=f'\'{tt["name"]}\''))
        get_table_show_id = cursor.fetchall()
        for zz in get_table_show_id:
            if zz['shows_id'] == show_id:
                print('Невозможно удалить данное шоу т.к. существует сеанс (для зала без цен) с таким шоу. Сперва удалите сеанс')
                exit()

    cursor.execute('''
    SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'session-g-%' ORDER BY name
    ''')
    tables_i = cursor.fetchall()
    for tt in tables_i:
        table_show_id = '''
            SELECT shows_id FROM {session}
            '''
        cursor.execute(table_show_id.format(session=f'\'{tt["name"]}\''))
        get_table_show_id = cursor.fetchall()
        for zz in get_table_show_id:
            if zz['shows_id'] == show_id:
                print('Невозможно удалить данное шоу т.к. существует сеанс (для зала с ценами) с таким шоу. Сперва удалите сеанс')
                exit()

    # Удаляем выбранные шоу
    cursor.execute('''DELETE FROM shows WHERE id = :show ''', {'show': show_id})
    db.commit()

    test = input('Хотите еще удалить шоу из базы данных? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if test == 'n':
        # Выводим наличие шоу
        get_shows()
        db.close()
        break

