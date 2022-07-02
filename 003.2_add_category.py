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

cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL UNIQUE
)
''')
db.commit()


# Выводим существующие категории
def get_category():
    cursor.execute("SELECT id, category FROM categories ORDER BY id")
    get = cursor.fetchall()

    for i in get:
        print(f"\"{i['id']}\" - \"{i['category']}\"")


while True:
    # Выводим существующие категории
    get_category()

    NAME_V = input('Введите название категории: ')

    try:
        cursor.execute('''
        INSERT INTO categories (category) VALUES (:category);''', {'category': NAME_V})
        db.commit()
    except sqlite3.IntegrityError:
        print('Такая категория уже существует')
        exit()

    test = input('Хотите еще добавить шоу в базу данных? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if test == 'n':
        # Выводим категории
        get_category()
        db.close()
        break
