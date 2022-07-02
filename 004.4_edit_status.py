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


def get_status():
    cursor.execute("SELECT id, status FROM status ORDER BY id")
    get = cursor.fetchall()

    for i in get:
        print(f"\"{i['id']}\" - \"{i['status']}\"")


while True:

    try:
        get_status()
    except sqlite3.OperationalError:
        print('Таблицы со статусами не существует. Сперва создайте таблицу со статусами.')
        exit()

    # Проверка на то, что id статуса - целое положительное число и существует в таблице статусов
    while True:
        try:
            # Устанавливаем значение status по-умолчанию
            status_id = int(input('Введите id статуса, который хотите отредактировать: '))
            if status_id == 1:
                print('Данное значение статуса используется по-умолчанию. Его нельзя редактировать.')
                exit()
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

    status_new = input('Введите новое значение выбранного статуса: ')
    # Проверяем имя категории
    cursor.execute("SELECT id, status FROM status ORDER BY id")
    get_status_check = cursor.fetchall()
    for s_check in get_status_check:
        if s_check['status'] == status_new:
            print('Статус с таким значением уже существует')
            print(f"id - \"{s_check['id']}\" - значение статуса - \"{s_check['status']}\"")
            exit()

    cursor.execute('''UPDATE status SET status = :status WHERE id = :id''', {'status': status_new, 'id': status_id})

    db.commit()

    test = input('Хотите еще сделать изменения в статусах? \
    Нажмите "y", если "да" или "n", если хотите "закончить": ')

    if test == 'n':
        get_status()
        db.close()
        break
