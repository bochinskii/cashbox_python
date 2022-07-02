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


def get_category():
    cursor.execute("SELECT id, category FROM categories ORDER BY id")
    get = cursor.fetchall()

    for i in get:
        print(f"\"{i['id']}\" - \"{i['category']}\"")


while True:

    # Выводим все категории
    print('Возможные варианты категорий:')
    try:
        get_category()
    except sqlite3.OperationalError:
        print('Таблицы с категориями не существует. Сперва создайте таблицу с категориями.')
        exit()

    # Проверка на то, что id категории - целое положительное число и существует в таблице категорий
    while True:
        try:
            category_id = int(input('Введите id категории, которую хотите отредактировать: '))
            if category_id > 0:
                cursor.execute("SELECT id, category FROM categories ORDER BY id")
                get_category_check = cursor.fetchall()
                list_ids = []
                for c in get_category_check:
                    list_ids.append(c['id'])
                if category_id <= list_ids[-1]:
                    break
                else:
                    print('По введенному id не возможно назначить категорию')
            else:
                print('По введенному id не возможно назначить категорию')
        except ValueError:
            print('По введенному id не возможно назначить категорию')

    # Вводим имя категории
    category_new_name = input('Введите новое название выбранной категории: ')

    # Проверяем имя категории
    cursor.execute("SELECT id, category FROM categories ORDER BY id")
    get_category_check = cursor.fetchall()
    for c_check in get_category_check:
        if c_check['category'] == category_new_name:
            print('Категория с таким именем уже существует')
            print(f"id - \"{c_check['id']}\" - имя категории - \"{c_check['category']}\"")
            exit()

    cursor.execute('''
    UPDATE categories SET category = :category WHERE id = :id''', {'category': category_new_name, 'id': category_id})

    db.commit()

    test = input('Хотите еще сделать изменения категории? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if test == 'n':
        # Выводим наличие шоу
        get_category()
        db.close()
        break

