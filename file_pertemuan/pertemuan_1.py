# class Nasabah :
#     def __init__(self, nama, nomor_rekening):
#         self.nama = nama
#         self.nomor_rekening = nomor_rekening

#     def tarik_tunai(self, atm, jumlah):
#         atm.saldo_kas -= jumlah


# class MesinAtm:
#     def __init__(self, id_atm, lokasi, saldo_kas):
#         self.id_atm = id_atm
#         self.lokasi = lokasi
#         self.saldo_kas = saldo_kas

# dapa = Nasabah("dapa", 676767)
# atm_pusat = MesinAtm("pusat", "samarinda", 400000000)

# dapa.tarik_tunai(atm_pusat, 10000000)

# print(atm_pusat.saldo_kas)

class bank :
    def __init__(self, nama_bank, kode):
        self.karyawan = []
        self.nama_bank = nama_bank
        self.kode = kode

    def tambah_karyawan(self, karyawan) :
        self.karyawan.append(karyawan)


class karyawan :
    def __init__(self, nama, nip, posisi):
        self.nama = nama
        self.nip = nip
        self.posisi = posisi

Bank = bank('bcaIhsan', 123)
karyawanBaru = karyawan("orang", 122, "promosi")

Bank.tambah_karyawan(karyawanBaru)

print(Bank.karyawan[0].nama)