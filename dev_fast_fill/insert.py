import sqlite3

# Define path to DB Location
DB_PATH = 'E:\\TEMP_WORK\\chashbox\\cashbox_db.sqlite'

db = sqlite3.connect(DB_PATH)
cursor = db.cursor()

#
# Fill the hall
#
HALL = [
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11),
    (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 13), (2, 14),
    (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16),
    (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (4, 16),
    (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15),
    (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12)
]
cursor.executemany("INSERT INTO hall (row, seat) VALUES (?, ?)", HALL)

#
# Fill the hall with prices
#
price_row_1 = 100
price_row_2 = 200
price_row_3 = 200
price_row_4 = 300
price_row_5 = 600
price_row_6 = 600
HALL_PRICES = [
    (1, 1, price_row_1), (1, 2, price_row_1), (1, 3, price_row_1), (1, 4, price_row_1), (1, 5, price_row_1), (1, 6, price_row_1), (1, 7, price_row_1), (1, 8, price_row_1), (1, 9, price_row_1), (1, 10, price_row_1), (1, 11, price_row_1),
    (2, 1, price_row_2), (2, 2, price_row_2), (2, 3, price_row_2), (2, 4, price_row_2), (2, 5, price_row_2), (2, 6, price_row_2), (2, 7, price_row_2), (2, 8, price_row_2), (2, 9, price_row_2), (2, 10, price_row_2), (2, 11, price_row_2), (2, 12, price_row_2), (2, 13, price_row_2), (2, 14, price_row_2),
    (3, 1, price_row_3), (3, 2, price_row_3), (3, 3, price_row_3), (3, 4, price_row_3), (3, 5, price_row_3), (3, 6, price_row_3), (3, 7, price_row_3), (3, 8, price_row_3), (3, 9, price_row_3), (3, 10, price_row_3), (3, 11, price_row_3), (3, 12, price_row_3), (3, 13, price_row_3), (3, 14, price_row_3), (3, 15, price_row_3), (3, 16, price_row_3),
    (4, 1, price_row_4), (4, 2, price_row_4), (4, 3, price_row_4), (4, 4, price_row_4), (4, 5, price_row_4), (4, 6, price_row_4), (4, 7, price_row_4), (4, 8, price_row_4), (4, 9, price_row_4), (4, 10, price_row_4), (4, 11, price_row_4), (4, 12, price_row_4), (4, 13, price_row_4), (4, 14, price_row_4), (4, 15, price_row_4), (4, 16, price_row_4),
    (5, 1, price_row_5), (5, 2, price_row_5), (5, 3, price_row_5), (5, 4, price_row_5), (5, 5, price_row_5), (5, 6, price_row_5), (5, 7, price_row_5), (5, 8, price_row_5), (5, 9, price_row_5), (5, 10, price_row_5), (5, 11, price_row_5), (5, 12, price_row_5), (5, 13, price_row_5), (5, 14, price_row_5), (5, 15, price_row_5),
    (6, 1, price_row_6), (6, 2, price_row_6), (6, 3, price_row_6), (6, 4, price_row_6), (6, 5, price_row_6), (6, 6, price_row_6), (6, 7, price_row_6), (6, 8, price_row_6), (6, 9, price_row_6), (6, 10, price_row_6), (6, 11, price_row_6), (6, 12, price_row_6)
]
cursor.executemany("INSERT INTO hall_prices (row, seat, price) VALUES (?, ?, ?)", HALL_PRICES)

#
# Fill the category
#
cursor.executescript('''
INSERT INTO categories (category) VALUES ('сеанс для детей');
INSERT INTO categories (category) VALUES ('сеанс для широкого круга зрителей');
''')

#
#  Fill the status
#
cursor.executescript('''
INSERT INTO status (status) VALUES ('свободно');
INSERT INTO status (status) VALUES ('продано');
INSERT INTO status (status) VALUES ('продано предварительно 1');
INSERT INTO status (status) VALUES ('продано предварительно 2');
INSERT INTO status (status) VALUES ('продано предварительно 3');
INSERT INTO status (status) VALUES ('продано предварительно 4');
INSERT INTO status (status) VALUES ('продано предварительно 5');
''')

#
#  Fill the prices
#
cursor.executescript('''
INSERT INTO prices (price) VALUES (100);
INSERT INTO prices (price) VALUES (200);
INSERT INTO prices (price) VALUES (300);
INSERT INTO prices (price) VALUES (400);
''')


db.commit()

db.close()
