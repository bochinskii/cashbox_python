import sqlite3
import re

# Define path to DB Location
DB_PATH = 'E:\\TEMP_WORK\\chashbox\\cashbox_db.sqlite'


# Параметры базы данных
def dict_factory(cur, row):
    d = {}
    for idx, col in enumerate(cur.description):
        d[col[0]] = row[idx]
    return d


db = sqlite3.connect(DB_PATH)
db.row_factory = dict_factory
cursor = db.cursor()


# Выводим все шоу которые у нас есть
def get_shows():
    cursor.execute('''
            SELECT shows.id, shows.name, categories.category FROM shows
            INNER JOIN categories ON shows.category_id = categories.id ORDER BY categories.category
            ''')
    get_shows = cursor.fetchall()
    for i in get_shows:
        print(f"\"{i['id']}\" - \"{i['name']}\" - \"{i['category']}\"")


# Выводим статусы которые у нас есть
def get_status():
    cursor.execute('''
    SELECT id, status FROM status ORDER BY id
    ''')
    get_status = cursor.fetchall()
    for s in get_status:
        print(f"\"{s['id']}\" - {s['status']}")


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

# Создаем таблицу сеанса с ценами
cursor.execute('''
CREATE TABLE IF NOT EXISTS 'sessions-hall-prices' (
    id INTEGER PRIMARY KEY,
    date DATETIME NOT NULL,
    shows_id INTEGER NOT NULL,
    hall_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL, 
    FOREIGN KEY (shows_id) REFERENCES shows(id),
    FOREIGN KEY (hall_id) REFERENCES hall_prices(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
)
''')
db.commit()

# Создаем таблицу сеанса без цен, если ее нет (чтобы не было ошибки)
cursor.execute('''
CREATE TABLE IF NOT EXISTS 'sessions-hall' (
        id INTEGER PRIMARY KEY,
        date DATETIME NOT NULL,
        shows_id INTEGER NOT NULL,
        hall_id INTEGER NOT NULL,
        status_id INTEGER NOT NULL,
        price_id INTEGER, 
        FOREIGN KEY (shows_id) REFERENCES shows(id),
        FOREIGN KEY (hall_id) REFERENCES hall(id),
        FOREIGN KEY (status_id) REFERENCES status(id),
        FOREIGN KEY (price_id) REFERENCES prices(id)
)''')
db.commit()

# Смотрим сеансы, которые у нас есть
cursor.execute('''
SELECT date, shows.name, categories.category, hall."row", hall.seat, status.status, prices.price FROM 'sessions-hall'
INNER JOIN shows ON shows_id = shows.id
INNER JOIN hall ON hall_id = hall.id
INNER JOIN status ON status_id = status.id
INNER JOIN categories ON shows.category_id = categories.id
INNER JOIN prices ON price_id = prices.id ORDER BY date''')
get_result_hall = cursor.fetchall()

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


print('Сеансы для групп: ')
for r_hall in get_result_hall:
    if r_hall['row'] == 1 and r_hall['seat'] == 1:
        print(f"{r_hall['date']} - \"{r_hall['name']}\" ({r_hall['category']})")


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

# Проверяем есть ли уже созданный сеанс на эту дату
cursor.execute('''
SELECT date, shows.name, categories.category, hall."row", hall.seat, status.status, prices.price FROM 'sessions-hall'
INNER JOIN shows ON shows_id = shows.id
INNER JOIN hall ON hall_id = hall.id
INNER JOIN status ON status_id = status.id
INNER JOIN categories ON shows.category_id = categories.id
INNER JOIN prices ON price_id = prices.id
WHERE date = strftime('%Y-%m-%d %H:%M',:date)''', {'date': date})
get_session_hall = cursor.fetchall()

cursor.execute('''
SELECT date, shows.name, categories.category, hall_prices."row", hall_prices.seat, hall_prices.price, \
status.status FROM 'sessions-hall-prices'
INNER JOIN shows ON shows_id = shows.id
INNER JOIN hall_prices ON hall_id = hall_prices.id
INNER JOIN status ON status_id = status.id
INNER JOIN categories ON shows.category_id = categories.id
WHERE date = strftime('%Y-%m-%d %H:%M',:date)''', {'date': date})
get_session_hall_prices = cursor.fetchall()

