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

# Смотрим сеансы, которые у нас есть в двух таблицах
cursor.execute('''
SELECT date, shows.name, categories.category, hall."row", hall.seat, status.status, prices.price FROM 'sessions-hall'
INNER JOIN shows ON shows_id = shows.id
INNER JOIN hall ON hall_id = hall.id
INNER JOIN status ON status_id = status.id
INNER JOIN categories ON shows.category_id = categories.id
INNER JOIN prices ON price_id = prices.id ORDER BY date''')
get_result_hall = cursor.fetchall()

cursor.execute('''
SELECT date, shows.name, categories.category, hall_prices."row", hall_prices.seat, hall_prices.price, \
status.status FROM 'sessions-hall-prices'
INNER JOIN shows ON shows_id = shows.id
INNER JOIN hall_prices ON hall_id = hall_prices.id
INNER JOIN status ON status_id = status.id
INNER JOIN categories ON shows.category_id = categories.id ORDER BY date''')
get_result_hall_prices = cursor.fetchall()


print('Сеансы: ')
for r_hall_prices in get_result_hall_prices:
    if r_hall_prices['row'] == 1 and r_hall_prices['seat'] == 1:
        print(f"{r_hall_prices['date']} - \"{r_hall_prices['name']}\" ({r_hall_prices['category']})")


print('Сеансы для групп: ')
for r_hall in get_result_hall:
    if r_hall['row'] == 1 and r_hall['seat'] == 1:
        print(f"{r_hall['date']} - \"{r_hall['name']}\" ({r_hall['category']})")
