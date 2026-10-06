# Dokumentasi Relasi UML & Inheritance pada `velvetRoom.py`

Dokumen ini menjelaskan struktur class, relasi Unified Modeling Language (UML), serta penerapan konsep Object-Oriented Programming (OOP) khususnya **Inheritance (Pewarisan)** pada kode Python `velvetRoom.py`.

---

## 1. Ringkasan Konsep OOP yang Diterapkan

1. **Inheritance (Pewarisan)**: Mengizinkan class turunan (*subclass*) untuk mewarisi atribut dan method dari class induk (*superclass*).
2. **Encapsulation (Pengkapsulan)**: Menyembunyikan detail implementasi internal atribut (menggunakan `__` private attribute) dan menyediakan pemanggilan terkontrol via `@property` dan `@setter`.
3. **Method Overriding**: Mengubah perilaku method pada *subclass* yang telah didefinisikan sebelumnya di *superclass*.
4. **Aggregation / Composition**: Menggambarkan hubungan kepemilikan antar objek (misal: Persona memiliki Skill).

---

## 2. Analisis Class & Inheritance (Pewarisan)

#### A. Superclass: `User`
Class induk yang merepresentasikan atribut dan perilaku umum pengguna sistem.
* **Atribut Public**: `nama`, `uang`, `status`
* **Atribut Private**: `__password` (Diakses menggunakan `@property` dan `@password.setter` untuk validasi minimal 3 karakter)
* **Method**:
  * `display_profile()`: Menampilkan informasi dasar user.
  * `ubah_password(password_lama, password_baru)`: Memverifikasi dan mengubah password.

#### B. Subclass: `Player` (`class Player(User)`)
* **Inheritance**: Mewarisi seluruh atribut (`nama`, `uang`, `status`) dan method (`ubah_password`) dari `User`.
* **Super Call**: Memanggil `super().__init__(nama, password, uang, status=2)` untuk menginisialisasi atribut induk dengan status khusus Player (2).
* **Atribut Tambahan**: `fusion_count`, `inventory_persona`, `inventory_skill`.
* **Method Overriding**: `display_profile()` dipanggil menggunakan `super().display_profile()`, lalu ditambahi pencetakan `total fusion dilakukan`.
* **Spesifikasi Perilaku**: Memiliki fitur transaksi dan pengelolaan persona pribadi (`beli_persona`, `fuse_persona`, `update_skill_persona`, `hapus_persona`).

#### C. Subclass: `Admin` (`class Admin(User)`)
* **Inheritance**: Mewarisi seluruh atribut dan method dari `User`.
* **Super Call**: Memanggil `super().__init__(nama, password, uang, status=1)` dengan nilai `uang` *default* tinggi ($999.999$) dan `status` Admin (1).
* **Atribut Tambahan**: `persona_dibuat`.
* **Method Overriding**: `display_profile()` memanggil `super().display_profile()` lalu mencetak `total persona dibuat`.
* **Spesifikasi Perilaku**: Memiliki hak akses mengelola *database* persona global (`tambah_persona`, `update_persona`, `hapus_persona`, `lihat_semua_persona`).

---

## 3. Relasi UML Terperinci

Berikut adalah daftar relasi antar class yang terdapat di dalam program beserta penjelasannya:

| Class A | Relasi UML | Class B | Keterangan Relasi |
| :--- | :---: | :--- | :--- |
| **Player** | **Generalization** (*Inheritance*) | **User** | Player adalah seorang User (Is-A relationship). |
| **Admin** | **Generalization** (*Inheritance*) | **User** | Admin adalah seorang User (Is-A relationship). |
| **Persona** | **Aggregation** | **Skill** | Persona memiliki daftar objek `Skill` dalam list `skills`. Skill bisa berdiri sendiri tanpa tergantung satu Persona khusus. |
| **Player** | **Aggregation** | **Persona** | Player menyimpan kumpulan `Persona` di daftar `inventory_persona`. |

---



## 4. Bukti Penerapan dalam Kode (`velvetRoom.py`)

### A. Penggunaan `super().__init__()`
Mengalirkan data dari *subclass* ke *superclass*:
```python
class Player(User):
    def __init__(self, nama, password, uang=10000, fusion_count=0):
        self.fusion_count = fusion_count
        # Memanggil constructor milik User
        super().__init__(nama, password, uang, status=2) 
```

### B. Method Overriding fungsi superclass
`Player` dan `Admin` memanggil implementasi milik parent, lalu menambah fungsionalitasnya sendiri:
```python
def display_profile(self):
    super().display_profile() # Memanggil cetak nama, uang, status dari class User
    print(f"total fusion dilakukan : {self.fusion_count}") # Fitur khusus Player
```

### C. Pewarisan Method
Objek `admin1` dan `player1` dapat mengakses method `ubah_password()` yang ada pada class `User`, tanpa perlu mendefinisikan ulang method tersebut di dalam class `Admin` maupun `Player`:
```python
# Objek Admin & Player menggunakan method warisan dari User
admin1.ubah_password("444", "igor_secret")
player1.ubah_password("038", "ozora123")
```