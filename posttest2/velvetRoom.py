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
            if self.cek_skill_ada(skill_baru.nama, exclude_index=index):
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

class User:
    
    def __init__(self, nama, password, uang, status):
        self.nama = nama
        self.__password = password 
        self.uang = uang
        self.status = status

    def display_profile(self):
        """Method dasar yang bisa di-override"""
        print(f"Nama   : {self.nama}")
        print(f"Uang   : {self.uang}")
        print(f"Status : {'Admin' if self.status == 1 else 'Player'}")

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


class Player(User):
   
    def __init__(self, nama, password, uang=10000, fusion_count=0):
        self.fusion_count = fusion_count
        super().__init__(nama, password, uang, status=2)

        self.inventory_persona = []
        self.inventory_skill = []

    def display_profile(self):
        super().display_profile()
        print(f"total fusion dilakukan : {self.fusion_count}")

    def lihat_inventory(self):
        if not self.inventory_persona:
            print("Kamu belum punya persona apa-apa")
            return
        for i, p in enumerate(self.inventory_persona):
            p.display_info(tampilkan_harga=False)

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
                self.fusion_count += 1
                for idx in sorted([index1, index2], reverse=True):
                    self.inventory_persona.pop(idx)
                return True
        print("Nomor yang dipilih tidak valid")
        return False

    def update_skill_persona(self, index_persona, index_skill, skill_baru):
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
        if 0 <= index < len(self.inventory_persona):
            removed = self.inventory_persona.pop(index)
            print(f"Persona {removed.nama} berhasil dihapus")
            return True
        print("Nomor persona tidak ada")
        return False

class Admin(User):

    def __init__(self, nama, password, uang=999999, persona_dibuat=0):
        self.persona_dibuat = persona_dibuat
        super().__init__(nama, password, uang, status=1)

    def display_profile(self):
        super().display_profile()
        print(f"total persona dibuat : {self.persona_dibuat}")

    def lihat_semua_persona(self, daftar_persona):
        if not daftar_persona:
            print("Tidak ada persona yang bisa dibaca")
            return
        for i, p in enumerate(daftar_persona):
            p.display_info(tampilkan_harga=True)

    def tambah_persona(self, daftar_persona, persona_baru):
        for p in daftar_persona:
            if p.nama.lower() == persona_baru.nama.lower():
                print("Gagal: Nama persona sudah ada!")
                return False
        daftar_persona.append(persona_baru)
        self.persona_dibuat += 1
        print(f"Data persona '{persona_baru.nama}' berhasil dimasukkan")
        return True

    def update_persona(self, daftar_persona, index, atribut, nilai_baru):
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
    "baisudi": Skill("Baisudi", "Menyembuhkan status penyakit ringan", 0),
    "sukukaja": Skill("Sukukaja", "Meningkatkan Hit/Evade 1 anggota tim", 0),
    "holy arrow": Skill("Holy Arrow", "Serangan sihir elemen Bless dengan peluang efek Charm", 0),
    "apt pupil": Skill("Apt Pupil", "Meningkatkan peluang serangan Kritis", 0)
}

personaUtama = [
    Persona("Orpheus", 10, "Fool", 500, [daftar_skill["agi"], daftar_skill["dia"], daftar_skill["bash"], daftar_skill["tarunda"]]),
    Persona("Jack o Lantern", 15, "Magician", 750, [daftar_skill["bufu"], daftar_skill["pulinpa"], daftar_skill["mabufu"], daftar_skill["shock punch"], daftar_skill["freeze boost"], daftar_skill["magic boost"]]),
    Persona("Archangel", 20, "Justice", 1000, [daftar_skill["kouha"], daftar_skill["single shot"], daftar_skill["baisudi"], daftar_skill["sukukaja"], daftar_skill["holy arrow"], daftar_skill["apt pupil"]])
]

print("=== TEST INHERITANCE ===")

admin1 = Admin("Igor", "444", 999999)
player1 = Player("joljora", "038", 10000)

print("\n--- tes ubah password (warisan dari superclass user) ---")
admin1.ubah_password("444", "igor_secret")
player1.ubah_password("038", "ozora123")


print("\n--- test method dari sublclass admin ---")
admin1.lihat_semua_persona(personaUtama)
pixie = Persona("Pixie", 2, "Lovers", 300, [daftar_skill["dia"], daftar_skill["agi"]])
admin1.tambah_persona(personaUtama, pixie)

print("\n--- test method dari subclass player ---")
player1.beli_persona(personaUtama[0])
player1.beli_persona(personaUtama[1])
player1.lihat_inventory()


player1.display_profile()
print("\n")
admin1.display_profile()