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
              FOREIGN KEY (pharmacy_id) REFERENCES pharmacies (id))
              ''')

    c.execute('''
              CREATE TABLE IF NOT EXISTS suppliers (
              id INTEGER PRIMARY KEY,
              name TEXT NOT NULL,
              inn TEXT NOT NULL,
              address TEXT NOT NULL,
              phone TEXT NOT NULL)
              ''')

    c.execute('''
              CREATE TABLE IF NOT EXISTS orders (
              id INTEGER PRIMARY KEY,
              drug_id INTEGER NOT NULL,
              supplier_id INTEGER NOT NULL,
              quantity INTEGER NOT NULL,
              price REAL NOT NULL,
              date TEXT NOT NULL,
              FOREIGN KEY (drug_id) REFERENCES drugs (id),
              FOREIGN KEY (supplier_id) REFERENCES suppliers (id))
              ''')

    c.execute('''
              CREATE TABLE IF NOT EXISTS inventory (
              id INTEGER PRIMARY KEY,
              drug_id INTEGER NOT NULL,
              quantity INTEGER NOT NULL,
              date TEXT NOT NULL,
              FOREIGN KEY (drug_id) REFERENCES drugs (id))
              ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_db()
