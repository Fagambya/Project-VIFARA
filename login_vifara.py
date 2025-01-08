import sys
import os
import random
import pandas as pd

def bersih():
    os.system('cls' if os.name == 'nt' else 'clear')

#variabel global, untuk verifikasi user sedang login atau tidak.
#deklarasi diluar fungsi dan bisa diakses oleh seluruh fungsi
login_status = False

#===============================================================================
# Data Handling
#===============================================================================

#Untuk pengecekan userid agar tidak duplikat
def validasi_userid(userid, data):
    return not data['userid'].astype(str).str.contains(str(userid)).any() #Mengembalikan nilai True apabila tidak ada kecocokan

#Untuk pengecekan username agar tidak duplikat
def validasi_username(username, data):
    return not data['username'].astype(str).str.contains(str(username)).any() #Mengembalikan nilai True apabila tidak ada kecocokan

#Untuk memberikan userid acak pada saat register
def generate_userid():
    return str(random.randint(10000000, 99999999))


#===============================================================================
# Isi Proses
#===============================================================================

#login
def login():
    global login_status
    while True:
        print("\n===== SISTEM LOGIN =====")
        try:
            data = pd.read_csv('users.csv')
        except FileNotFoundError:
            print(" ❌ File users.csv tidak ditemukan!")
            return False
        
        username = input(' ✨ Username / ID\t: ')
        password = input(' 🔑 Password\t\t: ')
        user = data[
            ((data['username'] == username) & (data['password'] == password)) |
            ((data['userid'].astype(str) == username) & (data['password'] == password))
        ]

        # Digunakan untuk memeriksa apakah dataframe user tidak kosong
        # Jika terpenuhi maka akan membuat dictionary yang akan dicocokkan users.csv
        if not user.empty:
            user_data = {
                'username': user.iloc[0]['username'],
                'userid': user.iloc[0]['userid'],
                'nama': user.iloc[0]['nama'],
                'role': user.iloc[0]['role']
            }


            login_status = True
            bersih()
            print(' ✅ Login berhasil ! ')
            return user_data
        else:
            bersih()
            print(' ❌ Username / Password Tidak Sesuai!')
            input(' Tekan Enter untuk mencoba lagi...')


#REGISTRASI PEGAWAI
def register():
    while True:
        bersih()
        print("\n===== SISTEM REGISTRASI =====")
        try:
            data = pd.read_csv('users.csv')
        except FileNotFoundError:
            print(" ❌ File users.csv tidak ditemukan!")
            return False

        # Input dan validasi username
        while True:
            username = input(' ✨ Username\t\t: ')
            if len(username) < 2:
                print(" ❌ Username minimal 2 karakter!")
                continue
            if not validasi_username(username, data):
                print(" ❌ Username sudah digunakan!")
                continue
            break

        while True:
            userid = generate_userid()
            if not validasi_userid(userid, data):
                continue
            break
        print(f' 📋 User ID\t\t: {userid}')


        # Input dan validasi password
        while True:
            password = input(' 🔑 Password\t\t: ')
            if len(password) < 1:
                print(" ❌ Password minimal 1 karakter!")
                continue
            confirm_password = input(' 🔄 Confirm Password:\t: ')
            if password != confirm_password:
                print(" ❌ Password tidak cocok!")
                continue
            break

        # Input nama
        nama = input(' 👤 Nama\t\t: ')

        # Membuat dictionary untuk data baru
        new_user = {
            'username': [username],
            'userid': [userid],
            'password': [password],
            'nama': [nama],
            'role': ["pegawai"]
        }

        # Menambahkan data baru ke DataFrame
        new_df = pd.DataFrame(new_user)
        data = pd.concat([data, new_df], ignore_index=True)

        # Menyimpan ke file CSV
        try:
            data.to_csv('users.csv', index=False)
            bersih()
            print(" ✅ Registrasi berhasil!")
            input('klik enter untuk kembali')
            return True
        except Exception as error:
            print(f" ❌ Terjadi kesalahan saat menyimpan data: {str(error)}")
            return False

# registrasi buat role ADMIN
def register_admin():
    while True:
        bersih()
        print("\n===== SISTEM REGISTRASI =====")
        try:
            data = pd.read_csv('users.csv')
        except FileNotFoundError:
            print(" ❌ File users.csv tidak ditemukan!")
            return False

        # Input dan validasi username
        while True:
            username = input(' ✨ Username\t\t: ')
            if len(username) < 2:
                print(" ❌ Username minimal 2 karakter!")
                continue
            if not validasi_username(username, data):
                print(" ❌ Username sudah digunakan!")
                continue
            break

        while True:
            userid = generate_userid()
            if not validasi_userid(userid, data):
                continue
            break
        print(f' 📋 User ID\t\t: {userid}')


        # Input dan validasi password
        while True:
            password = input(' 🔑 Password\t\t: ')
            if len(password) < 1:
                print(" ❌ Password minimal 1 karakter!")
                continue
            confirm_password = input(' 🔄 Confirm Password:\t: ')
            if password != confirm_password:
                print(" ❌ Password tidak cocok!")
                continue
            break

        # Input nama
        nama = input(' 👤 Nama\t\t: ')

        # Input dan validasi role
        while True:
            print (" 👥 Role\t\t:\n\t1. pegawai\t2. admin")
            pilihan_role = input(' 👥 Pilih role [1 / 2]\t: ')
            if pilihan_role == '1':
                role = 'pegawai'
            elif pilihan_role == '2':
                role = 'admin'
            else:
                print(" ❌ Pilihan tidak valid! Harap pilih 1 atau 2.")
                continue
            break

        # Membuat dictionary untuk data baru
        new_user = {
            'username': [username],
            'userid': [userid],
            'password': [password],
            'nama': [nama],
            'role': [role]
        }

        # Menambahkan data baru ke DataFrame
        new_df = pd.DataFrame(new_user)
        data = pd.concat([data, new_df], ignore_index=True)

        # Menyimpan ke file CSV
        try:
            data.to_csv('users.csv', index=False)
            bersih()
            print(" ✅ Registrasi berhasil!")
            return True
        except Exception as error:
            print(f" ❌ Terjadi kesalahan saat menyimpan data: {str(error)}")
            return False

#LOGOUT
def logout():
    # Mengakses variabel global untuk verifikasi login
    global login_status
    if login_status:
        login_status = False
        bersih()
        print(' ✅ Logout berhasil!')
        return True
    else:
        print(' ❌ Anda belum login!')
        return False

#ABOUT VIFARA
def about():
    menu = """
    ## Tentang Aplikasi VIFARA

    VIFARA adalah solusi inovatif untuk industri bioskop di era digital. Aplikasi ini menawarkan pemesanan tiket terpadu, pemilihan kursi real-time, dan pengecekan jadwal tayang yang mudah. 

    Nikmati layanan food & beverages, serta fasilitas tambahan seperti penyewaan bantal dan selimut untuk pengalaman menonton yang nyaman dan menyenangkan.

    Dengan VIFARA, Anda mendapatkan pengalaman hiburan yang berkualitas dan efisien, menjadikan setiap tayangan film momen yang tak terlupakan.
    """
    print(menu)
    input("Tekan Enter untuk kembali ke Menu Login")