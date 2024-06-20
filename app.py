import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%d-%m-%Y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)


# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('pharmacy.db')
    conn.row_factory = sqlite3.Row
    return conn


# Маршруты
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        secret = request.form['used_secret']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password, secret) VALUES (?, ?, ?)',
                     (username, hashed_password, secret))
        conn.commit()
        conn.close()

        logger.info(f'Зарегистрирован новый пользователь: {username}')

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['username']
            logger.info(f'Пользователь вошел в систему: {username}')
            return redirect(url_for('index'))
        else:
            logger.warning(f'Неудачная попытка входа: {username}')

    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'user_id' in session:
        user_id = session['user_id']
        logger.info(f'Пользователь вышел из системы: {user_id}')
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    pharmacies = conn.execute('SELECT * FROM pharmacies').fetchall()
    conn.close()
    return render_template('index.html', pharmacies=pharmacies)


@app.route('/select_pharmacy/<int:pharmacy_id>')
def select_pharmacy(pharmacy_id):
    session['pharmacy_id'] = pharmacy_id
    return redirect(url_for('drugs'))


@app.route('/drugs')
def drugs():
    if 'pharmacy_id' not in session:
        return redirect(url_for('index'))

    pharmacy_id = session['pharmacy_id']
    conn = get_db_connection()
    drugs = conn.execute('SELECT * FROM drugs WHERE pharmacy_id = ?', (pharmacy_id,)).fetchall()
    conn.close()
    return render_template('drugs.html', drugs=drugs)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'pharmacy_id' not in session:
        return redirect(url_for('index'))

    pharmacy_id = session['pharmacy_id']
    if request.method == 'POST':
        name = request.form['name']
        form = request.form['form']
        dosage = request.form['dosage']
        package = request.form['package']

        conn = get_db_connection()
        conn.execute('INSERT INTO drugs (pharmacy_id, name, form, dosage, package) VALUES (?, ?, ?, ?, ?)',
                     (pharmacy_id, name, form, dosage, package))
        conn.commit()
        conn.close()

        logger.info(f'Добавлен новый препарат: {name} (Аптека ID: {pharmacy_id})')

        return redirect(url_for('drugs'))

    return render_template('add.html')


@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    if 'pharmacy_id' not in session:
        return redirect(url_for('index'))

    pharmacy_id = session['pharmacy_id']
    conn = get_db_connection()
    drug = conn.execute('SELECT * FROM drugs WHERE id = ? AND pharmacy_id = ?', (id, pharmacy_id)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        form = request.form['form']
        dosage = request.form['dosage']
        package = request.form['package']

        conn.execute('UPDATE drugs SET name = ?, form = ?, dosage = ?, package = ? WHERE id = ? AND pharmacy_id = ?',
                     (name, form, dosage, package, id, pharmacy_id))
        conn.commit()
        conn.close()

        logger.info(f'Препарат отредактирован: ID {id} (Аптека ID: {pharmacy_id})')

        return redirect(url_for('drugs'))

    conn.close()
    return render_template('edit.html', drug=drug)


@app.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    if 'pharmacy_id' not in session:
        return redirect(url_for('index'))

    pharmacy_id = session['pharmacy_id']
    conn = get_db_connection()
    conn.execute('DELETE FROM drugs WHERE id = ? AND pharmacy_id = ?', (id, pharmacy_id))
    conn.commit()
    conn.close()

    logger.info(f'Препарат удален: ID {id} (Аптека ID: {pharmacy_id})')

    return redirect(url_for('drugs'))


@app.route('/admin/drugs')
def admin_drugs():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    drugs = conn.execute('''
        SELECT drugs.id, drugs.name, drugs.form, drugs.dosage, drugs.package, pharmacies.address as pharmacy_name
        FROM drugs
        JOIN pharmacies ON drugs.pharmacy_id = pharmacies.id
    ''').fetchall()
    conn.close()
    return render_template('pharmacy_list.html', drugs=drugs)


@app.route('/admin/logs')
def view_logs():
    try:
        with open('app.log', 'r', encoding='utf-8') as log_file:
            logs = log_file.readlines()
        logs = [log.strip() for log in logs]
    except FileNotFoundError:
        logs = []

    return render_template('logs.html', logs=logs)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
