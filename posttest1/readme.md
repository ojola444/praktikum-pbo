# Persona Management System (Persona 3 Concept)

Sistem manajemen Persona berbasis Python yang menerapkan konsep *Object-Oriented Programming* (OOP). Program ini mengimplementasikan pengelolaan entity **Persona**, **Skill**, **User**, serta **Admin** yang memiliki hak akses berbeda.

---

##  Penjelasan Program

Program ini mensimulasikan sistem manajemen item/entitas dari gim Persona.
1. **Pemain (User)** dapat membeli Persona dari *global database*, mengelola skill pada Persona milik mereka, serta menggabungkan dua Persona (*Persona Fusion*) untuk mendapatkan Persona baru berdasarkan kalkulasi rata-rata level.
2. **Pengelola (Admin)** dapat mengelola database Persona global seperti menambah, mengubah atribut, dan menghapus Persona.
3. **Encapsulation & Validation** diterapkan pada atribut sensitif seperti `harga` skill dan `password` akun.

---

##  Struktur Class


| Class | Deskripsi Utama | Atribut Kunci | Method Utama |
| :--- | :--- | :--- | :--- |
| `Skill` | Merepresentasikan skill/kemampuan yang dimiliki Persona. | `nama`, `deskripsi`, `__harga` *(private)* | `@harga.setter`, `display_info()` |
| `Persona` | Entitas Persona yang menyimpan sekumpulan `Skill`. | `nama`, `level`, `arcana`, `harga`, `skills` | `tambah_skill()`, `update_skill()`, `hapus_skill()`, `bubble_sort_nama()` *(static)* |
| `User` | Pengguna biasa yang dapat membeli dan menggabungkan Persona. | `nama`, `__password`, `uang`, `inventory_persona` | `beli_persona()`, `fuse_persona()`, `update_skill_persona()`, `ubah_password()` |
| `Admin` | Pengelola dengan akses penuh terhadap daftar Persona global. | `nama`, `__password`, `status=1` | `tambah_persona()`, `update_persona()`, `hapus_persona()`, `lihat_semua_persona()` |

---

##  Panduan Pengujian Singkat

Pengujian dapat dilakukan langsung dengan menjalankan berkas `testing.py`.

### 1. Jalankan Pengujian
Buka terminal/command prompt dan jalankan perintah:
```bash
python testing.py
```

### 2. Skenario Pengujian Utama

| Kategori Test | Aksi yang Diuji | Hasil yang Diharapkan |
| :--- | :--- | :--- |
| **Skill & Encapsulation** | Mengubah `harga` skill ke nilai negatif | Mengembalikan `ValueError: Harga tidak boleh negatif`. |
| **Persona Skills** | Menambah skill yang sama / melebihi limit 8 | Muncul pesan *warning* skill duplicate atau limit penuh. |
| **Admin Operations** | Menambah, update atribut, dan hapus Persona global | Database Persona global terbarui secara *real-time*. |
| **User Purchase** | Membeli Persona dengan uang yang tidak cukup | Transaksi ditolak dengan pesan `Uang tidak cukup!`. |
| **Persona Fusion** | Menggabungkan 2 Persona dari inventory | Memunculkan Persona baru berlevel paling mendekati $\lfloor \frac{\text{Lvl}_1 + \text{Lvl}_2}{2} \rfloor + 1$. |

---