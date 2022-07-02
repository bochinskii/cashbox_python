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
    INNER JOIN categories ON shows.category_id = categories.id ORDER BY shows.category_id
    ''')
    get = cursor.fetchall()

    for i in get:
        print(f"\"{i['id']}\" - \"{i['name']}\" - \"{i['category']}\"")


def get_category():
    cursor.execute("SELECT id, category FROM categories ORDER BY id")
    get = cursor.fetchall()

    for i in get:
        print(f"\"{i['id']}\" - \"{i['category']}\"")


# Проверка существования таблицы с категориями - "categories".
try:
    cursor.execute("SELECT id, category FROM categories ORDER BY id")
    get_category_check = cursor.fetchall()
except sqlite3.OperationalError:
    print('Не возможно добавить шоу т.к. нет ни одной категории. Создайте сперва категории.')
    exit()

# Создаетм таблицу в базе данных, если ее нет.
cursor.execute('''
CREATE TABLE IF NOT EXISTS shows (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL UNIQUE,
category_id INTEGER NOT NULL,
FOREIGN KEY (category_id) REFERENCES categories(id)
)
''')
db.commit()

while True:
    # Выводим наличие шоу
    get_shows()

    NAME_V = input('Введите название шоу: ')
    # Проверка наличия такого шоу по имени
    cursor.execute('''
        SELECT shows.id, shows.name, categories.category FROM shows
        INNER JOIN categories ON shows.category_id = categories.id ORDER BY shows.category_id
        ''')
    get_shows_check = cursor.fetchall()

    for s in get_shows_check:
        if s['name'] == NAME_V:
            print('Такое шоу уже существует')
            exit()

    # Выводим все категории
    print('Возможные варианты категорий:')
    get_category()

    # Проверка на то, что id категории - целое положительное число и существует в таблице категорий
    while True:
        try:
            CATEGORY_V = int(input('Введите id категории для данного шоу: '))
            if CATEGORY_V > 0:
                cursor.execute("SELECT id, category FROM categories ORDER BY id")
                GET_CATEGORY_CHECK = cursor.fetchall()
                LIST_IDS = []
                for c in GET_CATEGORY_CHECK:
                    LIST_IDS.append(c['id'])
                if CATEGORY_V <= LIST_IDS[-1]:
                    break
                else:
                    print('По введенному id не возможно назначить категорию')
            else:
                print('По введенному id не возможно назначить категорию')
        except ValueError:
            print('По введенному id не возможно назначить категорию')

    # Заполняем таблицу
    SHOW_L = [
        (NAME_V, CATEGORY_V)
    ]

    cursor.executemany("INSERT INTO shows (name, category_id) VALUES (?, ?)", SHOW_L)
    db.commit()

    TEST = input('Хотите еще добавить шоу в базу данных? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if TEST == 'n':
        # Выводим наличие шоу
        get_shows()
        db.close()
        break




