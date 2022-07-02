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


# Просмотр зала с ценами по рядам
def get_hall_prices():
    get = cursor.execute('''
    SELECT hall_prices."row", hall_prices.seat, hall_prices.price FROM hall_prices
    ''')
    for i in get:
        print(f"\"{i['row']}/{i['seat']}\" - \"{i['price']}\"")


try:
    get_hall_prices()
except sqlite3.OperationalError:
    print('Таблицы зала с ценами не существует. Сперва создайте зал с ценами.')
    exit()

while True:
    try:
        first_row = int(input('Введите новую цену для 1-го ряда: '))
        if first_row > 0:
            break
        else:
            print('Нужно ввести положительное целое число. Попробуйте еще раз')
    except ValueError:
        print('Нужно ввести положительное целое число. Попробуйте еще раз')

while True:
    try:
        second_row = int(input('Введите новую цену для 2-го ряда: '))
        if second_row > 0:
            break
        else:
            print('Нужно ввести положительное целое число. Попробуйте еще раз')
    except ValueError:
        print('Нужно ввести положительное целое число. Попробуйте еще раз')

while True:
    try:
        third_row = int(input('Введите новую цену для 3-го ряда: '))
        if third_row > 0:
            break
        else:
            print('Нужно ввести положительное целое число. Попробуйте еще раз')
    except ValueError:
        print('Нужно ввести положительное целое число. Попробуйте еще раз')

while True:
    try:
        fourth_row = int(input('Введите новую цену для 4-го ряда: '))
        if fourth_row > 0:
            break
        else:
            print('Нужно ввести положительное целое число. Попробуйте еще раз')
    except ValueError:
        print('Нужно ввести положительное целое число. Попробуйте еще раз')

while True:
    try:
        fifth_row = int(input('Введите новую цену для 5-го ряда: '))
        if fifth_row > 0:
            break
        else:
            print('Нужно ввести положительное целое число. Попробуйте еще раз')
    except ValueError:
        print('Нужно ввести положительное целое число. Попробуйте еще раз')

while True:
    try:
        sixth_row = int(input('Введите новую цену для 6-го ряда: '))
        if sixth_row > 0:
            break
        else:
            print('Нужно ввести положительное целое число. Попробуйте еще раз')
    except ValueError:
        print('Нужно ввести положительное целое число. Попробуйте еще раз')

if first_row:
    first_row = int(first_row)
    cursor.execute('''
    UPDATE hall_prices SET price = :price WHERE row = 1
    ''', {'price': first_row})
if second_row:
    second_row = int(second_row)
    cursor.execute('''
    UPDATE hall_prices SET price = :price WHERE row = 2
    ''', {'price': second_row})
if third_row:
    third_row = int(third_row)
    cursor.execute('''
    UPDATE hall_prices SET price = :price WHERE row = 3
    ''', {'price': third_row})
if fourth_row:
    fourth_row = int(fourth_row)
    cursor.execute('''
    UPDATE hall_prices SET price = :price WHERE row = 4
    ''', {'price': fourth_row})
if fifth_row:
    fifth_row = int(fifth_row)
    cursor.execute('''
    UPDATE hall_prices SET price = :price WHERE row = 5
    ''', {'price': fifth_row})
if sixth_row:
    sixth_row = int(sixth_row)
    cursor.execute('''
    UPDATE hall_prices SET price = :price WHERE row = 6
    ''', {'price': sixth_row})

db.commit()

get_hall_prices()

db.close()
