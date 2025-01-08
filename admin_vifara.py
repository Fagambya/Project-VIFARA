import pandas as pd
import login_vifara as lovi
import os
from tabulate import tabulate


def bersih():
    os.system('cls' if os.name == 'nt' else 'clear')

#====================================================
# BUAT DISPLAY KURSI
#====================================================
def generate_kursi(studio):
    #Membuat tampilan kursi bioskop berdasarkan Studio
    if studio == 'Studio 1':
        rows = 'ABCDEFGH'
        cols = range(1, 11)  # 10 kursi per baris
    elif studio == 'Studio 2':
        rows = 'ABCDEF'  # 6 baris
        cols = range(1, 11)
    else:
        return []

   #membuat tata letak kursi
    seat_layout = []
    for row in rows:
        row_seats = [f'{row}{col}' for col in cols]
        seat_layout.append(row_seats)

    return seat_layout

def cek_kursi_terpakai(film, jam, studio):
    # Untuk memeriksa kursi yang sudah dipesan
    try:
        df_tiket = pd.read_csv('Data Rekap.csv')
        kursi_terpakai = df_tiket[
            (df_tiket['film'] == film) & 
            (df_tiket['jam'] == jam) & 
            (df_tiket['studio'] == studio)
        ]['kursi'].tolist()
        return kursi_terpakai
    except FileNotFoundError:
        return []

def display_kursi(seat_layout, kursi_terpakai):
    # Menampilkan kursi dalam format kisi
    print("\nDenah Kursi:")
    print("    " + " ".join(f"{i:2}" for i in range(1, 11)))
    print("   " + "---" * 10)

    # menampilkan kursi pada posisi aslinya
    for row_num, row in enumerate(seat_layout):
        print(f"{chr(65 + row_num)} |", end=" ")
        for seat in row:
            if seat in kursi_terpakai:
                print(f" {seat} ", end=" ")  # Kursi terpakai (tanpa tanda [])
            else:
                print(f"[{seat}]", end=" ")  # Kursi tersedia
        print()

    print("\nKeterangan:")
    print("\t[]\t= Kursi tersedia")
    print("Kursi tanpa []  = Kursi terpakai")


#====================================================
## BUAT VALIDASI JADWAL
#====================================================
def check_jadwal_conflict(df, studio, jam_tayang):
    # Konversi jam_tayang ke datetime untuk perbandingan
    waktu_baru = pd.to_datetime(jam_tayang, format='%H:%M').time()
    
    # Filter jadwal untuk studio yang sama
    jadwal_studio = df[df['Studio'] == studio]
    
    # Diasumsikan setiap film memakan waktu 2 jam
    DURASI_FILM = pd.Timedelta(hours=2)
    
    for _, jadwal in jadwal_studio.iterrows():
        waktu_existing = pd.to_datetime(jadwal['Jam Tayang'], format='%H:%M').time()
        waktu_existing_dt = pd.to_datetime(waktu_existing.strftime('%H:%M'))
        waktu_baru_dt = pd.to_datetime(waktu_baru.strftime('%H:%M'))
        
        # Periksa apakah jadwal baru tabrakan dengan jadwal yang ada
        if abs(waktu_existing_dt - waktu_baru_dt) < DURASI_FILM:
            return True, jadwal['Film'], jadwal['Jam Tayang']
    
    return False, None, None

#====================================================
# UNTUK MENGUBAH DATA KARYAWAN DAN MANAGEMENT
#====================================================

