# Redmoon’s Library PRO

Redmoon’s Library PRO adalah website sistem informasi perpustakaan sederhana
*AI-assisted creation*

## Fitur
- Halaman utama menampilkan daftar buku
- Panel admin untuk mengelola data buku
- Tambah buku
- Edit buku
- Hapus buku
- Database otomatis dibuat saat aplikasi dijalankan

## Teknologi
- Python 3
- Flask
- SQLite
- Bootstrap 5
- Gunicorn (untuk deploy di Render)

## Struktur Data
Tabel `buku` memiliki field:
- `id`
- `judul`
- `penerbit`

## Cara Menjalankan di Lokal

### 1. Install dependency
```bash
pip install -r requirements.txt