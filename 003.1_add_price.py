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
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY,
    price TEXT NOT NULL UNIQUE
)
''')
db.commit()

# Проверка существования контента в таблице с ценами ("prices").
cursor.execute("SELECT id, price FROM prices")
GET_PRICES_CHECK = cursor.fetchall()
if not GET_PRICES_CHECK:
    # Устанавливаем значение "0" как по-умолчанию
    cursor.execute('''
    INSERT INTO prices (price) VALUES (0);''')
    db.commit()


# Выводим возможные цены
def get_price():
    cursor.execute("SELECT id, price FROM prices ORDER BY price")
    get = cursor.fetchall()

    for i in get:
        print(f"\"{i['price']}\"")


while True:
    # Выводим возможные цены
    get_price()

    name_v = int(input('Введите новую цену: '))

    try:
        cursor.execute('''
        INSERT INTO prices (price) VALUES (:price);''', {'price': name_v})
        db.commit()
    except sqlite3.IntegrityError:
        print('Такая цена уже существует')
        exit()

    test = input('Хотите еще добавить цену в базу данных? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if test == 'n':
        # Выводим наличие шоу
        get_price()
        db.close()
        break