def data_karyawan():
    while True:
        bersih()
        try:
            # Membaca file users.csv
            df = pd.read_csv('users.csv')
            
            # Memfilter pegawai
            pegawai_df = df[df['role'] == 'pegawai'].reset_index(drop=True)
            
            # Buat Tampilan
            display_df = pegawai_df.copy()
            display_df.index = range(1, len(display_df) + 1)  # Memulai index dari 1
            
            # Membuat tampilan tabulate
            print("\n=== MANAJEMEN DATA KARYAWAN ===\n")
            print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))
            
            print("\nMenu:")
            print("1. Hapus Karyawan")
            print("2. Tambah Karyawan")
            print("3. Kembali ke Menu Utama")

            
            pilihan = input("\nPilih menu [1-2]: ")
            
            if pilihan == "1":
                if len(pegawai_df) == 0:
                    input("\nTidak ada karyawan yang dapat dihapus. Tekan Enter untuk kembali...")
                    continue
                    
                while True:
                    try:
                        index = int(input("\nMasukkan nomor karyawan yang akan dihapus: "))
                        if 1 <= index <= len(pegawai_df):  # Disesuaikan index
                            # Dapatkan nama pengguna karyawan yang dipilih (sesuaikan indeks dengan -1)
                            username_to_delete = pegawai_df.iloc[index-1]['username']
                            
                            # Konfirmasi Hapus
                            konfirmasi = input(f"\nYakin hapus karyawan {username_to_delete}? (ya/tidak): ").lower()
                            
                            if konfirmasi == 'ya':
                                # Menghapus karyawan dari data frame / tabulate
                                df = df[df['username'] != username_to_delete]
                                
                                # Menyimpan ke csv
                                df.to_csv('users.csv', index=False)
                                print("\n✅ Karyawan berhasil dihapus!")
                                input("Tekan Enter untuk melanjutkan...")
                                break
                            else:
                                print("\nPenghapusan dibatalkan.")
                                input("Tekan Enter untuk melanjutkan...")
                                break
                        else:
                            print("\n❌ Nomor karyawan tidak valid!")
                            input("Tekan Enter untuk mencoba lagi...")
                    except ValueError:
                        print("\n❌ Masukkan angka yang valid!")
                        input("Tekan Enter untuk mencoba lagi...")

            elif pilihan == "2":
                lovi.register_admin()
                return True
                        
            elif pilihan == "3":
                bersih()
                break
            else:
                print("\n❌ Pilihan tidak valid!")
                input("Tekan Enter untuk mencoba lagi...")
                
        except FileNotFoundError:
            print("\n❌ File users.csv tidak ditemukan!")
            input("Tekan Enter untuk kembali...")
            break
        except Exception as error:
            print(f"\n❌ Terjadi kesalahan: {str(error)}")
            input("Tekan Enter untuk kembali...")
            break

