from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'kidlB3CmgUZ4rrLv-gmyiaPfZLUNsz7tm-EruSzmDOctVAsaJh-eK6w8UvWaLsBkuJ1-G4acFp6nLWPeqRhW'


def get_db_connection():
    conn = sqlite3.connect('pharmacy.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
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


@app.route('/add', methods=('GET', 'POST'))
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

        return redirect(url_for('drugs'))

    return render_template('add.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
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

        return redirect(url_for('drugs'))

    conn.close()
    return render_template('edit.html', drug=drug)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    if 'pharmacy_id' not in session:
        return redirect(url_for('index'))

    pharmacy_id = session['pharmacy_id']
    conn = get_db_connection()
    conn.execute('DELETE FROM drugs WHERE id = ? AND pharmacy_id = ?', (id, pharmacy_id))
    conn.commit()
    conn.close()

    return redirect(url_for('drugs'))


if __name__ == '__main__':
    app.run(debug=True)