if get_session_hall:
    print('ВНИМАНИЕ: Обнаружено что сеанс на данную дату уже создан!')
    test_warning_1 = input('Нажмите "y", чтобы посмотреть на этот сеанс или "n", чтобы не выйти: ')
    if test_warning_1 == 'y':
        for s in get_session_hall:
            print(f"{s['date']} - \"{s['name']}\" ({s['category']}) - {s['row']}/{s['seat']} - {s['price']} - {s['status']}")
        exit()
    else:
        exit()
        db.close()

if get_session_hall_prices:
    print('ВНИМАНИЕ: Обнаружено что сеанс на данную дату уже создан!')
    test_warning_1 = input('Нажмите "y", чтобы посмотреть на этот сеанс или "n", чтобы не выйти: ')
    if test_warning_1 == 'y':
        for s in get_session_hall_prices:
            print(f"{s['date']} - \"{s['name']}\" ({s['category']}) - {s['row']}/{s['seat']} - {s['price']} - {s['status']}")
        exit()
    else:
        exit()
        db.close()

# Смотрим шоу, которые у нас есть
print('Шоу в наличии:')
get_shows()


# Проверка на то, что id шоу - целое положительное число и существует в таблице категорий
while True:
    try:
        # Выбираем шоу по id
        show_id = int(input('Введите id шоу, которое запланировано на выбранную дату: '))
        if show_id > 0:
            cursor.execute("SELECT id, name FROM shows ORDER BY id")
            get_shows_check = cursor.fetchall()
            list_ids = []
            for c in get_shows_check:
                list_ids.append(c['id'])
            if show_id <= list_ids[-1]:
                break
            else:
                print('По введенному id не возможно назначить шоу')
        else:
            print('По введенному id не возможно назначить шоу')
    except ValueError:
        print('По введенному id не возможно назначить шоу')

# Выводим статусы которые у нас есть
get_status()


# Проверка на то, что id статуса - целое положительное число и существует в таблице статусов
while True:
    try:
        # Устанавливаем значение status по-умолчанию
        status_id = int(input('Ведите id статуса по-умолчанию для всех мест данного сеанса: '))
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
                test = input('Хотите использовать значение по-умолчанию - "1"? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
                if test != 'n':
                    status_id = 1
                    break
        else:
            print('По введенному id не возможно назначить статус')
            test = input('Хотите использовать значение по-умолчанию - "1"? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
            if test != 'n':
                status_id = 1
                break
    except ValueError:
        print('По введенному id не возможно назначить статус')
        test = input('Хотите использовать значение по-умолчанию - "1"? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
        if test != 'n':
            status_id = 1
            break

# Проверка на существование талицы зала с ценами
cursor.execute('''
SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'hall_prices' ORDER BY name
''')
hall_check = cursor.fetchall()


# Устанавливаем ряды и меса
cursor.execute('''
SELECT id FROM hall_prices
''')
get_hall = cursor.fetchall()


# Наполняем таблицу значениями по-умолчанию
try:
    for h in get_hall:
        cursor.execute(
            "INSERT INTO 'sessions-hall-prices' (date, shows_id, hall_id, status_id) VALUES (strftime('%Y-%m-%d %H:%M',:date), :show, :hall, :status)",
            {'date': date, 'show': show_id, 'hall': h['id'], 'status': status_id})
        db.commit()
except sqlite3.IntegrityError:
    print('Не правильный формат даты. Введите дату в формате - "YYYY-MM-DD hh:mm"')
    exit()

test = input('Сеанс создан. Хотите посмотреть результат? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
if test == 'n':
    print('Всего хорошего!')
    db.close()
    exit()
else:
    cursor.execute('''
    SELECT date, shows.name, categories.category, hall_prices."row", hall_prices.seat, hall_prices.price, \
    status.status FROM 'sessions-hall-prices'
    INNER JOIN shows ON shows_id = shows.id
    INNER JOIN hall_prices ON hall_id = hall_prices.id
    INNER JOIN status ON status_id = status.id
    INNER JOIN categories ON shows.category_id = categories.id
    WHERE date = strftime('%Y-%m-%d %H:%M',:date)''',
                   {'date': date})
    get_result = cursor.fetchall()

    for r in get_result:
        print(
            f"{r['date']} - \"{r['name']}\" ({r['category']}) - {r['row']}/{r['seat']} - {r['price']} - {r['status']}")
    db.close()

