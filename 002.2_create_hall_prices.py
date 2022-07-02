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


# Show The Hall with prices
def get_hall_prices():
    cursor.execute("SELECT id, row, seat, price FROM hall_prices")
    get = cursor.fetchall()
    for j in get:
        print(f"id - \"{j['id']}\" - \"{j['row']}/{j['seat']}\" - \"{j['price']}\" руб.")


# Search The Hall with prices table
cursor.execute('''
SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'hall_prices' ORDER BY name
''')

# Check The Hall with prices existing
HALL_CHECK = cursor.fetchall()
if HALL_CHECK:
    print('Зал с ценами уже создан')
    exit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS hall_prices (
    id INTEGER PRIMARY KEY, 
    row INTEGER NOT NULL,
    seat INTEGER NOT NULL,
    price INT NOT NULL
)
''')
db.commit()


while True:
    print('Введите номер ряда и количество мест в нем.')
    while True:
        try:
            ROW = int(input('Введите номер ряда: '))
            if ROW > 0:
                break
        except ValueError:
            print('Номер ряда представляет из себя целое положительное число')
        except NameError:
            print('Номер ряда представляет из себя целое положительное число')
    while True:
        try:
            SEATS = int(input('Введите количество мест для него: '))
            if SEATS > 0:
                break
        except ValueError:
            print('Номер места представляет из себя целое положительное число')
        except NameError:
            print('Номер места представляет из себя целое положительное число')
    while True:
        try:
            PRICE = int(input('Введите цену для этого ряда: '))
            if PRICE > 0:
                break
        except ValueError:
            print('Цена представляет из себя целое положительное число')
        except NameError:
            print('Цена представляет из себя целое положительное число')

    # Проверка наличия такого ряда
    cursor.execute("SELECT id, row, seat FROM hall_prices")
    get_check_hall = cursor.fetchall()
    for H_CHECK in get_check_hall:
        if H_CHECK['row'] == ROW:
            print('Ряд с таким номером уже есть. Удалите данный зал и начните заново.')
            exit()

    HALL_PRICES = []
    for i in range(1, SEATS + 1):
        HALL_PRICES.append((ROW, i, PRICE))

    cursor.executemany("INSERT INTO hall_prices (row, seat, price) VALUES (?, ?, ?)", HALL_PRICES)
    db.commit()

    CHECK = input('Хотите продолжить создавать ряды? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if CHECK == 'n':
        # Выводим зал
        get_hall_prices()

        db.close()
        break
