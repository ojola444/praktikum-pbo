import copy

class Skill:
    def __init__(self, nama, deskripsi="", harga=0):
        self.nama = nama
        self.deskripsi = deskripsi
        self.__harga = harga 

    @property
    def harga(self):
        return self.__harga

    @harga.setter
    def harga(self, nilai_baru):
        if nilai_baru < 0:
            raise ValueError("Harga tidak boleh negatif")
        self.__harga = nilai_baru

    def display_info(self):
        info = f"    - {self.nama}"
        if self.deskripsi:
            info += f" ({self.deskripsi})"
        if self.__harga > 0:
            info += f" [Harga: {self.__harga}]"
        print(info)


class Persona:
    def __init__(self, nama, level, arcana, harga, skills=None):
        self.nama = nama
        self.level = level
        self.arcana = arcana
        self.harga = harga
        self.skills = skills if skills is not None else []

    def display_info(self, tampilkan_harga=True):
      
        print(f"\n====== {self.nama} ======")
        print(f"Level  : {self.level}")
        print(f"Arcana : {self.arcana}")
        print("Skills :", end=" ")
        if self.skills:
            print(", ".join(s.nama for s in self.skills))
        else:
            print("Tidak ada")
        if tampilkan_harga:
            print(f"Harga  : {self.harga}")

    def cek_skill_ada(self, nama_skill, exclude_index=-1):
        for i, skill in enumerate(self.skills):
            if i == exclude_index:
                continue
            if skill.nama.lower() == nama_skill.lower():
                return True
        return False

    def tambah_skill(self, skill_obj):
        if len(self.skills) >= 8:
            print("Skill sudah penuh (maksimal 8)")
            return False
        if self.cek_skill_ada(skill_obj.nama):
            print(f"Skill '{skill_obj.nama}' sudah ada di persona ini")
            return False
        self.skills.append(skill_obj)
        return True

    def update_skill(self, index, skill_baru):
        
        if 0 <= index < len(self.skills):
            if (self.cek_skill_ada(skill_baru.nama, exclude_index=index)):
                print(f"Skill '{skill_baru.nama}' sudah ada di persona ini")
                return False
            self.skills[index] = skill_baru
            return True
        print("Index skill tidak valid")
        return False


    def hapus_skill(self, index):
        if 0 <= index < len(self.skills):
            return self.skills.pop(index)
        return None

    @staticmethod
    def bubble_sort_nama(daftar_persona, ascending=True):
        n = len(daftar_persona)
        for i in range(n - 1):
            swapped = False
            for j in range(n - i - 1):
                condition = (
                    daftar_persona[j].nama.lower() > daftar_persona[j + 1].nama.lower()
                    if ascending
                    else daftar_persona[j].nama.lower() < daftar_persona[j + 1].nama.lower()
                )
                if condition:
                    daftar_persona[j], daftar_persona[j + 1] = daftar_persona[j + 1], daftar_persona[j]
                    swapped = True
            if not swapped:
                break
    