#setting jadwal
def setting_jadwal():
    while True:
        bersih()
        try:
            # Membaca file csv
            df = pd.read_csv('jadwal_bioskop.csv')
            
            # Buat tampilan
            display_df = df.copy()
            display_df.index = range(1, len(display_df) + 1)
            
            # Display data in tabulate format
            print("\n=== MANAJEMEN JADWAL FILM ===\n")
            print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))
            
            print("\nMenu:")
            print("1. Tambah Jadwal Film")
            print("2. Hapus Jadwal Film")
            print("3. Ubah Harga Film")
            print("4. Kembali ke Menu Utama")
            
            pilihan = input("\nPilih menu [1-4]: ")
            
            if pilihan == "1":
                print("\n=== TAMBAH JADWAL FILM ===")
                film = input("Masukkan nama film: ")
                
                # Memilih studio
                while True:
                    print("\nPilih Studio:")
                    print("1. Studio 1")
                    print("2. Studio 2")
                    studio_pilihan = input("Masukkan pilihan studio [1-2]: ")
                    
                    if studio_pilihan in ["1", "2"]:
                        studio = f"Studio {studio_pilihan}"
                        break
                    print("\n❌ Pilihan studio tidak valid!")
                
                # Jam tayang validation
                while True:
                    jam_tayang = input("Masukkan jam tayang (HH:MM): ")
                    try:
                        pd.to_datetime(jam_tayang, format='%H:%M')
                        
                        # pengecekan tabrakan film
                        conflict, existing_film, existing_time = check_jadwal_conflict(df, studio, jam_tayang)
                        
                        if conflict:
                            print(f"\n❌ Jadwal bertabrakan dengan film {existing_film} pada jam {existing_time}")
                            print("Silakan pilih jam tayang lain!")
                            continue
                        
                        break
                    except ValueError:
                        print("\n❌ Format jam tidak valid! Gunakan format HH:MM")
                
                # Harga validation
                while True:
                    try:
                        harga = int(input("Masukkan harga tiket: "))
                        if harga > 0:
                            break
                        print("\n❌ Harga harus lebih dari 0!")
                    except ValueError:
                        print("\n❌ Masukkan angka yang valid!")
                
                # Add new schedule
                new_row = pd.DataFrame({
                    'Film': [film],
                    'Studio': [studio],
                    'Jam Tayang': [jam_tayang],
                    'harga': [harga]
                })
                
                df = pd.concat([df, new_row], ignore_index=True)
                # sortir berdasarkan studio dan jam
                df = df.sort_values(['Studio', 'Jam Tayang']).reset_index(drop=True)
                df.to_csv('jadwal_bioskop.csv', index=False)
                
                print("\n✅ Jadwal film berhasil ditambahkan!")
                input("Tekan Enter untuk melanjutkan...")
            
            elif pilihan == "2":
                
                if len(df) == 0:
                    input("\nTidak ada jadwal film yang dapat dihapus. Tekan Enter untuk kembali...")
                    continue
                
                while True:
                    print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))
                    try:
                        index = int(input("\nMasukkan nomor jadwal film yang akan dihapus: "))
                        if 1 <= index <= len(df):
                            schedule_to_delete = df.iloc[index-1]
                            
                            konfirmasi = input(
                                f"\nYakin hapus jadwal film {schedule_to_delete['Film']} "
                                f"di {schedule_to_delete['Studio']} "
                                f"pukul {schedule_to_delete['Jam Tayang']}? (ya/tidak): "
                            ).lower()
                            
                            if konfirmasi == 'ya':
                                df = df.drop(df.index[index-1]).reset_index(drop=True)
                                df.to_csv('jadwal_bioskop.csv', index=False)
                                print("\n✅ Jadwal film berhasil dihapus!")
                                input("Tekan Enter untuk melanjutkan...")
                                break
                            else:
                                print("\nPenghapusan dibatalkan.")
                                input("Tekan Enter untuk melanjutkan...")
                                break
                        else:
                            print("\n❌ Nomor jadwal film tidak valid!")
                    except ValueError:
                        print("\n❌ Masukkan angka yang valid!")

            elif pilihan == "3":
                if len(df) == 0:
                    input("\nTidak ada jadwal film yang dapat diubah. Tekan Enter untuk kembali...")
                    continue
                
                while True:
                    try:
                        # Group by Film to show unique films and their current prices
                        film_prices = df[['Film', 'harga']].drop_duplicates()
                        film_prices.index = range(1, len(film_prices) + 1)
                        
                        print("\n=== DAFTAR HARGA FILM ===")
                        print(tabulate(film_prices, headers='keys', tablefmt='grid', showindex=True))
                        
                        index = int(input("\nMasukkan nomor film yang akan diubah harganya: "))
                        if 1 <= index <= len(film_prices):
                            film_to_update = film_prices.iloc[index-1]['Film']
                            current_price = film_prices.iloc[index-1]['harga']
                            
                            print(f"\nFilm: {film_to_update}")
                            print(f"Harga saat ini: Rp {current_price}")
                            
                            new_price = int(input("Masukkan harga baru: "))
                            if new_price > 0:
                                # Update all instances of the film
                                df.loc[df['Film'] == film_to_update, 'harga'] = new_price
                                df.to_csv('jadwal_bioskop.csv', index=False)
                                print("\n✅ Harga film berhasil diubah!")
                                input("Tekan Enter untuk melanjutkan...")
                                break
                            else:
                                print("\n❌ Harga harus lebih dari 0!")
                        else:
                            print("\n❌ Nomor film tidak valid!")
                    except ValueError:
                        print("\n❌ Masukkan angka yang valid!")
                        input("Tekan Enter untuk mencoba lagi...")
            
            elif pilihan == "4":
                break
            else:
                print("\n❌ Pilihan tidak valid!")
                input("Tekan Enter untuk mencoba lagi...")
                
        except FileNotFoundError:
            print("\n❌ File jadwal_bioskop.csv tidak ditemukan!")
            input("Tekan Enter untuk kembali...")
            break
        except Exception as error:
            print(f"\n❌ Terjadi kesalahan: {str(error)}")
            input("Tekan Enter untuk kembali...")
            break

