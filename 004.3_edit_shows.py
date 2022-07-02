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


def get_shows():
    cursor.execute('''
    SELECT shows.id, shows.name, categories.category FROM shows
    INNER JOIN categories ON shows.category_id = categories.id ORDER BY categories.id
    ''')
    get = cursor.fetchall()

    for i in get:
        print(f"\"{i['id']}\" - \"{i['name']}\" - \"{i['category']}\"")


def get_category():
    cursor.execute("SELECT id, category FROM categories ORDER BY id")
    get = cursor.fetchall()

    for i in get:
        print(f"\"{i['id']}\" - \"{i['category']}\"")


while True:

    try:
        get_shows()
    except sqlite3.OperationalError:
        print('Таблицы с шоу не существует. Сперва создайте таблицу с шоу.')
        exit()

    # Проверка на то, что id шоу - целое положительное число и существует в таблице категорий
    while True:
        try:
            # Выбираем шоу по id
            show_id = int(input('Введите id шоу, которое хотите изменить: '))
            if show_id > 0:
                cursor.execute("SELECT id, name FROM shows ORDER BY id")
                get_shows_check = cursor.fetchall()
                list_ids = []
                for c in get_shows_check:
                    list_ids.append(c['id'])
                if show_id <= list_ids[-1]:
                    break
                else:
                    print('По введенному id не возможно назначить шоу')
            else:
                print('По введенному id не возможно назначить шоу')
        except ValueError:
            print('По введенному id не возможно назначить шоу')
    while True:
        try:
            choice = int(input('Что вы хотите изменить:\n\
"1" - название шоу;\n\
"2" - категорию шоу;\n\
"3" - имя и категорию.\n\
Введите нужное значение: '))
            if choice == 1:
                show_name_new = input('Введите новое название шоу: ')
                # Проверяем имя шоу
                cursor.execute("SELECT id, name FROM shows ORDER BY id")
                get_shows_check = cursor.fetchall()
                for s_check in get_shows_check:
                    if s_check['name'] == show_name_new:
                        print('Шоу с таким именем уже существует')
                        print(f"id - \"{s_check['id']}\" - название шоу - \"{s_check['name']}\"")
                        exit()
                cursor.execute('''
                UPDATE shows SET name = :name WHERE id = :id ''', {'name': show_name_new, 'id': show_id})
                db.commit()
                get_shows()
                break
            if choice == 2:
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
                        category_id = int(input('Введите новое id категории: '))
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

                cursor.execute('''
                UPDATE shows SET category_id = :cat WHERE id = :id ''', {'cat': category_id, 'id': show_id})
                db.commit()
                break
            if choice == 3:
                show_name_new = input('Введите новое название шоу: ')
                # Проверяем имя шоу
                cursor.execute("SELECT id, name FROM shows ORDER BY id")
                get_shows_check = cursor.fetchall()
                for s_check in get_shows_check:
                    if s_check['name'] == show_name_new:
                        print('Шоу с таким именем уже существует')
                        print(f"id - \"{s_check['id']}\" - название шоу - \"{s_check['name']}\"")
                        exit()

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
                        category_id = int(input('Введите новое id категории: '))
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

                cursor.execute('''UPDATE shows SET name = :name, category_id = :cat WHERE id = :id ''',
                               {'name': show_name_new, 'cat': category_id, 'id': show_id})
                db.commit()
                break

            if choice != 1 and choice != 2 and choice != 3:
                print('Вы ввели не существуущее значение')
        except ValueError:
            print('Вы ввели не существуущее значение')

    test = input('Хотите еще сделать изменения в шоу? \n\
Нажмите клавишу "Enter", если "да" или введите "n" и нажмите "Enter", если хотите выйти: ')
    if test == 'n':
        # Выводим наличие шоу
        db.close()
        break
