import sqlite3

# Define path to DB Location
DB_PATH = 'E:\\TEMP_WORK\\chashbox\\cashbox_db.sqlite'


db = sqlite3.connect(DB_PATH)
cursor = db.cursor()

# Star hall
cursor.execute('''
CREATE TABLE IF NOT EXISTS hall (
    id INTEGER PRIMARY KEY, 
    row INTEGER NOT NULL,
    seat INTEGER NOT NULL
)
''')
# Categories
cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL UNIQUE
)
''')
# Status
cursor.execute('''
CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY,
    status TEXT NOT NULL UNIQUE
)
''')

# Shows
cursor.execute('''
CREATE TABLE IF NOT EXISTS shows (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
''')

# Prices
cursor.execute('''
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY,
    price TEXT NOT NULL UNIQUE
)
''')

# Star hall with prices
cursor.execute('''
CREATE TABLE IF NOT EXISTS hall_prices (
    id INTEGER PRIMARY KEY, 
    row INTEGER NOT NULL,
    seat INTEGER NOT NULL,
    price INT NOT NULL
)
''')

# Sessions individual prices
cursor.execute('''
CREATE TABLE IF NOT EXISTS 'sessions-hall' (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    shows_id INTEGER NOT NULL,
    hall_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL DEFAULT 'свободно',
    price_id INTEGER NOT NULL, 
    FOREIGN KEY (shows_id) REFERENCES shows(id),
    FOREIGN KEY (hall_id) REFERENCES hall(id),
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (price_id) REFERENCES prices(id)
)
''')

# Sessions
cursor.execute('''
CREATE TABLE IF NOT EXISTS 'sessions-hall-prices' (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    shows_id INTEGER NOT NULL,
    hall_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL DEFAULT 'свободно', 
    FOREIGN KEY (shows_id) REFERENCES shows(id),
    FOREIGN KEY (hall_id) REFERENCES hall_prices(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
)
''')


db.commit()

db.close()