class User:

    def __init__(self, nama, password, uang=10000):
        self.nama = nama
        self.__password = password 
        self.uang = uang
        self.status = 2
        self.inventory_persona = []
        self.inventory_skill = []

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password_baru):
        
        if len(password_baru) < 3:
            raise ValueError("Password minimal 3 karakter")
        self.__password = password_baru

    def ubah_password(self, password_lama, password_baru):
        
        if self.__password != password_lama:
            print("Password lama salah!")
            return False
        try:
            self.password = password_baru  # Memanggil @setter di atas
            print("Password berhasil diubah!")
            return True
        except ValueError as e:
            print(f"Gagal: {e}")
            return False

    def lihat_inventory(self):

        if not self.inventory_persona:
            print("Kamu belum punya persona apa-apa")
            return
        for i, p in enumerate(self.inventory_persona):
            p.display_info(tampilkan_harga=False)  # User biasa tidak lihat harga

    def beli_persona(self, persona_obj):
        
        if self.uang >= persona_obj.harga:
            self.uang -= persona_obj.harga
            persona_copy = copy.deepcopy(persona_obj)
            self.inventory_persona.append(persona_copy)
            print(f"Berhasil membeli {persona_obj.nama}! Sisa uang: {self.uang}")
            return True
        else:
            print("Uang tidak cukup!")
            return False

    def fuse_persona(self, index1, index2, daftar_persona_global):
        
        if len(self.inventory_persona) < 2:
            print("Tidak ada persona yang bisa digabung (Minimal 2)")
            return False

        if (0 <= index1 < len(self.inventory_persona) and
            0 <= index2 < len(self.inventory_persona) and
            index1 != index2):

            lvl1 = self.inventory_persona[index1].level
            lvl2 = self.inventory_persona[index2].level
            target_level = (lvl1 + lvl2) // 2 + 1

            terdekat = None
            min_diff = float('inf')
            for p in daftar_persona_global:
                diff = abs(p.level - target_level)
                if diff < min_diff:
                    min_diff = diff
                    terdekat = p

            if terdekat:
                self.inventory_persona.append(copy.deepcopy(terdekat))
                print(f"Fusion berhasil! Mendapatkan: {terdekat.nama}")

                for idx in sorted([index1, index2], reverse=True):
                    self.inventory_persona.pop(idx)
                return True

        print("Nomor yang dipilih tidak valid")
        return False

    def update_skill_persona(self, index_persona, index_skill, skill_baru):
        """
        Menggantikan updateSkillUser()
        Mengubah skill pada persona tertentu di inventory.
        """
        if 0 <= index_persona < len(self.inventory_persona):
            persona = self.inventory_persona[index_persona]
            if not persona.skills:
                print("Persona ini tidak memiliki skill")
                return False
            if persona.update_skill(index_skill, skill_baru):
                print("Pembaruan skill berhasil!")
                return True
        else:
            print("Nomor persona tidak ada")
        return False

    def hapus_persona(self, index):
        """Menggantikan hapusPersonaUser()"""
        if 0 <= index < len(self.inventory_persona):
            removed = self.inventory_persona.pop(index)
            print(f"Persona {removed.nama} berhasil dihapus")
            return True
        print("Nomor persona tidak ada")
        return False


class Admin:
    """Admin (status 1). Bisa CRUD database persona global."""

    def __init__(self, nama, password, uang=999999):
        self.nama = nama
        self.__password = password
        self.uang = uang
        self.status = 1
        self.inventory_persona = []  
        self.inventory_skill = []

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password_baru):
        if len(password_baru) < 3:
            raise ValueError("Password minimal 3 karakter")
        self.__password = password_baru

    def ubah_password(self, password_lama, password_baru):
        if self.__password != password_lama:
            print("Password lama salah!")
            return False
        try:
            self.password = password_baru
            print("Password berhasil diubah!")
            return True
        except ValueError as e:
            print(f"Gagal: {e}")
            return False

    def lihat_semua_persona(self, daftar_persona):
        """Menggantikan lihatPersonaUtama()"""
        if not daftar_persona:
            print("Tidak ada persona yang bisa dibaca")
            return
        for i, p in enumerate(daftar_persona):
            p.display_info(tampilkan_harga=True)  # Admin bisa lihat harga

    def tambah_persona(self, daftar_persona, persona_baru):
       
        for p in daftar_persona:
            if p.nama.lower() == persona_baru.nama.lower():
                print("Gagal: Nama persona sudah ada!")
                return False
        daftar_persona.append(persona_baru)
        print(f"Data persona '{persona_baru.nama}' berhasil dimasukkan")
        return True

    def update_persona(self, daftar_persona, index, atribut, nilai_baru):
        """
        Menggantikan updatePersona()
        atribut bisa: "nama", "level", "arcana", "harga"
        Untuk update skill, gunakan Persona.update_skill() langsung.
        """
        if not (0 <= index < len(daftar_persona)):
            print("Nomor tidak valid")
            return False

        p = daftar_persona[index]

        if atribut == "nama":
            for i, existing in enumerate(daftar_persona):
                if i != index and existing.nama.lower() == nilai_baru.lower():
                    print("Gagal: Nama persona sudah ada!")
                    return False
            p.nama = nilai_baru
        elif atribut == "level":
            p.level = nilai_baru
        elif atribut == "arcana":
            p.arcana = nilai_baru
        elif atribut == "harga":
            p.harga = nilai_baru
        else:
            print("Atribut tidak dikenali")
            return False

        print("Berhasil diubah!")
        return True

    def hapus_persona(self, daftar_persona, index):
        if 0 <= index < len(daftar_persona):
            removed = daftar_persona.pop(index)
            print(f"Persona '{removed.nama}' berhasil dihapus")
            return True
        print("Tidak ada persona di nomor itu")
        return False

