import sqlite3

def initiale_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)
    ''')
    conn.commit()
    #date = [
       # ('Милона', 'средство', 100), ('ГлобиФер', 'средство', 200), ('Хелибакт', 'средство', 300), ('Компливит', 'средство', 400)
    #]
    cursor.execute("INSERT INTO products(title, description, price) VALUES ('Милона-11', 'средство для предстательной железы', 100)")
    cursor.execute("INSERT INTO products(title, description, price) VALUES ('ГлобоФер', 'повышает железо', 200)")
    cursor.execute("INSERT INTO products(title, description, price) VALUES ('Хелибакт', 'средство для ЖКТ', 300)")
    cursor.execute("INSERT INTO products(title, description, price) VALUES ('Компливит', 'витаминный комплекс', 400)")
    conn.commit()
    conn.close()
def get_all_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.commit()
    conn.close()
    return products