#untuk membooking kursi dengan nama admin
def setting_kursi():
    while True:
        bersih()
        
        print("\n=== MANAJEMEN KURSI ===")
        print("1. Booking Kursi oleh Admin")
        print("2. Ubah Kursi Pengunjung")
        print("3. Kembali ke Menu Utama")
        
        pilihan = input("\nPilih menu [1-3]: ")
        
        if pilihan == "1":
            # Original booking functionality remains the same
            # Membaca data jadwal film
            df_jadwal = pd.read_csv('jadwal_bioskop.csv')
            if df_jadwal.empty:
                print("\n❌ Tidak ada jadwal film yang tersedia.")
                input("Tekan Enter untuk kembali...")
                continue
            
            # Menampilkan jadwal untuk pemilihan
            print("\n=== PILIH JADWAL FILM ===\n")
            print(tabulate(df_jadwal, headers='keys', tablefmt='grid', showindex=True))
            
            # Memilih jadwal film
            index_jadwal = int(input("\nMasukkan nomor jadwal film yang akan dibooking: ")) - 1
            if 0 <= index_jadwal < len(df_jadwal):
                film = df_jadwal.iloc[index_jadwal]['Film']
                studio = df_jadwal.iloc[index_jadwal]['Studio']
                jam_tayang = df_jadwal.iloc[index_jadwal]['Jam Tayang']
                
                # Mengambil denah kursi
                seat_layout = generate_kursi(studio)
                kursi_terpakai = cek_kursi_terpakai(film, jam_tayang, studio)
                
                # Menampilkan denah kursi
                display_kursi(seat_layout, kursi_terpakai)
                
                # Memilih kursi untuk dibooking
                while True:
                    kursi = input("\nMasukkan nomor kursi yang akan dibooking (Klik Enter untuk selesai): ").upper()
                    if not kursi:
                        break
                    if kursi in kursi_terpakai:
                        print("\n❌ Kursi sudah dibooking! Pilih kursi lain.")
                    elif kursi not in [seat for row in seat_layout for seat in row]:
                        print("\n❌ Kursi tidak valid! Cek kembali nomor kursi.")
                    else:
                        # Menyimpan data booking ke dalam Data Rekap.csv
                        ticket_data = {
                            'nama': 'Admin',  # Nama admin yang melakukan booking
                            'film': film,
                            'jam': jam_tayang,
                            'studio': studio,
                            'kursi': kursi,
                            'harga': 0,
                            'harga_makan':0,
                            'harga_fasilitas':0,
                            'total_harga':0
                        }
                        
                        # Cek apakah file sudah ada, jika tidak buat baru
                        try:
                            df_tiket = pd.read_csv('Data Rekap.csv')
                        except FileNotFoundError:
                            df_tiket = pd.DataFrame(columns=ticket_data.keys())
                        
                        # Menambahkan data booking
                        df_tiket = pd.concat([df_tiket, pd.DataFrame([ticket_data])], ignore_index=True)
                        df_tiket.to_csv('Data Rekap.csv', index=False)
                        
                        print(f"\n✅ Kursi {kursi} berhasil dibooking untuk film {film}!")
                        kursi_terpakai.append(kursi)  # Update daftar kursi terpakai
                        display_kursi(seat_layout, kursi_terpakai)
        
        elif pilihan == "2":
            # Ubah Kursi Pengunjung
            try:
                # Baca Data Rekap
                df_tiket = pd.read_csv('Data Rekap.csv')
                
                if df_tiket.empty:
                    print("\n❌ Tidak ada tiket yang tersedia untuk diubah.")
                    input("Tekan Enter untuk kembali...")
                    continue
                
                # Tampilkan daftar tiket yang bisa diubah
                print("\n=== DAFTAR TIKET ===")
                display_df = df_tiket.copy()
                display_df.index = range(1, len(display_df) + 1)
                print(tabulate(display_df[['nama', 'film', 'jam', 'studio', 'kursi']], 
                               headers='keys', tablefmt='grid', showindex=True))
                
                # Pilih tiket untuk diubah
                while True:
                    try:
                        index = int(input("\nMasukkan nomor tiket yang akan diubah kursinya: ")) - 1
                        
                        if 0 <= index < len(df_tiket):
                            # Ambil detail tiket yang dipilih
                            tiket = df_tiket.iloc[index]
                            
                            # Generate seat layout untuk studio yang sesuai
                            seat_layout = generate_kursi(tiket['studio'])
                            
                            # Cek kursi yang sudah terpakai untuk film dan jam tersebut
                            kursi_terpakai = cek_kursi_terpakai(
                                tiket['film'], 
                                tiket['jam'], 
                                tiket['studio']
                            )
                            
                            # Hapus kursi saat ini dari daftar kursi terpakai
                            kursi_terpakai.remove(tiket['kursi'])
                            
                            # Tampilkan denah kursi
                            print(f"\nMengubah kursi untuk {tiket['nama']} - {tiket['film']}")
                            display_kursi(seat_layout, kursi_terpakai)
                            
                            # Pilih kursi baru
                            while True:
                                kursi_baru = input("\nMasukkan nomor kursi baru: ").upper()
                                
                                if kursi_baru in kursi_terpakai:
                                    print("\n❌ Kursi sudah dibooking! Pilih kursi lain.")
                                elif kursi_baru not in [seat for row in seat_layout for seat in row]:
                                    print("\n❌ Kursi tidak valid! Cek kembali nomor kursi.")
                                else:
                                    # Update kursi dalam DataFrame
                                    df_tiket.loc[index, 'kursi'] = kursi_baru
                                    
                                    # Simpan perubahan
                                    df_tiket.to_csv('Data Rekap.csv', index=False)
                                    
                                    print(f"\n✅ Kursi berhasil diubah dari {tiket['kursi']} menjadi {kursi_baru}")
                                    input("Tekan Enter untuk melanjutkan...")
                                    break
                            
                            break
                        else:
                            print("\n❌ Nomor tiket tidak valid!")
                    
                    except ValueError:
                        print("\n❌ Masukkan angka yang valid!")
            
            except FileNotFoundError:
                print("\n❌ File Data Rekap.csv tidak ditemukan!")
                input("Tekan Enter untuk kembali...")
        
        elif pilihan == "3":
            bersih()
            break
        
        else:
            print("\n❌ Pilihan tidak valid!")
            input("Tekan Enter untuk mencoba lagi...")