#objek bawaan untuk persona dan skillnya

daftar_skill = {
    "masukunda": Skill("Masukunda", "Menurunkan Defence seluruh musuh selama 3 giliran", 0),
    "dekaja": Skill("Dekaja", "Menghapus semua efek buff status pada seluruh musuh", 0),
    "debilitate": Skill("Debilitate", "Menurunkan Attack, Defence, dan Hit/Evade 1 musuh", 0),
    "charge": Skill("Charge", "Meningkatkan damage serangan fisik berikutnya sebesar 2.5x", 0),
    "concentrate": Skill("Concentrate", "Meningkatkan damage serangan sihir berikutnya sebesar 2.5x", 0),
    
    "agi": Skill("Agi", "Luka sihir elemen Api kecil ke 1 musuh", 0),
    "dia": Skill("Dia", "Memulihkan sedikit HP ke 1 anggota tim", 0),
    "bash": Skill("Bash", "Serangan fisik elemen Physical sedang ke 1 musuh", 0),
    "tarunda": Skill("Tarunda", "Menurunkan Attack 1 musuh selama 3 giliran", 0),
    "bufu": Skill("Bufu", "Luka sihir elemen Es kecil ke 1 musuh", 0),
    "pulinpa": Skill("Pulinpa", "Peluang menyebabkan status Panic/Confusion ke 1 musuh", 0),
    "mabufu": Skill("Mabufu", "Luka sihir elemen Es kecil ke seluruh musuh", 0),
    "shock punch": Skill("Shock Punch", "Serangan fisik dengan peluang menyebabkan status Shock", 0),
    "freeze boost": Skill("Freeze Boost", "Meningkatkan peluang memberikan status Freeze", 0),
    "magic boost": Skill("Magic Boost", "Meningkatkan damage semua serangan sihir sebesar 25%", 0),
    "kouha": Skill("Kouha", "Luka sihir elemen Bless/Light kecil ke 1 musuh", 0),
    "single shot": Skill("Single Shot", "Serangan fisik jarak jauh elemen Gun/Rifle", 0),
    "baisudi": Skill("Baisudi", "Menyembuhkan status penyakit ringan (Cure status ailments)", 0),
    "sukukaja": Skill("Sukukaja", "Meningkatkan Hit/Evade (kecepatan) 1 anggota tim", 0),
    "holy arrow": Skill("Holy Arrow", "Serangan sihir elemen Bless dengan peluang efek Charm", 0),
    "apt pupil": Skill("Apt Pupil", "Meningkatkan peluang serangan Kritis (Critical rate)", 0)
}


