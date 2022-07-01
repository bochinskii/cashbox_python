import sqlite3

# Define path to DB Location
DB_PATH = 'E:\\TEMP_WORK\\chashbox\\cashbox_db.sqlite'


# Use preset function
def dict_factory(cur, row):
    d = {}
    for idx, col in enumerate(cur.description):
        d[col[0]] = row[idx]
    return d


db = sqlite3.connect(DB_PATH)

db.row_factory = dict_factory
cursor = db.cursor()


# Show The Hall
def get_hall():
    cursor.execute("SELECT id, row, seat FROM hall")
    get = cursor.fetchall()
    for j in get:
        print(f"id - \"{j['id']}\" - \"{j['row']}/{j['seat']}\"")


# Search The Hall table
cursor.execute('''
SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'hall' ORDER BY name
''')

# Check The Hall existing
HALL_CHECK = cursor.fetchall()
if HALL_CHECK:
    print('Зал без цен уже создан')
    exit()

# Star hall
cursor.execute('''
CREATE TABLE IF NOT EXISTS hall (
id INTEGER PRIMARY KEY, 
row INTEGER NOT NULL,
seat INTEGER NOT NULL
)
''')
db.commit()

while True:
    print('Введите номер ряда и количество мест в нем.')
    while True:
        try:
            row = int(input('Введите номер ряда: '))
            if row > 0:
                break
        except ValueError:
            print('Номер ряда представляет из себя целое положительное число')
        except NameError:
            print('Номер ряда представляет из себя целое положительное число')
    while True:
        try:
            seats = int(input('Введите количество мест для него: '))
            if seats > 0:
                break
        except ValueError:
            print('Номер места представляет из себя целое положительное число')
        except NameError:
            print('Номер места представляет из себя целое положительное число')

    # Проверка наличия такого ряда
    cursor.execute("SELECT id, row, seat FROM hall")
    get_check_hall = cursor.fetchall()
    for h_check in get_check_hall:
        if h_check['row'] == row:
            print('Ряд с таким номером уже есть. Удалите данный зал и начните заново.')
            exit()

    hall = []
    for i in range(1, seats + 1):
        hall.append((row, i))

    cursor.executemany("INSERT INTO hall (row, seat) VALUES (?, ?)", hall)
    db.commit()

    check = input('Хотите продолжить создавать ряды? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if check == 'n':
        # Выводим зал
        get_hall()

        db.close()
        break

#
# Hall scheme
#
'''
hall = [
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11),
    (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14),
    (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16),
    (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16),
    (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15),
    (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12)
]'''