#untuk merubah stock makanan yang disediakan
def stock_makanan():
    while True:
        bersih()
        try:
            # Read the CSV file
            df = pd.read_csv('makanan.csv')
            
            # Create display dataframe with clean numbering
            display_df = df.copy()
            display_df.index = range(1, len(display_df) + 1)
            
            # Display data in tabulate format
            print("\n=== MANAJEMEN STOCK MAKANAN DAN MINUMAN ===\n")
            print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))
            
            print("\nMenu:")
            print("1. Tambah Stock")
            print("2. Kurangi Stock")
            print("3. Tambah Menu Baru")
            print("4. Hapus Menu")
            print("5. Kembali ke Menu Utama")
            
            pilihan = input("\nPilih menu [1-5]: ")
            
            if pilihan in ["1", "2"]:
                if len(df) == 0:
                    input("\nTidak ada makanan/minuman yang terdaftar. Tekan Enter untuk kembali...")
                    continue
                    
                while True:
                    try:
                        index = int(input("\nMasukkan nomor makanan/minuman: "))
                        if 1 <= index <= len(df):
                            menu = df.iloc[index-1]
                            print(f"\nMenu yang dipilih: {menu['Nama Menu']}")
                            print(f"Stock saat ini: {menu['Stok']}")
                            
                            try:
                                jumlah = int(input("Masukkan jumlah yang akan " + 
                                                 ("ditambahkan: " if pilihan == "1" else "dikurangi: ")))
                                
                                if jumlah < 0:
                                    print("\n❌ Jumlah tidak boleh negatif!")
                                    input("Tekan Enter untuk mencoba lagi...")
                                    continue
                                
                                if pilihan == "2" and jumlah > menu['Stok']:
                                    print("\n❌ Stock tidak mencukupi!")
                                    input("Tekan Enter untuk mencoba lagi...")
                                    continue
                                
                                # Update stock
                                new_stock = menu['Stok'] + jumlah if pilihan == "1" else menu['Stok'] - jumlah
                                df.loc[index-1, 'Stok'] = new_stock
                                
                                # Save changes to CSV
                                df.to_csv('makanan.csv', index=False)
                                
                                print(f"\n✅ Stock berhasil {'ditambahkan' if pilihan == '1' else 'dikurangi'}!")
                                print(f"Stock baru: {new_stock}")
                                input("Tekan Enter untuk melanjutkan...")
                                break
                                
                            except ValueError:
                                print("\n❌ Masukkan angka yang valid!")
                                input("Tekan Enter untuk mencoba lagi...")
                                
                        else:
                            print("\n❌ Nomor menu tidak valid!")
                            input("Tekan Enter untuk mencoba lagi...")
                            
                    except ValueError:
                        print("\n❌ Masukkan angka yang valid!")
                        input("Tekan Enter untuk mencoba lagi...")

            elif pilihan == "3":
                print("\n=== TAMBAH MENU BARU ===")
                try:
                    # Get the last index and create new ID
                    new_id = len(df) + 1
                    
                    nama_menu = input("Masukkan nama menu: ")
                    while True:
                        try:
                            harga = int(input("Masukkan harga menu: "))
                            if harga <= 0:
                                print("\n❌ Harga harus lebih dari 0!")
                                continue
                            break
                        except ValueError:
                            print("\n❌ Masukkan angka yang valid!")
                    
                    while True:
                        try:
                            stok = int(input("Masukkan jumlah stok awal: "))
                            if stok < 0:
                                print("\n❌ Stok tidak boleh negatif!")
                                continue
                            break
                        except ValueError:
                            print("\n❌ Masukkan angka yang valid!")
                    
                    # Add new menu
                    new_menu = pd.DataFrame({
                        'IDProduct': [new_id],
                        'Nama Menu': [nama_menu],
                        'Harga': [harga],
                        'Stok': [stok]
                    })
                    
                    df = pd.concat([df, new_menu], ignore_index=True)
                    df.to_csv('makanan.csv', index=False)
                    
                    print("\n✅ Menu baru berhasil ditambahkan!")
                    input("Tekan Enter untuk melanjutkan...")
                    
                except Exception as e:
                    print(f"\n❌ Terjadi kesalahan: {str(e)}")
                    input("Tekan Enter untuk kembali...")

            elif pilihan == "4":
                if len(df) == 0:
                    input("\nTidak ada menu yang dapat dihapus. Tekan Enter untuk kembali...")
                    continue
                
                while True:
                    try:
                        index = int(input("\nMasukkan nomor menu yang akan dihapus: "))
                        if 1 <= index <= len(df):
                            menu = df.iloc[index-1]
                            
                            # Confirm deletion
                            konfirmasi = input(f"\nYakin hapus menu {menu['Nama Menu']}? (ya/tidak): ").lower()
                            
                            if konfirmasi == 'ya':
                                # Delete the menu
                                df = df.drop(df.index[index-1])
                                
                                # Reset IDProduct to maintain sequence
                                df['IDProduct'] = range(1, len(df) + 1)
                                
                                # Save changes to CSV
                                df.to_csv('makanan.csv', index=False)
                                print("\n✅ Menu berhasil dihapus!")
                                input("Tekan Enter untuk melanjutkan...")
                                break
                            else:
                                print("\nPenghapusan dibatalkan.")
                                input("Tekan Enter untuk melanjutkan...")
                                break
                        else:
                            print("\n❌ Nomor menu tidak valid!")
                            input("Tekan Enter untuk mencoba lagi...")
                    except ValueError:
                        print("\n❌ Masukkan angka yang valid!")
                        input("Tekan Enter untuk mencoba lagi...")
                        
            elif pilihan == "5":
                bersih()
                break
            else:
                print("\n❌ Pilihan tidak valid!")
                input("Tekan Enter untuk mencoba lagi...")
                
        except FileNotFoundError:
            print("\n❌ File makanan.csv tidak ditemukan!")
            input("Tekan Enter untuk kembali...")
            break
        except Exception as error:
            print(f"\n❌ Terjadi kesalahan: {str(error)}")
            input("Tekan Enter untuk kembali...")
            break

