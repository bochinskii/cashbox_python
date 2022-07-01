import sqlite3
import os

# Define path to DB Location
DB_PATH = 'E:\\TEMP_WORK\\chashbox\\cashbox_db.sqlite'

# Check DB existing
DB_CHECK = os.path.exists(DB_PATH)
if DB_CHECK:
    print(f'База данных {DB_PATH} уже существует. \
Если хотите перезаписать существующую базу данных, то сперва удалите ее.')
else:
    # Create DB
    db = sqlite3.connect(DB_PATH)
    db.close()

    # Check DB creating
    DB_CHECK = os.path.exists(DB_PATH)

    if DB_CHECK:
        print('База данных создана.')
    else:
        print('ОШИБКА. Базу данных НЕ создана.')
