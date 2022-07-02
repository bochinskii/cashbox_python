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
    get_category()

    # Проверка на то, что id категории - целое положительное число и существует в таблице категорий
    while True:
        try:
            category_id = int(input('Введите id категории, которую хотите удалить: '))
            if category_id > 0:
                cursor.execute("SELECT id, category FROM categories ORDER BY id")
                get_category_check = cursor.fetchall()
                list_ids = []
                for c in get_category_check:
                    list_ids.append(c['id'])
                if category_id <= list_ids[-1]:
                    break
                else:
                    print('По введенному id не возможно удалить категорию')
            else:
                print('По введенному id не возможно удалить категорию')
        except ValueError:
            print('По введенному id не возможно удалить категорию')
        except IndexError:
            print('Таблица с категориями пуста')
            exit()

    # Смотрим наличие выбранной категории в шоу чтобы ее не удалить, если она есть
    try:
        cursor.execute('''
        SELECT category_id FROM shows''')
        get_result_shows = cursor.fetchall()
        for s_check in get_result_shows:
            if s_check['category_id'] == category_id:
                print('Невозможно удалить категорию т.к. существует(ют) шоу с данной категорией. Сперва удалите шоу')
                exit()
    except sqlite3.OperationalError:
        cursor.execute('''DELETE FROM categories WHERE id = :category ''', {'category': category_id})
        db.commit()

    cursor.execute('''DELETE FROM categories WHERE id = :category ''', {'category': category_id})
    db.commit()

    test = input('Хотите еще удалить категорию из базы данных? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if test == 'n':
        # Выводим наличие шоу
        get_category()
        db.close()
        break
