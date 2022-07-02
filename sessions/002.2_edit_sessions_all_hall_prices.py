import sqlite3
import re

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


# Выводим возможные статусы
def get_status():
    cursor.execute("SELECT id, status FROM status ")
    get_status = cursor.fetchall()
    for i in get_status:
        print(f"\"{i['id']}\" - \"{i['status']}\"")


# Выводим все доступные шоу
def get_shows():
    cursor.execute('''
    SELECT shows.id, shows.name, categories.category FROM shows
    INNER JOIN categories ON shows.category_id = categories.id
    ''')
    get_shows = cursor.fetchall()
    for i in get_shows:
        print(f"\"{i['id']}\" - \"{i['name']}\" - \"{i['category']}\"")

# Проверка существования таблицы с шоу - "shows".
try:
    cursor.execute("SELECT id, name FROM shows")
    get_shows_check = cursor.fetchall()
except sqlite3.OperationalError:
    print('Не возможно создать сеанс т.к. нет ни одного шоу. Создайте сперва таблицу с шоу.')
    exit()

# Проверка существования зала без цен - "hall".
try:
    cursor.execute("SELECT id, row, seat FROM hall")
    get_hall_check = cursor.fetchall()
except sqlite3.OperationalError:
    print('Не возможно создать сеанс т.к. не создан зал без цен. Создайте сперва таблицу с залом.')
    exit()

# Проверка существования зала с ценами - "hall_prices".
try:
    cursor.execute("SELECT id, row, seat, price FROM hall_prices")
    get_hall_prices_check = cursor.fetchall()
except sqlite3.OperationalError:
    print('Не возможно создать сеанс т.к. не создан зал с ценами. Создайте сперва таблицу с залом.')
    exit()

# Проверка существования таблицы со статусами - "status".
try:
    cursor.execute("SELECT id, status FROM status")
    get_status_check = cursor.fetchall()
except sqlite3.OperationalError:
    print('Не возможно создать сеанс т.к. нет ни одного статуса. Создайте сперва таблицу со стасусами.')
    exit()

