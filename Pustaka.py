from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__, template_folder='Depan')

DATABASE = 'instance/redmoon_library.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs('instance', exist_ok=True)

    conn = sqlite3.connect(DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS buku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            penerbit TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()


@app.route('/')
def home():
    conn = get_db_connection()
    buku_list = conn.execute('SELECT * FROM buku ORDER BY id ASC').fetchall()
    conn.close()
    return render_template('home.html', buku_list=buku_list)


@app.route('/admin')
def admin():
    conn = get_db_connection()
    buku_list = conn.execute('SELECT * FROM buku ORDER BY id ASC').fetchall()
    conn.close()
    return render_template('admin.html', buku_list=buku_list)


@app.route('/tambah', methods=('GET', 'POST'))
def tambah():
    if request.method == 'POST':
        judul = request.form['judul'].strip()
        penerbit = request.form['penerbit'].strip()

        if judul and penerbit:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO buku (judul, penerbit) VALUES (?, ?)',
                (judul, penerbit)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))

    return render_template('tambah.html')


@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    buku = conn.execute('SELECT * FROM buku WHERE id = ?', (id,)).fetchone()

    if buku is None:
        conn.close()
        return redirect(url_for('admin'))

    if request.method == 'POST':
        judul = request.form['judul'].strip()
        penerbit = request.form['penerbit'].strip()

        if judul and penerbit:
            conn.execute(
                'UPDATE buku SET judul = ?, penerbit = ? WHERE id = ?',
                (judul, penerbit, id)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))

    conn.close()
    return render_template('edit.html', buku=buku)


@app.route('/hapus/<int:id>', methods=('POST',))
def hapus(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM buku WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))



if __name__ == '__main__':
    app.run(debug=True)