personaUtama = [
    Persona(
        nama="Orpheus", 
        level=10, 
        arcana="Fool", 
        harga=500, 
        skills=[
            daftar_skill["agi"],
            daftar_skill["dia"],
            daftar_skill["bash"],
            daftar_skill["tarunda"]
        ]
    ),
    Persona(
        nama="Jack o Lantern", 
        level=15, 
        arcana="Magician", 
        harga=750, 
        skills=[
            daftar_skill["bufu"],
            daftar_skill["pulinpa"],
            daftar_skill["mabufu"],
            daftar_skill["shock punch"],
            daftar_skill["freeze boost"],
            daftar_skill["magic boost"]
        ]
    ),
    Persona(
        nama="Archangel", 
        level=20, 
        arcana="Justice", 
        harga=1000, 
        skills=[
            daftar_skill["kouha"],
            daftar_skill["single shot"],
            daftar_skill["baisudi"],
            daftar_skill["sukukaja"],
            daftar_skill["holy arrow"],
            daftar_skill["apt pupil"]
        ]
    )
]

##### testing program #####

print("\n test method persona")
print("\n tampilkan data persona")
personaUtama[0].display_info()

print("\n")

print("cek skill persona apakah sudah ada di persona itu")
print(f"skill {daftar_skill['sukukaja'].nama} ada di persona {personaUtama[1].nama}? = {personaUtama[1].cek_skill_ada("sukukaja")}")

print("\n method tambah skill")
personaUtama[2].tambah_skill(daftar_skill["holy arrow"])

print("\n method update skill")
personaUtama[1].update_skill(3, daftar_skill["concentrate"])

print("\n method hapus skill")
personaUtama[1].hapus_skill(5)

print("\n static method sorting persona")
Persona.bubble_sort_nama(personaUtama)
personaUtama[0].display_info()
personaUtama[1].display_info()

print("\n test method skill")
#test ubah atribute private dengan decorator
daftar_skill["debilitate"].harga = 1000

print("\n methode menampilkan info tentang skill yang dipilih")
daftar_skill["debilitate"].display_info()

# Objek Admin
admin1 = Admin("Igor", "444", 999999)
admin2 = Admin("Margaret", "888", 500000)

# Objek User
user1 = User("joljora", "038", 10000)
user2 = User("Makoto", "123", 150)


print("\n test method admin")
print(f"\n--- Admin 1: {admin1.nama} ---")

# method mengubah password
admin1.ubah_password("444", "igor_secret")  

# method melihat semua persona global
admin1.lihat_semua_persona(personaUtama)

# method tambah persona globa baru
pixie = Persona("Pixie", 2, "Lovers", 300, [daftar_skill["dia"], daftar_skill["agi"]])
admin1.tambah_persona(personaUtama, pixie)

# method update persona global
admin1.update_persona(personaUtama, index=0, atribut="harga", nilai_baru=600)  

# method 
admin1.hapus_persona(personaUtama, index=1)  # Menghapus persona index ke-1

# cek semua persona setelah perubahan
admin1.lihat_semua_persona(personaUtama)


# test ubah password kalau password lama salah
admin2.ubah_password("password_salah", "999") 


print("\n test method user")
print(f"\n user 1: {user1.nama} ")

print("\n method ubah password ")
user1.ubah_password("038", "ozora123")

print("\n method lihat invetory")
user1.lihat_inventory()

print("\n method beli persona ")
user1.beli_persona(personaUtama[0]) 
user1.beli_persona(personaUtama[1]) 

print("\n test lihat inventory (setelah beli)")
user1.lihat_inventory()

print("\n method update skill persona(di inventory)")
user1.update_skill_persona(index_persona=0, index_skill=0, skill_baru=daftar_skill["charge"])

print("\n method gabungkan 2 persona untuk cari persona baru")
user1.fuse_persona(index1=0, index2=1, daftar_persona_global=personaUtama)
user1.lihat_inventory()

print("\n method hapus persona dari inventory")
user1.hapus_persona(index=0)
user1.lihat_inventory()

print(f"\n user 2: {user2.nama}")

print("\n test beli persona kalo uangnya dikit")
user2.beli_persona(personaUtama[0])  # Uang awal 1500, harga misal > 1500