while True:
    try:
        # Смотрим сеансы, которые у нас есть
        cursor.execute('''
        SELECT date, shows.name, categories.category, hall."row", hall.seat, status.status, prices.price FROM 'sessions-hall'
        INNER JOIN shows ON shows_id = shows.id
        INNER JOIN hall ON hall_id = hall.id
        INNER JOIN status ON status_id = status.id
        INNER JOIN categories ON shows.category_id = categories.id
        INNER JOIN prices ON price_id = prices.id ORDER BY date''')
        get_result_hall = cursor.fetchall()
        print('Сеансы для групп: ')
        for r_hall in get_result_hall:
            if r_hall['row'] == 1 and r_hall['seat'] == 1:
                print(f"{r_hall['date']} - \"{r_hall['name']}\" ({r_hall['category']})")
    except sqlite3.OperationalError:
        print('Таблицы с сеансами не существует')
        exit()
    try:
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

    # Проверка формата ввода даты
    if not date:
        print('Вы не ввели дату проведения сеанса. Попробуйте еще раз')
        exit()

    # Проверка формата ввода даты
    pattern = r"^(20[0-9][0-9])-(0[1-9]|1[1-2])-(0[0-9]|1[0-9]|2[0-9]|3[0-1])\s([0-1][0-9]|2[0-3]):([0-5][0-9])$"
    if not re.findall(pattern, date):
        print('Не правильный формат даты. Введите дату в формате - "YYYY-MM-DD hh:mm"')
        exit()

    # Выводим выбранный сеанс по введенной дате
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

    try:
        # Выбор того, что хотим отредактировать
        choice = int(input('Что вы хотите изменить:\n\
"1" - статус места;\n\
"2" - статус для последовательности мест.\n\
"3" - шоу запланированное на данную дату;\n\
"4" - дату проведения сеанса;\n\
Введите нужное значение: '))
    except ValueError:
        print('Вы ввели не существующее значение')
        exit()

    # Изменяем статус места
    if choice == 1:
        while True:
            while True:
                try:
                    # Преобразуем ряд и место в id
                    hall_id_row = int(input('Введите номер ряда: '))
                    hall_id_seat = int(input('Введите номер места: '))
                    cursor.execute('''SELECT id FROM hall_prices WHERE "row" = :row AND seat = :seat''',
                                   {'row': hall_id_row, 'seat': hall_id_seat})
                    get_hall_id = cursor.fetchall()
                    hall_id = get_hall_id[0]['id']
                    break
                except IndexError:
                    print('Данного ряда или места не существует. Попробуйте еще раз')
                except ValueError:
                    print('Данного ряда или места не существует. Попробуйте еще раз')

            # Выводим возможные статусы
            get_status()

            # Проверка на то, что id статуса - целое положительное число и существует в таблице статусов
            while True:
                try:
                    # Устанавливаем значение status по-умолчанию
                    status_id = int(
                        input('Введите id возможного статуса, на который хотите поменять выбранные ряд и место: '))
                    if status_id > 0:
                        cursor.execute("SELECT id, status FROM status ORDER BY id")
                        get_status_check = cursor.fetchall()
                        list_ids = []
                        for c in get_status_check:
                            list_ids.append(c['id'])
                        if status_id <= list_ids[-1]:
                            break
                        else:
                            print('По введенному id не возможно назначить статус')

                    else:
                        print('По введенному id не возможно назначить статус')
                except ValueError:
                    print('По введенному id не возможно назначить статус')

            # Делаем изменения
            cursor.execute(
                "UPDATE 'sessions-hall-prices' SET status_id = :status WHERE date = :date AND hall_id = :hall",
                {'status': status_id, 'date': date, 'hall': hall_id})
            db.commit()

            test_choice_1 = input('Хотите еще изменить статус места?\n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
            if test_choice_1 == 'n':
                break

    # Изменяем статус для последовательности мест
    if choice == 2:
        while True:
            while True:
                try:
                    hall_row_id_start = int(input('Введите номер ряда, с которого будет происходить изменение статуса: '))
                    hall_seat_id_start = int(input('Введите номер места, с которого будет происходить изменение статуса: '))
                    hall_row_id_end = int(input('Введите номер ряда, по который будет происходить изменение статуса: '))
                    hall_seat_id_end = int(input('Введите номер места, по которое будет происходить изменение статуса: '))

                    # Выясняем id стартового значения
                    cursor.execute('''
                    SELECT id FROM hall WHERE "row" = :row AND seat = :seat''',
                                   {'row': hall_row_id_start, 'seat': hall_seat_id_start})
                    get_hall_id_start = cursor.fetchall()
                    hall_id_start = get_hall_id_start[0]['id']

                    # Выясняем id последнего значения
                    cursor.execute('''SELECT id FROM hall WHERE "row" = :row AND seat = :seat''',
                                   {'row': hall_row_id_end, 'seat': hall_seat_id_end})
                    get_hall_id_end = cursor.fetchall()
                    hall_id_end = get_hall_id_end[0]['id']
                    break
                except IndexError:
                    print('Данного ряда или места не существует. Попробуйте еще раз')
                except ValueError:
                    print('Данного ряда или места не существует. Попробуйте еще раз')

            # Выводим все возможные статусы
            get_status()
            # Проверка на то, что id статуса - целое положительное число и существует в таблице статусов
            while True:
                try:
                    # Устанавливаем значение status по-умолчанию
                    status_id_many = int(input('Введите id возможного статуса, на который хотите поменять выбранные ряд и место: '))
                    if status_id_many > 0:
                        cursor.execute("SELECT id, status FROM status ORDER BY id")
                        get_status_check = cursor.fetchall()
                        list_ids = []
                        for c in get_status_check:
                            list_ids.append(c['id'])
                        if status_id_many <= list_ids[-1]:
                            break
                        else:
                            print('По введенному id не возможно назначить статус')

                    else:
                        print('По введенному id не возможно назначить статус')
                except ValueError:
                    print('По введенному id не возможно назначить статус')

            # Заполняем статус выбранных мест

            s = hall_id_start
            while s <= hall_id_end:
                status_many = '''
                UPDATE {session} SET status_id = :status_id WHERE hall_id = :hall_id AND date = :date
                '''
                cursor.execute(status_many.format(session=f'\'sessions-hall-prices\''),
                               {'date': date, 'status_id': status_id_many, 'hall_id': s})
                db.commit()
                s += 1

            test_choice_2 = input('Хотите еще изменить статус места?\n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
            if test_choice_2 == 'n':
                break

    # Изменяем название шоу
    if choice == 3:
        # Выводим все доступные шоу
        get_shows()

        # Проверка на то, что id шоу - целое положительное число и существует в таблице категорий
        while True:
            try:
                # Меняем на выбранное шоу
                show_id_new = int(input('Введите id шоу, на которое хотите поменять сеанс: '))
                if show_id_new > 0:
                    cursor.execute("SELECT id, name FROM shows ORDER BY id")
                    get_shows_check = cursor.fetchall()
                    list_ids = []
                    for c in get_shows_check:
                        list_ids.append(c['id'])
                    if show_id_new <= list_ids[-1]:
                        break
                    else:
                        print('По введенному id не возможно назначить шоу')
                else:
                    print('По введенному id не возможно назначить шоу')
            except ValueError:
                print('По введенному id не возможно назначить шоу')

        # Изменяем название шоу в сеансе

        show_new = '''
        UPDATE {session} SET shows_id = :show_id_new WHERE date = :date
        '''
        cursor.execute(show_new.format(session=f'\'sessions-hall-prices\''),
                       {'date': date, 'show_id_new': show_id_new})
        db.commit()

    # Изменяем дату проведения сеанса
    if choice == 4:

        date_new = input('Введите новую дату проведения сеанса: ')

        # Проверка формата ввода даты
        if not date_new:
            print('Вы не ввели дату проведения сеанса. Попробуйте еще раз')
            exit()

        # Проверка формата ввода даты
        pattern = r"^(20[0-9][0-9])-(0[1-9]|1[1-2])-(0[0-9]|1[0-9]|2[0-9]|3[0-1])\s([0-1][0-9]|2[0-3]):([0-5][0-9])$"
        if not re.findall(pattern, date_new):
            print('Не правильный формат даты. Введите дату в формате - "YYYY-MM-DD hh:mm"')
            exit()

        # Проверяем есть ли уже созданный сеанс на эту дату
        cursor.execute('''
                SELECT date, shows.name, categories.category, hall."row", hall.seat, status.status, prices.price FROM 'sessions-hall'
                INNER JOIN shows ON shows_id = shows.id
                INNER JOIN hall ON hall_id = hall.id
                INNER JOIN status ON status_id = status.id
                INNER JOIN categories ON shows.category_id = categories.id
                INNER JOIN prices ON price_id = prices.id
                WHERE date = :date''', {'date': date_new})
        get_session_hall = cursor.fetchall()

        cursor.execute('''
                SELECT date, shows.name, categories.category, hall_prices."row", hall_prices.seat, hall_prices.price, \
                status.status FROM 'sessions-hall-prices'
                INNER JOIN shows ON shows_id = shows.id
                INNER JOIN hall_prices ON hall_id = hall_prices.id
                INNER JOIN status ON status_id = status.id
                INNER JOIN categories ON shows.category_id = categories.id
                WHERE date = :date''', {'date': date_new})
        get_session_hall_prices = cursor.fetchall()

        if get_session_hall:
            print('ВНИМАНИЕ: Обнаружено что сеанс на данную дату уже создан!')
            test_warning_1 = input('Нажмите "ENTER", чтобы посмотреть на этот сеанс или "n" и "ENTER", чтобы не выйти: ')
            if test_warning_1 != 'n':
                for s in get_session_hall:
                    print(
                        f"{s['date']} - \"{s['name']}\" ({s['category']}) - {s['row']}/{s['seat']} - {s['price']} - {s['status']}")
                exit()
            else:
                exit()
                db.close()

        if get_session_hall_prices:
            print('ВНИМАНИЕ: Обнаружено что сеанс на данную дату уже создан!')
            test_warning_1 = input('Нажмите "ENTER", чтобы посмотреть на этот сеанс или "n" и "ENTER", чтобы не выйти: ')
            if test_warning_1 != 'n':
                for s in get_session_hall_prices:
                    print(
                        f"{s['date']} - \"{s['name']}\" ({s['category']}) - {s['row']}/{s['seat']} - {s['price']} - {s['status']}")
                exit()
            else:
                exit()
                db.close()

        # Делаем изменения
        cursor.execute("UPDATE 'sessions-hall-prices' SET date = :date_new WHERE date = :date",
                           {'date_new': date_new, 'date': date})
        db.commit()

    if choice != 1 and choice != 2 and choice != 3 and choice != 4:
        print('Вы ввели не правильное значение.')
        exit()

    test = input('Хотите еще сделать изменения в сеансах? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if test == 'n':
        db.close()
        break
