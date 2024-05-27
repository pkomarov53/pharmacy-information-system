from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('pharmacy.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    drugs = conn.execute('SELECT * FROM drugs').fetchall()
    conn.close()
    return render_template('index.html', drugs=drugs)


@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        form = request.form['form']
        dosage = request.form['dosage']
        package = request.form['package']

        conn = get_db_connection()
        conn.execute('INSERT INTO drugs (name, form, dosage, package) VALUES (?, ?, ?, ?)',
                     (name, form, dosage, package))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    drug = conn.execute('SELECT * FROM drugs WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        form = request.form['form']
        dosage = request.form['dosage']
        package = request.form['package']

        conn.execute('UPDATE drugs SET name = ?, form = ?, dosage = ?, package = ? WHERE id = ?',
                     (name, form, dosage, package, id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', drug=drug)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM drugs WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
