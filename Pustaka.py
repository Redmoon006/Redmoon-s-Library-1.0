from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__, template_folder='Depan')

DATABASE = 'instance/redmoon_library.db'


# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# INIT DATABASE
def init_db():
    os.makedirs('instance', exist_ok=True)

    conn = sqlite3.connect(DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS buku (
            id_buku TEXT PRIMARY KEY,
            judul_buku TEXT NOT NULL,
            penerbit TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()


# HOME (WEB UTAMA)
@app.route('/')
def home():
    keyword = request.args.get('keyword', '').strip()

    conn = get_db_connection()

    if keyword:
        buku_list = conn.execute('''
            SELECT * FROM buku
            WHERE id_buku LIKE ?
               OR judul_buku LIKE ?
               OR penerbit LIKE ?
            ORDER BY id_buku ASC
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%')).fetchall()
    else:
        buku_list = conn.execute('SELECT * FROM buku ORDER BY id_buku ASC').fetchall()

    conn.close()
    return render_template('home.html', buku_list=buku_list, keyword=keyword)


# ADMIN PANEL
@app.route('/admin')
def admin():
    keyword = request.args.get('keyword', '').strip()

    conn = get_db_connection()

    if keyword:
        buku_list = conn.execute('''
            SELECT * FROM buku
            WHERE id_buku LIKE ?
               OR judul_buku LIKE ?
               OR penerbit LIKE ?
            ORDER BY id_buku ASC
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%')).fetchall()
    else:
        buku_list = conn.execute('SELECT * FROM buku ORDER BY id_buku ASC').fetchall()

    conn.close()
    return render_template('admin.html', buku_list=buku_list, keyword=keyword)


# TAMBAH BUKU
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    error = None

    if request.method == 'POST':
        id_buku = request.form.get('id_buku', '').strip()
        judul_buku = request.form.get('judul_buku', '').strip()
        penerbit = request.form.get('penerbit', '').strip()

        if not id_buku or not judul_buku or not penerbit:
            error = 'Semua field wajib diisi.'
        else:
            conn = get_db_connection()
            cek = conn.execute('SELECT * FROM buku WHERE id_buku = ?', (id_buku,)).fetchone()

            if cek:
                error = 'ID Buku sudah ada. Gunakan ID lain.'
                conn.close()
            else:
                conn.execute(
                    'INSERT INTO buku (id_buku, judul_buku, penerbit) VALUES (?, ?, ?)',
                    (id_buku, judul_buku, penerbit)
                )
                conn.commit()
                conn.close()
                return redirect(url_for('admin'))

    return render_template('tambah.html', error=error)


# EDIT BUKU
@app.route('/edit/<id_buku>', methods=['GET', 'POST'])
def edit(id_buku):
    conn = get_db_connection()
    buku = conn.execute('SELECT * FROM buku WHERE id_buku = ?', (id_buku,)).fetchone()

    if buku is None:
        conn.close()
        return redirect(url_for('admin'))

    error = None

    if request.method == 'POST':
        judul_buku = request.form.get('judul_buku', '').strip()
        penerbit = request.form.get('penerbit', '').strip()

        if not judul_buku or not penerbit:
            error = 'Judul dan penerbit wajib diisi.'
        else:
            conn.execute(
                'UPDATE buku SET judul_buku = ?, penerbit = ? WHERE id_buku = ?',
                (judul_buku, penerbit, id_buku)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))

    conn.close()
    return render_template('edit.html', buku=buku, error=error)


# HAPUS BUKU
@app.route('/hapus/<id_buku>', methods=['POST'])
def hapus(id_buku):
    conn = get_db_connection()
    conn.execute('DELETE FROM buku WHERE id_buku = ?', (id_buku,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))


# DETAIL BUKU
@app.route('/detail/<id_buku>')
def detail(id_buku):
    conn = get_db_connection()
    buku = conn.execute('SELECT * FROM buku WHERE id_buku = ?', (id_buku,)).fetchone()
    conn.close()

    if buku is None:
        return redirect(url_for('home'))

    return render_template('detail.html', buku=buku)


# RUN APP
if __name__ == '__main__':
    app.run(debug=True)