#untuk merubah stock fasilitas yang disediakan
def stock_fasilitas():
    while True:
        bersih()
        try:
            # Read the CSV file
            df = pd.read_csv('fasilitas.csv')
            
            # Create display dataframe with clean numbering
            display_df = df.copy()
            display_df.index = range(1, len(display_df) + 1)
            
            # Display data in tabulate format
            print("\n=== MANAJEMEN STOCK FASILITAS ===\n")
            print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))
            
            print("\nMenu:")
            print("1. Tambah Stock")
            print("2. Kurangi Stock")
            print("3. Tambah Fasilitas Baru")
            print("4. Hapus Fasilitas")
            print("5. Kembali ke Menu Utama")
            
            pilihan = input("\nPilih menu [1-5]: ")
            
            if pilihan in ["1", "2"]:
                if len(df) == 0:
                    input("\nTidak ada fasilitas yang terdaftar. Tekan Enter untuk kembali...")
                    continue
                    
                while True:
                    try:
                        index = int(input("\nMasukkan nomor fasilitas: "))
                        if 1 <= index <= len(df):
                            produk = df.iloc[index-1]
                            print(f"\nFasilitas yang dipilih: {produk['namaproduk']}")
                            print(f"Stock saat ini: {produk['stock']}")
                            
                            try:
                                jumlah = int(input("Masukkan jumlah yang akan " + 
                                                 ("ditambahkan: " if pilihan == "1" else "dikurangi: ")))
                                
                                if jumlah < 0:
                                    print("\n❌ Jumlah tidak boleh negatif!")
                                    input("Tekan Enter untuk mencoba lagi...")
                                    continue
                                
                                if pilihan == "2" and jumlah > produk['stock']:
                                    print("\n❌ Stock tidak mencukupi!")
                                    input("Tekan Enter untuk mencoba lagi...")
                                    continue
                                
                                # Update stock
                                new_stock = produk['stock'] + jumlah if pilihan == "1" else produk['stock'] - jumlah
                                df.loc[index-1, 'stock'] = new_stock
                                
                                # Save changes to CSV
                                df.to_csv('fasilitas.csv', index=False)
                                
                                print(f"\n✅ Stock berhasil {'ditambahkan' if pilihan == '1' else 'dikurangi'}!")
                                print(f"Stock baru: {new_stock}")
                                input("Tekan Enter untuk melanjutkan...")
                                break
                                
                            except ValueError:
                                print("\n❌ Masukkan angka yang valid!")
                                input("Tekan Enter untuk mencoba lagi...")
                                
                        else:
                            print("\n❌ Nomor fasilitas tidak valid!")
                            input("Tekan Enter untuk mencoba lagi...")
                            
                    except ValueError:
                        print("\n❌ Masukkan angka yang valid!")
                        input("Tekan Enter untuk mencoba lagi...")

            elif pilihan == "3":
                print("\n=== TAMBAH FASILITAS BARU ===")
                try:
                    # Get the last index and create new ID
                    new_id = len(df) + 1
                    
                    nama_fasilitas = input("Masukkan nama fasilitas: ")
                    harga_produk = input('Masukkan harga produk:')
                    while True:
                        try:
                            stok = int(input("Masukkan jumlah stok awal: "))
                            if stok < 0:
                                print("\n❌ Stok tidak boleh negatif!")
                                continue
                            break
                        except ValueError:
                            print("\n❌ Masukkan angka yang valid!")
                    
                    # Add new facility
                    new_fasilitas = pd.DataFrame({
                        'id product': [new_id],
                        'namaproduk': [nama_fasilitas],
                        'harga produk': [harga_produk],
                        'stock': [stok]
                    })
                    
                    df = pd.concat([df, new_fasilitas], ignore_index=True)
                    df.to_csv('fasilitas.csv', index=False)
                    
                    print("\n✅ Fasilitas baru berhasil ditambahkan!")
                    input("Tekan Enter untuk melanjutkan...")
                    
                except Exception as e:
                    print(f"\n❌ Terjadi kesalahan: {str(e)}")
                    input("Tekan Enter untuk kembali...")

            elif pilihan == "4":
                if len(df) == 0:
                    input("\nTidak ada fasilitas yang dapat dihapus. Tekan Enter untuk kembali...")
                    continue
                
                while True:
                    try:
                        index = int(input("\nMasukkan nomor fasilitas yang akan dihapus: "))
                        if 1 <= index <= len(df):
                            produk = df.iloc[index-1]
                            
                            # Confirm deletion
                            konfirmasi = input(f"\nYakin hapus fasilitas {produk['namaproduk']}? (ya/tidak): ").lower()
                            
                            if konfirmasi == 'ya':
                                # Delete the facility
                                df = df.drop(df.index[index-1])
                                
                                # Reset idproduct to maintain sequence
                                df['id product'] = range(1, len(df) + 1)
                                
                                # Save changes to CSV
                                df.to_csv('fasilitas.csv', index=False)
                                print("\n✅ Fasilitas berhasil dihapus!")
                                input("Tekan Enter untuk melanjutkan...")
                                break
                            else:
                                print("\nPenghapusan dibatalkan.")
                                input("Tekan Enter untuk melanjutkan...")
                                break
                        else:
                            print("\n❌ Nomor fasilitas tidak valid!")
                            input("Tekan Enter untuk mencoba lagi...")
                    except ValueError:
                        print("\n❌ Masukkan angka yang valid!")
                        input("Tekan Enter untuk mencoba lagi...")
                        
            elif pilihan == "5":
                bersih()
                break
            else:
                print("\n❌ Pilihan tidak valid!")
                input("Tekan Enter untuk mencoba lagi...")
                
        except FileNotFoundError:
            print("\n❌ File fasilitas.csv tidak ditemukan!")
            input("Tekan Enter untuk kembali...")
            break
        except Exception as error:
            print(f"\n❌ Terjadi kesalahan: {str(error)}")
            input("Tekan Enter untuk kembali...")
            break

