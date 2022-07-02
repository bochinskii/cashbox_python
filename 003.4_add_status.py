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
CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY,
    status TEXT NOT NULL UNIQUE
)
''')
db.commit()

# Проверка существования контента в таблице со статусами ("status").
cursor.execute("SELECT id, status FROM status")
get_status_check = cursor.fetchall()
if not get_status_check:
    # Устанавливаем значение "0" как по-умолчанию
    cursor.execute('''
    INSERT INTO status (status) VALUES ('свободно');''')
    db.commit()


# Выводим возможные статусы
def get_status():
    cursor.execute("SELECT id, status FROM status ORDER BY id")
    get = cursor.fetchall()

    for i in get:
        print(f"\"{i['id']}\" - \"{i['status']}\"")


while True:
    # Выводим возможные статусы
    get_status()

    NAME_V = input('Введите новый статус: ')

    try:
        cursor.execute('''
        INSERT INTO status (status) VALUES (:status);''', {'status': NAME_V})
        db.commit()
    except sqlite3.IntegrityError:
        print('Такой статус уже существует')
        exit()

    test = input('Хотите еще добавить статус в базу данных? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if test == 'n':
        # Выводим наличие шоу
        get_status()
        db.close()
        break
