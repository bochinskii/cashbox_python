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

    # Выводим все цены
    print('Возможные варианты цен:')
    try:
        get_price()
    except sqlite3.OperationalError:
        print('Таблицы с ценами не существует. Сперва создайте таблицу с ценами.')
        exit()

    while True:
        price = input('Ведите цену, которую хотите изменить: ')
        if price == '0':
            print('Данное значение цены используется по-умолчанию. Ее нельзя редактировать.')
            exit()
        try:
            # Находим id цены по значению
            cursor.execute('''SELECT id FROM prices WHERE price = :price''', {'price': price})
            get_price_id = cursor.fetchall()
            PRICE_ID = get_price_id[0]['id']
            break
        except IndexError:
            print('Такой цены не существует. Попробуйте еще раз.')

    # Вводим новое значение цены
    PRICE_NEW = int(input('Введите новое значение выбранной цены: '))
    try:

        cursor.execute('''
        UPDATE prices SET price = :price WHERE id = :id''', {'price': PRICE_NEW, 'id': PRICE_ID})
        db.commit()
    except sqlite3.IntegrityError:
        print('Такая цена уже существует. Выберете другое значение.')
        exit()

    TEST = input('Хотите еще изменить уены? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if TEST == 'n':
        # Выводим наличие шоу
        get_price()
        db.close()
        break