#untuk mengecek laporan keuangan dari data rekap, pesan makanan, pesan fasilitas
def laporan_keuangan():
    while True:
        bersih()
        try:
            # Read all CSV files
            df_tiket = pd.read_csv('Data Rekap.csv')
            df_makanan = pd.read_csv('data pesan makanan.csv')
            df_fasilitas = pd.read_csv('data pesan fasilitas.csv')
            
            print("\n=== LAPORAN KEUANGAN ===\n")
            
            # Calculate total income from tickets
            total_tiket = df_tiket['harga'].sum()
            
            # Calculate total income from food
            total_makanan = df_makanan['total_bayar'].sum()
            
            # Calculate total income from facilities
            total_fasilitas = df_fasilitas['total_bayar'].sum()
            
            # Calculate grand total
            grand_total = total_tiket + total_makanan + total_fasilitas
            
            # Display summary
            print("Rincian Pendapatan:")
            print(f"1. Penjualan Tiket    : Rp {total_tiket:,}")
            print(f"2. Penjualan Makanan  : Rp {total_makanan:,}")
            print(f"3. Penyewaan Fasilitas: Rp {total_fasilitas:,}")
            print("-" * 40)
            print(f"Total Pendapatan      : Rp {grand_total:,}")
            
            print("\nMenu:")
            print("1. Lihat Detail Penjualan Tiket")
            print("2. Lihat Detail Penjualan Makanan")
            print("3. Lihat Detail Penyewaan Fasilitas")
            print("4. Kembali ke Menu Utama")
            
            pilihan = input("\nPilih menu [1-4]: ")
            
            if pilihan == "1":
                print("\n=== DETAIL PENJUALAN TIKET ===")
                # Group by film and calculate total sales
                detail_tiket = df_tiket.groupby('film')['harga'].agg(['count', 'sum']).reset_index()
                detail_tiket.columns = ['Film', 'Jumlah Tiket', 'Total Pendapatan']
                print(tabulate(detail_tiket, headers='keys', tablefmt='grid', showindex=False))
                input("\nTekan Enter untuk kembali...")
                
            elif pilihan == "2":
                print("\n=== DETAIL PENJUALAN MAKANAN ===")
                # Group by menu name and calculate total sales
                detail_makanan = df_makanan.groupby('nama_menu')['total_bayar'].agg(['count', 'sum']).reset_index()
                detail_makanan.columns = ['Menu', 'Jumlah Terjual', 'Total Pendapatan']
                print(tabulate(detail_makanan, headers='keys', tablefmt='grid', showindex=False))
                input("\nTekan Enter untuk kembali...")
                
            elif pilihan == "3":
                print("\n=== DETAIL PENYEWAAN FASILITAS ===")
                # Group by facility name and calculate total sales
                detail_fasilitas = df_fasilitas.groupby('nama_fasilitas')['total_bayar'].agg(['count', 'sum']).reset_index()
                detail_fasilitas.columns = ['Fasilitas', 'Jumlah Disewa', 'Total Pendapatan']
                print(tabulate(detail_fasilitas, headers='keys', tablefmt='grid', showindex=False))
                input("\nTekan Enter untuk kembali...")
                
            elif pilihan == "4":
                bersih()
                break
            else:
                print("\n❌ Pilihan tidak valid!")
                input("Tekan Enter untuk mencoba lagi...")
                
        except FileNotFoundError as e:
            print(f"\n❌ File tidak ditemukan: {str(e)}")
            input("Tekan Enter untuk kembali...")
            break

#untuk mengecek laporan pengunjung yang menonton film
def laporan_pengunjung():
    while True:
        bersih()
        try:
            # Membaca data dari CSV
            df = pd.read_csv('Data Rekap.csv')

            if df.empty:
                print("\n❌ Tidak ada data pengunjung yang tersedia.")
                input("Tekan Enter untuk kembali...")
                break

            # Menampilkan data dalam format tabel
            print("\n=== LAPORAN PENGUNJUNG ===\n")
            print(tabulate(df, headers='keys', tablefmt='grid', showindex=True))

            # Menampilkan total pengunjung
            total_pengunjung = len(df)
            print(f"\nTotal Pengunjung\t: {total_pengunjung}\n")
            
            input("Tekan Enter untuk kembali ke menu...")
            break

        except FileNotFoundError:
            print("\n❌ File Data Rekap.csv tidak ditemukan!")
            input("Tekan Enter untuk kembali...")
            break
        except Exception as error:
            print(f"\n❌ Terjadi kesalahan: {str(error)}")
            input("Tekan Enter untuk kembali...")
            break

