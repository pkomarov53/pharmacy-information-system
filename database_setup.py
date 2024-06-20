import sqlite3


def initialize_db():
    conn = sqlite3.connect('pharmacy.db')
    c = conn.cursor()

    c.execute('''
              CREATE TABLE IF NOT EXISTS pharmacies (
              id INTEGER PRIMARY KEY,
              name TEXT NOT NULL,
              address TEXT NOT NULL,
              phone TEXT NOT NULL)
              ''')

    c.execute('''
              CREATE TABLE IF NOT EXISTS drugs (
              id INTEGER PRIMARY KEY,
              pharmacy_id INTEGER NOT NULL,
              name TEXT NOT NULL,
              form TEXT NOT NULL,
              dosage TEXT NOT NULL,
              package TEXT NOT NULL,
              additional_info TEXT,
              FOREIGN KEY (pharmacy_id) REFERENCES pharmacies (id))
              ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            secret TEXT NOT NULL)
    ''')

    pharmacies_data = [
        (1, 'Аптека Здоровье', 'ул. Ленина, 15', '555-1234'),
        (2, 'Аптека Надежда', 'ул. Мира, 23', '555-5678'),
        (3, 'Аптека Добро', 'ул. Победы, 7', '555-9012'),
        (4, 'Аптека Жизнь', 'пр. Советский, 10', '555-3456'),
        (5, 'Аптека Спасение', 'ул. Гагарина, 3', '555-7890')
    ]
    c.executemany('INSERT INTO pharmacies (id, name, address, phone) VALUES (?, ?, ?, ?)', pharmacies_data)

    # Вставка данных в таблицу drugs
    drugs_data = [
        (1, 1, 'Аспирин', 'Таблетки', '500 мг', 'Коробка 20 шт.', 'Обезболивающее средство'),
        (2, 1, 'Ибупрофен', 'Таблетки', '200 мг', 'Коробка 30 шт.', 'Противовоспалительное средство'),
        (3, 2, 'Парацетамол', 'Сироп', '250 мг/5 мл', 'Флакон 100 мл', 'Жаропонижающее средство'),
        (4, 3, 'Амоксициллин', 'Капсулы', '250 мг', 'Коробка 10 шт.', 'Антибиотик'),
        (5, 4, 'Лоратадин', 'Таблетки', '10 мг', 'Коробка 15 шт.', 'Антигистаминное средство'),
        (6, 4, 'Нурофен для детей', 'Сироп', '100 мг/5 мл', 'Флакон 150 мл', 'Противовоспалительное средство'),
        (7, 5, 'Дексаметазон', 'Капли', '1 мг/мл', 'Флакон 5 мл', 'Глюкокортикостероидное средство'),
        (8, 5, 'Эспумизан', 'Капсулы', '40 мг', 'Коробка 20 шт.', 'Противогазовое средство'),
        (9, 5, 'Фенкарол', 'Таблетки', '100 мг', 'Коробка 30 шт.', 'Противокашлевое средство'),
        (10, 5, 'Фенистил', 'Гель', '1 мг/мл', 'Тюбик 50 г', 'Антигистаминное средство')
    ]
    c.executemany(
        'INSERT INTO drugs (id, pharmacy_id, name, form, dosage, package, additional_info) VALUES (?, ?, ?, ?, ?, ?, ?)',
        drugs_data)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_db()
