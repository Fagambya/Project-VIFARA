import login_vifara as lovi
import admin_vifara as adiv
import pandas as pd
from tabulate import tabulate
import os

##======================================================================##

def bersih():
    os.system('cls' if os.name == 'nt' else 'clear')

##======================================================================##

def print_dashboard_banner():
    banner = """
╔══════════════════════════════════════════════════╗
║             🎬 VIFARA MOVIE THEATER 🎬           ║
╚══════════════════════════════════════════════════╝
    """
    print(banner)

def menu_dashboard_pegawai(user_data):
    print_dashboard_banner()
    print(f"\t🌕 Selamat Datang, {user_data['nama']} | [ {user_data['role']} ]")
    menu_pegawai = """
╔══════════════════════════════════════════════════╗
║                  MENU PEGAWAI                    ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  [1] 🎟️   Penjualan Tiket                         ║
║  [2] 🍟  Penjualan Makanan                       ║
║  [3] 📅  Jadwal Film                             ║
║  [4] 💺  Ketersediaan Kursi                      ║
║  [5] 🍜  Stock Makanan dan Minuman               ║
║  [6] 🛏   Stock Fasilitas                         ║
║  [7] 📋  Riwayat Transaksi                       ║
║  [8] 🚪  Logout                                  ║ 
║                                                  ║
╚══════════════════════════════════════════════════╝
"""
    print(menu_pegawai)
    pilih_menu_pegawai(user_data)

def menu_dashboard_admin(user_data):
    print_dashboard_banner()
    print(f"\t🌐 Selamat Datang, {user_data['nama']} | [ {user_data['role']} ]")
    menu_admin = """
╔══════════════════════════════════════════════════╗
║                   MENU ADMIN                     ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  [1] 👥  Manajemen Karyawan                      ║
║  [2] 📅  Manajemen Jadwal Film                   ║
║  [3] 💺  Manajemen Kursi                         ║
║  [4] 🍜  Manajemen Makanan                       ║
║  [5] 🛏   Manajemen fasilitas                     ║
║  [6] 💰  Laporan Keuangan                        ║
║  [7] 📊  Laporan Pengunjung                      ║
║  [8] 🚪  Logout                                  ║
║                                                  ║
╚══════════════════════════════════════════════════╝
"""
    print(menu_admin)
    pilih_menu_admin(user_data)

def pilih_menu_pegawai(user_data):
        pilihan = input("Pilih Menu [1-8]: ")
        match pilihan:
            case "1":
                penjualan_tiket()
            case "2":
                pesan_jajan()
            case "3":
                tampilkan_jadwal_film()
            case "4":
                cek_kursi()
            case "5":
                cek_stock_makanan()
            case "6":
                cek_stock_fasilitas()
            case "7":
                riwayat_transaksi()
            case "8":
                input("\nTekan Enter untuk kembali ke menu login...")
                lovi.logout()
                return
            case _:
                print("⚠️  Error: Pilihan tidak valid!")
                input("\nTekan Enter untuk mencoba lagi...")
                bersih()
                return True

def pilih_menu_admin(user_data):
        pilihan = input("Pilih Menu [1-8]: ")
        match pilihan:
            case "1":
                adiv.data_karyawan()
            case "2":
                adiv.setting_jadwal()
            case "3":
                adiv.setting_kursi()
            case "4":
                adiv.stock_makanan()
            case "5":
                adiv.stock_fasilitas()
            case "6":
                adiv.laporan_keuangan()
            case "7":
                adiv.laporan_pengunjung()
            case "8":
                lovi.logout()
                return
            case _:
                print("⚠️  Error: Pilihan tidak valid!")
                input("\nTekan Enter untuk mencoba lagi...")
                bersih()
                return True

def tampilkan_dashboard(user_data):
    if user_data['role'] == 'pegawai':
        menu_dashboard_pegawai(user_data)
        
    elif user_data['role'] == 'admin':
        menu_dashboard_admin(user_data)

##======================================================================##
# UNTUK GENERATE KURSI
##======================================================================##

def generate_kursi(studio):
    # untuk menghasilkan tampilan dari kursi berdasarkan studio
    if studio == 'Studio 1':
        rows = 'ABCDEFGHI'
        cols = range(1, 11)  # 10 kursi per baris
    elif studio == 'Studio 2':
        rows = 'ABCDEF'  # 6 baris
        cols = range(1, 11)
    else:
        return []

    # Membuat seat Layout
    seat_layout = []
    for row in rows:
        row_seats = [f'{row}{col}' for col in cols]
        seat_layout.append(row_seats)

    return seat_layout

def cek_kursi_terpakai(film, jam, studio):
    # Menampilkan kursi yang sudah dipesan pada data rekap.csv
    try:
        df_tiket = pd.read_csv('Data Rekap.csv')
        kursi_terpakai = df_tiket[
            (df_tiket['film'] == film) & 
            (df_tiket['jam'] == jam) & 
            (df_tiket['studio'] == studio)
        ]['kursi'].tolist() # kolom kursi diambil dan diubah menjadi daftar
        return kursi_terpakai
    except FileNotFoundError:
        return []

def display_kursi(seat_layout, kursi_terpakai):
    # Tampilan Grid atau batasan kursi
    print("\nDenah Kursi:")
    print("    " + " ".join(f"{i:2}" for i in range(1, 11)))
    print("   " + "---" * 10)

    # Menampilkan kursi pada posisi aslinya ( tidak bergeser )
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

##======================================================================##
## PENJUALAN TIKET
##======================================================================##

def penjualan_tiket():
    while True:
        bersih()
        try:
            df_jadwal = pd.read_csv('jadwal_bioskop.csv')
            display_df = df_jadwal.copy()
            display_df.index = range(1, len(display_df) + 1)

            print("\n=== PENJUALAN TIKET BIOSKOP ===\n")
            print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))

            while True:
                pilih_jadwal = int(input("\nPilih nomor jadwal film [1-{}]: ".format(len(display_df))))
                
                if 1 <= pilih_jadwal <= len(display_df):
                    jadwal_terpilih = display_df.iloc[pilih_jadwal - 1]

                    print("\n=== DETAIL TIKET ===")
                    print(f"Film\t\t: {jadwal_terpilih['Film']}")
                    print(f"Studio\t\t: {jadwal_terpilih['Studio']}")
                    print(f"Jam Tayang\t: {jadwal_terpilih['Jam Tayang']}")
                    print(f"Harga\t\t: Rp {jadwal_terpilih['harga']:,}")

                    konfirmasi = input("\nLanjutkan pembelian tiket?\n [1] Ya / [2] Tidak\t: ")

                    if konfirmasi == '1':
                        print("\n=== INFORMASI PEMBELI ===")
                        nama = input("Masukkan nama pembeli: ")

                        # Generate seat layout
                        seat_layout = generate_kursi(jadwal_terpilih['Studio'])
                        kursi_terpakai = cek_kursi_terpakai(
                            jadwal_terpilih['Film'], 
                            jadwal_terpilih['Jam Tayang'], 
                            jadwal_terpilih['Studio']
                        )

                        display_kursi(seat_layout, kursi_terpakai)

                        kursi_tersedia = [seat for row in seat_layout for seat in row if seat not in kursi_terpakai]

                        tiket_data = []
                        kursi_dipilih = []  # Track selected seats separately
                        harga_makan = 0  
                        harga_fasilitas = 0

                        while True:
                            kursi = input("\nMasukkan nomor kursi (Klik Enter [ Untuk Selesai ]): ").upper()
                            # if not kursi:
                            #     break

                            if kursi not in kursi_tersedia:
                                print("\n❌ Kursi tidak tersedia!")
                                continue
                            
                            # Untuk memperbarui daftar kursi
                            # Kursi yang dipilih dihapus dari kursi_tersedia, 
                            # ditambahkan ke kursi_terpakai, dan juga dicatat dalam kursi_dipilih.
                            kursi_tersedia.remove(kursi)
                            kursi_terpakai.append(kursi)
                            kursi_dipilih.append(kursi)  # Track selected seats
                            print(f"\n✅ Tiket untuk kursi {kursi} ditambahkan.")
                            display_kursi(seat_layout, kursi_terpakai)

                            if not kursi_tersedia:
                                print("\n⚠ Tidak ada kursi tersisa!")
                                break

                            tiket = {
                                'nama': nama,
                                'film': jadwal_terpilih['Film'],
                                'jam': jadwal_terpilih['Jam Tayang'],
                                'studio': jadwal_terpilih['Studio'],
                                'kursi': kursi,
                                'harga': jadwal_terpilih['harga'],
                                'harga_makan': harga_makan,
                                'harga_fasilitas': harga_fasilitas,
                                'total_harga': 0
                            }
                            tiket_data.append(tiket)
                            break

                        while True:
                            print("\n=== MENU TAMBAHAN ===")
                            print(" [1] Makanan")
                            print(" [2] Fasilitas")
                            print(" [3] Batal Pembelian")
                            print(" [4] Konfirmasi Pembelian")

                            lanjutkan = input("\nPilih Menu [1/2/3/4]: ")
                            match lanjutkan:
                                case "1":
                                    harga_makan = pesan_makanan(nama)
                                    for t in tiket_data:
                                        t['harga_makan'] = harga_makan

                                case "2":
                                    harga_fasilitas = pesan_fasilitas(nama)
                                    for t in tiket_data:
                                        t['harga_fasilitas'] = harga_fasilitas

                                case "3":
                                    print("\n=== PEMBATALAN TRANSAKSI ===")
                                    print("Detail yang akan dibatalkan:")
                                    print(f"Nama: {nama}")
                                    print(f"Film: {jadwal_terpilih['Film']}")
                                    print(f"Kursi: {', '.join(kursi_dipilih)}")
                                    
                                    konfirmasi_batal = input("\nAnda yakin ingin membatalkan? (ya/tidak): ").lower()
                                    if konfirmasi_batal == 'ya':
                                        # Mengembalikan tampilan kursi ke semula
                                        for kursi in kursi_dipilih:
                                            kursi_terpakai.remove(kursi)
                                            kursi_tersedia.append(kursi)
                                        
                                        # Apabila Makanan diorder, akan mengembalikan stok ke semula
                                        if harga_makan > 0:
                                            try:
                                                df_makanan = pd.read_csv('data pesan makanan.csv')
                                                df_makanan = df_makanan[df_makanan['nama'] != nama]
                                                df_makanan.to_csv('data pesan makanan.csv', index=False)
                                            except FileNotFoundError:
                                                pass

                                        # Jika fasilitas sudah dipesan, restore stock
                                        if harga_fasilitas > 0:
                                            try:
                                                df_fasilitas = pd.read_csv('data pesan fasilitas.csv')
                                                df_fasilitas = df_fasilitas[df_fasilitas['nama'] != nama]
                                                df_fasilitas.to_csv('data pesan fasilitas.csv', index=False)
                                            except FileNotFoundError:
                                                pass

                                        print("\n✅ Transaksi berhasil dibatalkan")
                                        input("\nTekan Enter untuk kembali ke menu utama...")
                                        return True
                                    else:
                                        print("\nPembatalan dibatalkan")
                                        continue

                                case "4":
                                    if tiket_data:
                                        # Update total_harga
                                        for t in tiket_data:
                                            total_harga = t['harga'] + t['harga_makan'] + t['harga_fasilitas']
                                            t['total_harga'] = total_harga

                                        df_tiket = pd.DataFrame(tiket_data)
                                        try:
                                            df_existing = pd.read_csv('Data Rekap.csv')
                                            df_final = pd.concat([df_existing, df_tiket], ignore_index=True)
                                        except FileNotFoundError:
                                            df_final = df_tiket

                                        df_final.to_csv('Data Rekap.csv', index=False)
                                        
                                        print("\n=== RINGKASAN PEMBELIAN ===")
                                        print(tabulate(df_tiket, headers='keys', tablefmt='grid', showindex=True))
                                        print(f"Nama\t: {nama}")
                                        # print(f"Film: {jadwal_terpilih['Film']}")
                                        # print(f"Kursi: {', '.join(kursi_dipilih)}")
                                        # print(f"Total Tiket: {len(tiket_data)}")
                                        total_bayar = sum(t['total_harga'] for t in tiket_data)
                                        print(f"Total Pembayaran: Rp {total_bayar:,}")
                                        input("\nTekan Enter untuk melanjutkan pembayaran...")
                                        proses_pembayaran(total_bayar)
                                        return True

                                case _:
                                    print("⚠️  Error: Pilihan tidak valid!")
                                    input("\nTekan Enter untuk mencoba lagi...")
                                    continue
                                
                    elif konfirmasi == '2':
                        break
                    else:
                        print("\n❌ Pilihan tidak valid!")
                        input("Tekan Enter untuk mencoba lagi...")
                
                else:
                    print("\n❌ Nomor jadwal tidak valid!")
                    input("Tekan Enter untuk mencoba lagi...")
        except ValueError as e:
            print(f"⚠️  Error: {e}")
            input("\nTekan Enter untuk mencoba lagi...")


            lanjut = input("\nIngin membeli tiket lagi? (ya/tidak): ").lower()
            if lanjut != 'ya':
                break

        except FileNotFoundError:
            print("\n❌ File jadwal_bioskop.csv tidak ditemukan!")
            input("Tekan Enter untuk kembali...")
            break

def pesan_makanan(nama_pelanggan):
    while True:
        bersih()
        try:
            # Baca menu makanan dari CSV
            df_makanan = pd.read_csv('makanan.csv')

            # Buat dataframe untuk menampilkan menu dengan nomor yang rapi
            display_df = df_makanan.copy()
            display_df.index = range(1, len(display_df) + 1)

            # Tampilkan menu makanan
            print("\n=== MENU MAKANAN & MINUMAN ===\n")
            print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))

            # Inisialisasi pesanan
            pesanan = []
            total_harga_makan = 0

            while True:
                try:
                    pilih_menu = input("\nPilih nomor menu [1-{}] (Klik Enter [Untuk Selesai]): ".format(len(display_df)))
                    
                    if pilih_menu == "":
                        break
                    
                    pilih_menu = int(pilih_menu)
                    if 1 <= pilih_menu <= len(display_df):
                        menu_terpilih = display_df.iloc[pilih_menu - 1]

                        if menu_terpilih['Stok'] <= 0:
                            print("\n❌ Maaf, stok habis!")
                            continue

                        while True:
                            try:
                                jumlah = int(input(f"Masukkan jumlah {menu_terpilih['Nama Menu']}: "))
                                if jumlah <= 0:
                                    print("\n❌ Jumlah harus lebih dari 0!")
                                    continue
                                if jumlah > menu_terpilih['Stok']:
                                    print(f"\n❌ Stok tidak mencukupi! Stok tersedia: {menu_terpilih['Stok']}")
                                    continue
                                break
                            except ValueError:
                                print("\n❌ Masukkan angka yang valid!")

                        # Hitung subtotal
                        subtotal = menu_terpilih['Harga'] * jumlah
                        total_harga_makan += subtotal

                        # Tambahkan ke daftar pesanan
                        pesanan.append({
                            'idproduct': menu_terpilih['IDProduct'],
                            'nama': nama_pelanggan,
                            'nama_menu': menu_terpilih['Nama Menu'],
                            'total pesan': jumlah,
                            'total_bayar': subtotal
                        })

                        # Kurangi stok di makanan.csv
                        df_makanan.loc[df_makanan['IDProduct'] == menu_terpilih['IDProduct'], 'Stok'] -= jumlah
                        df_makanan.to_csv('makanan.csv', index=False)

                        print(f"\n✅ {jumlah}x {menu_terpilih['Nama Menu']} ditambahkan ke pesanan")
                        print(f"Subtotal: Rp {subtotal:,}")

                    else:
                        print("\n❌ Nomor menu tidak valid!")

                except ValueError:
                    print("\n❌ Masukkan angka yang valid!")

            # Simpan pesanan ke data pesan makanan.csv jika ada pesanan
            if pesanan:
                try:
                    df_pesanan_existing = pd.read_csv('data pesan makanan.csv')
                    df_pesanan_new = pd.DataFrame(pesanan)
                    df_pesanan_final = pd.concat([df_pesanan_existing, df_pesanan_new], ignore_index=True)
                except FileNotFoundError:
                    df_pesanan_final = pd.DataFrame(pesanan)

                df_pesanan_final.to_csv('data pesan makanan.csv', index=False)

                # Tampilkan ringkasan pesanan
                print("\n=== RINGKASAN PESANAN ===")
                print(tabulate(pesanan, headers='keys', tablefmt='grid'))
                print(f"\nTotal Pembayaran: Rp {total_harga_makan:,}")
                return total_harga_makan

            input("\nTekan Enter untuk kembali ke menu...")
            break

        except FileNotFoundError:
            print("\n❌ File makanan.csv tidak ditemukan!")
            input("Tekan Enter untuk kembali...")
            break
        except Exception as error:
            print(f"\n❌ Terjadi kesalahan: {str(error)}")
            input("Tekan Enter untuk kembali...")
            break

def pesan_fasilitas(nama_pelanggan):
    while True:
        bersih()
        try:
            df_fasilitas = pd.read_csv('fasilitas.csv')
            
            # Membaca data pesanan yang sudah ada
            try:
                df_pesanan = pd.read_csv('data pesan fasilitas.csv')
            except FileNotFoundError:
                df_pesanan = pd.DataFrame(columns=['idproduct', 'nama', 'nama_fasilitas', 'total pesan', 'total_bayar'])
            
            # Membuat dataframe untuk menampilkan dengan nomor yang rapi
            display_df = df_fasilitas.copy()
            display_df.index = range(1, len(display_df) + 1)
            
            # Menampilkan menu fasilitas
            print("\n=== MENU FASILITAS ===\n")
            print(f"Pelanggan: {nama_pelanggan}\n")
            print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))
            
            # Inisialisasi pesanan
            pesanan = []
            
            while True:
                try:
                    pilih_item = input("\nPilih nomor item [1-{}] (Klik Enter [Untuk Selesai]): ".format(len(display_df)))
                    
                    if pilih_item == "":
                        break
                    
                    pilih_item = int(pilih_item)
                    if 1 <= pilih_item <= len(display_df):
                        item_terpilih = display_df.iloc[pilih_item-1]
                        
                        if item_terpilih['stock'] <= 0:
                            print("\n❌ Maaf, stok habis!")
                            continue
                        
                        while True:
                            try:
                                jumlah = int(input(f"Masukkan jumlah {item_terpilih['namaproduk']} (max {item_terpilih['stock']}): "))
                                if 1 <= jumlah <= item_terpilih['stock']:
                                    break
                                print("\n❌ Jumlah tidak valid!")
                            except ValueError:
                                print("\n❌ Masukkan angka yang valid!")
                        
                        # Menghitung subtotal
                        subtotal = jumlah * item_terpilih['harga produk']
                        
                        # Menambahkan ke daftar pesanan
                        pesanan.append({
                            'idproduct': item_terpilih['id product'],
                            'nama': nama_pelanggan,
                            'nama_fasilitas': item_terpilih['namaproduk'],
                            'total pesan': jumlah,
                            'total_bayar': subtotal
                        })
                        
                        # Mengurangi stok di dataframe
                        df_fasilitas.loc[df_fasilitas['id product']==pilih_item, 'stock'] -= jumlah
                        df_fasilitas.to_csv('fasilitas.csv', index=False)
                        
                        print(f"\n✅ {jumlah} {item_terpilih['namaproduk']} ditambahkan ke pesanan")

                    else:
                        print("\n❌ Nomor item tidak valid!")
                        
                except ValueError:
                    print("\n❌ Masukkan angka yang valid!")
            
                # Menyimpan pesanan ke file data pesan fasilitas.csv
                df_pesanan = pd.concat([df_pesanan, pd.DataFrame(pesanan)], ignore_index=True)
                df_pesanan.to_csv('data pesan fasilitas.csv', index=False)

            # Menampilkan ringkasan pesanan jika ada
            if pesanan:
                print("\n=== RINGKASAN PESANAN FASILITAS ===")
                print(tabulate(pesanan, headers='keys', tablefmt='grid'))
                
                total_harga = sum(item['total_bayar'] for item in pesanan)
                print(f"\nTotal Pembayaran: Rp {total_harga:,}")

                input("\nTekan Enter untuk melanjutkan...")
                return total_harga
            
            else:
                print("\nTidak ada item yang dipesan")
                input("\nTekan Enter untuk kembali...")
                return False
                
        except FileNotFoundError:
            print("\n❌ File fasilitas.csv tidak ditemukan!")
            input("Tekan Enter untuk kembali...")
            return False
        except Exception as error:
            print(f"\n❌ Terjadi kesalahan: {str(error)}")
            input("Tekan Enter untuk kembali...")
            return False

##======================================================================##
## FUNGSI UNTUK DASHBOARD PEGAWAI
##======================================================================##

def pesan_jajan():
    pesanan = []
    total_bayar = 0
    
    while True:
        bersih()
        print("\n=== PEMESANAN MAKANAN & MINUMAN ===\n")
        
        try:
            # Read menu data
            df_menu = pd.read_csv('makanan.csv')
            df_menu.index = range(1, len(df_menu) + 1)
            
            # Display menu
            print(tabulate(df_menu, headers='keys', tablefmt='grid', showindex=True))
            
            if not pesanan:
                # Mendapatkan nama pelanggan
                nama = input("\nMasukkan nama pembeli: ")
            
            while True:
                try:
                    pilihan = int(input("\nPilih nomor menu [Input 0 untuk ke menu Selanjutnya]: "))
                    
                    if pilihan == 0:
                        break
                        
                    if 1 <= pilihan <= len(df_menu):
                        menu_dipilih = df_menu.iloc[pilihan - 1]
                        jumlah = int(input(f"Jumlah {menu_dipilih['Nama Menu']}: "))

                    if menu_dipilih['Stok'] <= 0:
                        print("\n❌ Maaf, stok habis!")
                        continue
                        
                    if jumlah > 0:
                        subtotal = menu_dipilih['Harga'] * jumlah
                        
                        pesanan_item = {
                            'idproduct': menu_dipilih['IDProduct'],
                            'nama': nama,
                            'nama_menu': menu_dipilih['Nama Menu'],
                            'total pesan': jumlah,
                            'total_bayar': subtotal
                        }
                        
                        pesanan.append(pesanan_item)
                        total_bayar += subtotal
                        
                        print(f"\n✅ Pesanan ditambahkan: {menu_dipilih['Nama Menu']} x{jumlah}")
                    else:
                        print("\n❌ Jumlah harus lebih dari 0 !")
                        
                except ValueError:
                    print("\n❌ Masukkan angka yang valid!")
            
            if pesanan:
                while True:
                    bersih()
                    print("\n=== RINGKASAN PESANAN ===")
                    print(tabulate(pesanan, headers='keys', tablefmt='grid'))
                    print('Keterangan Pesanan :')
                    for idx, p in enumerate(pesanan, 1):
                        print(f"{idx}. {p['nama_menu']} x {p['total pesan']}\t: Rp {p['total_bayar']:,}")
                    print(f"\nTotal Pembayaran\t: Rp {total_bayar:,}")
                    
                    print("\n=== MENU OPSI ===")
                    print("[1] Pesan Makanan Kembali")
                    print("[2] Edit Pesanan")
                    print("[3] Konfirmasi Pesanan")
                    print("[4] Batalkan Pesanan")
                    
                    opsi = input("\nPilih opsi [1-4]: ")
                    
                    match opsi:
                        case "1":
                            break  # Kembali ke menu pemesanan
                        
                        case "2":
                            try:
                                idx_edit = int(input("\nMasukkan nomor pesanan yang ingin diedit: ")) - 1
                                if 0 <= idx_edit < len(pesanan):
                                    # Kurangi total sebelumnya
                                    total_bayar -= pesanan[idx_edit]['total_bayar']
                                    
                                    # Input jumlah baru
                                    jumlah_baru = int(input("Masukkan jumlah baru: "))
                                    if jumlah_baru <= 0:
                                        # Hapus pesanan
                                        pesanan.pop(idx_edit)
                                        print("\n✅ Pesanan dihapus!")
                                    else:
                                        # Update jumlah dan total bayar
                                        menu_harga = df_menu[df_menu.index == pesanan[idx_edit]['idproduct']]['Harga'].iloc[0]
                                        subtotal_baru = menu_harga * jumlah_baru
                                        
                                        pesanan[idx_edit]['total pesan'] = jumlah_baru
                                        pesanan[idx_edit]['total_bayar'] = subtotal_baru
                                        total_bayar += subtotal_baru
                                        
                                        print("\n✅ Pesanan berhasil diupdate!")
                                else:
                                    print("\n❌ Nomor pesanan tidak valid!")
                                input("\nTekan Enter untuk melanjutkan...")
                            except ValueError:
                                print("\n❌ Masukkan angka yang valid!")
                                input("\nTekan Enter untuk melanjutkan...")
                        
                        case "3":
                            try:
                                df_existing = pd.read_csv('data pesan makanan.csv')
                                df_pesanan = pd.DataFrame(pesanan)
                                df_final = pd.concat([df_existing, df_pesanan], ignore_index=True)
                            except FileNotFoundError:
                                df_final = pd.DataFrame(pesanan)
                            
                            df_final.to_csv('data pesan makanan.csv', index=False)
                            print("\n✅ Pesanan berhasil disimpan!")
                            proses_pembayaran(total_bayar)
                            return total_bayar
                        
                        case "4":
                            konfirmasi = input("\nYakin ingin membatalkan semua pesanan? (ya/tidak): ").lower()
                            if konfirmasi == 'ya':
                                print("\nPesanan dibatalkan.")
                                input("\nTekan Enter untuk kembali ke menu utama...")
                                return 0
                        
                        case _:
                            print("\n❌ Opsi tidak valid!")
                            input("\nTekan Enter untuk mencoba lagi...")
            else:
                lanjut = input("\nIngin memesan? (ya/tidak): ").lower()
                if lanjut != 'ya':
                    break
                
        except FileNotFoundError:
            print("\n❌ File menu tidak ditemukan!")
            input("Tekan Enter untuk kembali...")
            break
        except Exception as e:
            print(f"\n❌ Terjadi kesalahan: {str(e)}")
            input("Tekan Enter untuk kembali...")
            break
    
    return 0

def tampilkan_jadwal_film():
    while True:
        bersih()
        try:
            # Read the movie schedule CSV
            df_jadwal = pd.read_csv('jadwal_bioskop.csv')
            
            # Create display dataframe with clean numbering
            display_df = df_jadwal.copy()
            display_df.index = range(1, len(display_df) + 1)
            
            print("\n=== JADWAL FILM ===\n")
            print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))
            
            pilihan = input("\nTekan Enter untuk kembali ke menu...")
            break
            
        except FileNotFoundError:
            print("\n❌ File jadwal_bioskop.csv tidak ditemukan!")
            input("Tekan Enter untuk kembali...")
            break
        except Exception as error:
            print(f"\n❌ Terjadi kesalahan: {str(error)}")
            input("Tekan Enter untuk kembali...")
            break

def cek_kursi():
    """Fungsi untuk mengecek ketersediaan kursi berdasarkan data tiket yang sudah dipesan."""
    bersih()
    try:
        # Membaca data tiket dari file CSV
        df_tiket = pd.read_csv('Data Rekap.csv')

        # Memastikan ada data tiket yang tersedia
        if df_tiket.empty:
            print("❌ Tidak ada data tiket yang ditemukan!")
            input("Tekan Enter untuk kembali...")
            return

        # Menampilkan daftar film dan studio yang tersedia dari data tiket
        film_studio_unique = df_tiket[['film', 'studio']].drop_duplicates()
        print("\n=== DAFTAR FILM DAN STUDIO ===")
        print(tabulate(film_studio_unique, headers='keys', tablefmt='grid', showindex=True))

        # Meminta input pengguna untuk memilih film dan studio
        pilihan = input("\nMasukkan nomor film yang ingin dicek (1-{}): ".format(len(film_studio_unique)))
        try:
            pilihan = int(pilihan)
            if 1 <= pilihan <= len(film_studio_unique):
                film_pilih = film_studio_unique.iloc[pilihan - 1]['film']
                studio_pilih = film_studio_unique.iloc[pilihan - 1]['studio']
            else:
                print("❌ Pilihan tidak valid!")
                input("Tekan Enter untuk kembali...")
                return
        except ValueError:
            print("❌ Masukkan angka yang valid!")
            input("Tekan Enter untuk kembali...")
            return

        # Mengambil jam tayang dari data tiket yang dipilih
        jam_tayang = df_tiket[(df_tiket['film'] == film_pilih) & (df_tiket['studio'] == studio_pilih)]['jam'].values

        if len(jam_tayang) == 0:
            print("❌ Tidak ada jadwal untuk film dan studio yang dipilih!")
            input("Tekan Enter untuk kembali...")
            return

        # Mengecek kursi terpakai
        kursi_terpakai = cek_kursi_terpakai(film_pilih, jam_tayang[0], studio_pilih)

        # Menampilkan denah kursi
        seat_layout = generate_kursi(studio_pilih)

        # Menampilkan kursi yang terpakai
        display_kursi(seat_layout, kursi_terpakai)

        input("\nTekan Enter untuk kembali ke menu...")
        bersih()
        return

    except FileNotFoundError:
        print("❌ File Data Rekap.csv tidak ditemukan!")
        input("Tekan Enter untuk kembali...")
    except Exception as error:
        print(f"❌ Terjadi kesalahan: {str(error)}")
        input("Tekan Enter untuk kembali...")

def cek_stock_makanan():
    while True:
        bersih()
        try:
            # Read the food menu CSV
            df_makanan = pd.read_csv('makanan.csv')
            
            # Create display dataframe with clean numbering
            display_df = df_makanan.copy()
            display_df.index = range(1, len(display_df) + 1)
            
            # Display food menu with stock
            print("\n=== STOCK MAKANAN & MINUMAN ===\n")
            print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))
            
            # Add warning for low stock items (less than 10)
            low_stock = df_makanan[df_makanan['Stok'] < 10]
            if not low_stock.empty:
                print("\n⚠️ PERINGATAN STOCK MENIPIS:")
                for _, item in low_stock.iterrows():
                    print(f"• {item['Nama Menu']}: {item['Stok']} unit tersisa")
            
            # Add option to return to menu
            input("\nTekan Enter untuk kembali ke menu...")
            bersih()
            break

        except FileNotFoundError:
            print("\n❌ File makanan.csv tidak ditemukan!")
            input("Tekan Enter untuk kembali...")
            break
        except Exception as error:
            print(f"\n❌ Terjadi kesalahan: {str(error)}")
            input("Tekan Enter untuk kembali...")
            break

def cek_stock_fasilitas():
    while True:
        bersih()
        try:
            # Membaca data dari file CSV
            df_fasilitas = pd.read_csv('fasilitas.csv')
            
            # Membuat dataframe untuk tampilan dengan penomoran yang bersih
            display_df = df_fasilitas.copy()
            display_df.index = range(1, len(display_df) + 1)
            
            # Menampilkan daftar fasilitas
            print("\n=== STOCK FASILITAS ===\n")
            print(tabulate(display_df, headers=['No', 'namaproduk', 'Harga', 'Stock'], 
                           tablefmt='grid', showindex=True))
            
            # Menambahkan peringatan untuk item dengan stok rendah (kurang dari 10)
            low_stock = df_fasilitas[df_fasilitas['stock'] < 10]
            if not low_stock.empty:
                print("\n⚠️ \t PERINGATAN STOCK MENIPIS:")
                for _, item in low_stock.iterrows():
                    print(f"• {item['namaproduk']}: {item['stock']} unit tersisa")
            
            # Opsi untuk kembali ke menu
            input("\nTekan Enter untuk kembali ke menu...")
            bersih()
            break

        except FileNotFoundError:
            print("\n❌ File fasilitas.csv tidak ditemukan!")
            input("Tekan Enter untuk kembali...")
            break
        except Exception as error:
            print(f"\n❌ Terjadi kesalahan: {str(error)}")
            input("Tekan Enter untuk kembali...")
            break

def riwayat_transaksi():
    bersih()
    print("=== RIWAYAT TRANSAKSI ===")
    print("[1] Data Pesan Fasilitas")
    print("[2] Data Pesan Makanan")
    print("[3] Data Pesan Tiket")
    print("[4] Kembali")

    pilihan = input("Pilih opsi [1-4]: ")

    try:
        if pilihan == '1':
            # Menampilkan data pesan fasilitas
            df_fasilitas = pd.read_csv('data pesan fasilitas.csv')
            if df_fasilitas.empty:
                print("📄 Tidak ada riwayat transaksi fasilitas yang ditemukan.")
            else:
                print(tabulate(df_fasilitas, headers='keys', tablefmt='grid', showindex=True))
                nama_pelanggan = input("Masukkan nama pelanggan untuk mencari: ")
                filtered_df = df_fasilitas[df_fasilitas['nama'] == nama_pelanggan]
                if not filtered_df.empty:
                    print(tabulate(filtered_df, headers='keys', tablefmt='grid'))
                else:
                    print("📄 Tidak ada transaksi fasilitas untuk nama tersebut.")

        elif pilihan == '2':
            # Menampilkan data pesan makanan
            df_makanan = pd.read_csv('data pesan makanan.csv')
            if df_makanan.empty:
                print("📄 Tidak ada riwayat transaksi makanan yang ditemukan.")
            else:
                print(tabulate(df_makanan, headers='keys', tablefmt='grid', showindex=True))
                nama_pelanggan = input("Masukkan nama pelanggan untuk mencari: ")
                filtered_df = df_makanan[df_makanan['nama'] == nama_pelanggan]
                if not filtered_df.empty:
                    print(tabulate(filtered_df, headers='keys', tablefmt='grid'))
                else:
                    print("📄 Tidak ada transaksi makanan untuk nama tersebut.")

        elif pilihan == '3':
            # Menampilkan data pesan tiket
            df_tiket = pd.read_csv('Data Rekap.csv')
            if df_tiket.empty:
                print("📄 Tidak ada riwayat transaksi tiket yang ditemukan.")
            else:
                print(tabulate(df_tiket, headers='keys', tablefmt='grid', showindex=True))
                nama_pelanggan = input("Masukkan nama pelanggan untuk mencari: ")
                filtered_df = df_tiket[df_tiket['nama'] == nama_pelanggan]
                if not filtered_df.empty:
                    print(tabulate(filtered_df, headers='keys', tablefmt='grid'))
                else:
                    print("📄 Tidak ada transaksi tiket untuk nama tersebut.")

        elif pilihan == '4':
            bersih()
            return  # Kembali ke menu sebelumnya

        else:
            print("⚠️ Pilihan tidak valid!")

        input ('klik enter untuk Kembali Mencari Transaksi !')
        return riwayat_transaksi()

    except FileNotFoundError as e:
        print(f"❌ File tidak ditemukan: {str(e)}")
        input("Tekan Enter untuk kembali...")

##======================================================================##
## PEMBAYARAN
##======================================================================##
def tampilkan_metode_pembayaran():
    print("\n+---------------------------------+")
    print("|       Metode Pembayaran         |")
    print("+---------------------------------+")
    print("| 1 | Tunai                      |")
    print("| 2 | Virtual Account            |")
    print("| 3 | E-Wallet                   |")
    print("+---------------------------------+")
    return input("Pilih metode pembayaran Anda (1/2/3): ")

def tampilkan_pilihan_bank():
    print("\n+-----------------------------------+")
    print("|       Pilihan Bank VA             |")
    print("+-----------------------------------+")
    print("| 1 | BCA Virtual Account          |")
    print("| 2 | Mandiri Virtual Account      |")
    print("| 3 | BNI Virtual Account          |")
    print("| 4 | BRI Virtual Account          |")
    print("| 5 | Kembali ke menu pembayaran   |")
    print("+-----------------------------------+")
    return input("Pilih bank Virtual Account (1/2/3/4/5): ")

def tampilkan_pilihan_ewallet():
    print("\n+-----------------------------------+")
    print("|       Pilihan E-Wallet            |")
    print("+-----------------------------------+")
    print("| 1 | GoPay                        |")
    print("| 2 | Dana                         |")
    print("| 3 | OVO                          |")
    print("| 4 | LinkAja                      |")
    print("| 5 | ShopeePay                    |")
    print("| 6 | Kembali ke menu pembayaran   |")
    print("+-----------------------------------+")
    return input("Pilih E-Wallet (1/2/3/4/5/6): ")

def konfirmasi_pembayaran():
    while True:
        konfirmasi = input("\nApakah pembayaran sudah selesai? (y/n): ").lower()
        if konfirmasi in ['y', 'n']:
            return konfirmasi == 'y'
        print("Input tidak valid! Masukkan 'y' untuk ya atau 'n' untuk tidak.")

def proses_pembayaran(total_bayar):
    while True:
        metode_bayar = tampilkan_metode_pembayaran()
        if metode_bayar == "1":
            print("\n+-------------------------------+")
            print("|       Pembayaran Tunai        |")
            print("+-------------------------------+")
            print(f"Silakan menerima pembayaran sebesar Rp.{total_bayar}")
            
            if konfirmasi_pembayaran():
                print("\nTerima kasih sudah mempercayai sistem kami")
                bersih()
                break
            else:
                print("\nKembali ke menu metode pembayaran...")
                continue

        elif metode_bayar == "2":
            print("\n+-------------------------------+")
            print("|  Pembayaran Virtual Account   |")
            print("+-------------------------------+")
            pilihan_bank = tampilkan_pilihan_bank()

            if pilihan_bank == "1":
                print("\n+-------------------------------+")
                print("Anda memilih BCA Virtual Account")
                print("+-------------------------------+")
                print("Nomor VA: 89288126718271")  # BCA dengan awalan 89288
                print(f"Silakan menerima pembayaran sebesar Rp.{total_bayar}")
                
                if konfirmasi_pembayaran():
                    print("\nTerima kasih sudah mempercayai sistem kami")
                    break
                else:
                    print("\nKembali ke menu metode pembayaran...")
                    continue
                    
            elif pilihan_bank == "2":
                print("\n+-------------------------------+")
                print("Anda memilih Mandiri Virtual Account")
                print("+-------------------------------+")
                print("Nomor VA: 88088126718271")  # Mandiri dengan awalan 88088
                print(f"Silakan menerima pembayaran sebesar Rp.{total_bayar}")
                
                if konfirmasi_pembayaran():
                    print("\nTerima kasih sudah mempercayai sistem kami")
                    break
                else:
                    print("\nKembali ke menu metode pembayaran...")
                    continue
                    
            elif pilihan_bank == "3":
                print("\n+-------------------------------+")
                print("Anda memilih BNI Virtual Account")
                print("+-------------------------------+")
                print("Nomor VA: 88877126718271")  # BNI dengan awalan 88877
                print(f"Silakan menerima pembayaran sebesar Rp.{total_bayar}")
                
                if konfirmasi_pembayaran():
                    print("\nTerima kasih sudah mempercayai sistem kami")
                    break
                else:
                    print("\nKembali ke menu metode pembayaran...")
                    continue
                    
            elif pilihan_bank == "4":
                print("\n+-------------------------------+")
                print("Anda memilih BRI Virtual Account")
                print("+-------------------------------+")
                print("Nomor VA: 88811126718271")  # BRI dengan awalan 88811
                print(f"Silakan menerima pembayaran sebesar Rp.{total_bayar}")
                
                if konfirmasi_pembayaran():
                    print("\nTerima kasih sudah mempercayai sistem kami")
                    break
                else:
                    print("\nKembali ke menu metode pembayaran...")
                    continue
                    
            elif pilihan_bank == "5":
                print("\nKembali ke menu metode pembayaran...")
                continue
            else:
                print("\nPilihan bank tidak valid! Kembali ke menu pembayaran.")
                continue

        elif metode_bayar == "3":
            print("\n+-------------------------------+")
            print("|      Pembayaran E-Wallet      |")
            print("+-------------------------------+")
            pilihan_ewallet = tampilkan_pilihan_ewallet()

            if pilihan_ewallet == "1":
                print("\n+-------------------------------+")
                print("        Anda memilih GoPay         ")
                print("+-------------------------------+")
                print("Pelanggan scan QR Code GoPay atau Transfer ke 8726182612 a/n VIFARA Bioskop")
                print(f"Silakan menerima pembayaran sebesar Rp.{total_bayar}")
                
                if konfirmasi_pembayaran():
                    print("\nTerima kasih sudah mempercayai sistem kami")
                    break
                else:
                    print("\nKembali ke menu metode pembayaran...")
                    continue
                    
            elif pilihan_ewallet == "2":
                print("\n+-------------------------------+")
                print("         Anda memilih Dana         ")
                print("+-------------------------------+")
                print("Pelanggan scan QR Code Dana atau Transfer ke 8726182613 a/n VIFARA Bioskop")
                print(f"Silakan menerima pembayaran sebesar Rp.{total_bayar}")
                
                if konfirmasi_pembayaran():
                    print("\nTerima kasih sudah mempercayai sistem kami")
                    break
                else:
                    print("\nKembali ke menu metode pembayaran...")
                    continue
                    
            elif pilihan_ewallet == "3":
                print("\n+-------------------------------+")
                print("          Anda memilih OVO         ")
                print("+-------------------------------+")
                print("Pelanggan scan QR Code OVO atau Transfer ke 8726182614 a/n VIFARA Bioskop")
                print(f"Silakan menerima pembayaran sebesar Rp.{total_bayar}")
                
                if konfirmasi_pembayaran():
                    print("\nTerima kasih sudah mempercayai sistem kami")
                    break
                else:
                    print("\nKembali ke menu metode pembayaran...")
                    continue
                    
            elif pilihan_ewallet == "4":
                print("\n+-------------------------------+")
                print("        Anda memilih LinkAja       ")
                print("+-------------------------------+")
                print("Pelanggan scan QR Code LinkAja atau Transfer ke 8726182615 a/n VIFARA Bioskop")
                print(f"Silakan menerima pembayaran sebesar Rp.{total_bayar}")
                
                if konfirmasi_pembayaran():
                    print("\nTerima kasih sudah mempercayai sistem kami")
                    break
                else:
                    print("\nKembali ke menu metode pembayaran...")
                    continue
                    
            elif pilihan_ewallet == "5":
                print("\n+-------------------------------+")
                print("       Anda memilih ShopeePay      ")
                print("+-------------------------------+")
                print("Pelanggan scan QR Code ShopeePay atau Transfer ke 8726182616 a/n VIFARA Bioskop")
                print(f"Silakan menerima pembayaran sebesar Rp.{total_bayar}")
                
                if konfirmasi_pembayaran():
                    print("\nTerima kasih sudah mempercayai sistem kami")
                    break
                else:
                    print("\nKembali ke menu metode pembayaran...")
                    continue
                    
            elif pilihan_ewallet == "6":
                print("\nKembali ke menu metode pembayaran...")
                continue
            else:
                print("\nPilihan E-Wallet tidak valid! Kembali ke menu pembayaran.")
                continue

        else:
            print("\nPilihan metode pembayaran tidak valid! Coba lagi.")
            continue


















# def riwayat_transaksi():
#     bersih()
#     try:
#         # Membaca data dari file CSV
#         df_tiket = pd.read_csv('Data Rekap.csv')

#         if df_tiket.empty:
#             print("❌ Tidak ada riwayat transaksi yang ditemukan!")
#             input("Tekan Enter untuk kembali...")
#             return
        

#         # Meminta input nama pembeli
#         print(tabulate(df_tiket, headers='keys', tablefmt='grid', showindex=True))
#         nama_pembeli = input("Masukkan nama pembeli untuk mengecek riwayat transaksi: ")

#         # Filter data berdasarkan nama pembeli
#         riwayat = df_tiket[df_tiket['nama'].str.contains(nama_pembeli, case=False)]

#         if riwayat.empty:
#             print(f"❌ Tidak ada riwayat transaksi untuk nama '{nama_pembeli}'!")
#             input("Tekan Enter untuk kembali...")
#             return

#         # Menampilkan riwayat transaksi
#         print("\n=== RIWAYAT TRANSAKSI ===")
#         print(tabulate(riwayat, headers='keys', tablefmt='grid', showindex=True))
#         input("\nTekan Enter untuk kembali...")

#     except FileNotFoundError:
#         print("❌ File Data Rekap.csv tidak ditemukan!")
#         input("Tekan Enter untuk kembali...")
#     except Exception as error:
#         print(f"❌ Terjadi kesalahan: {str(error)}")
#         input("Tekan Enter untuk kembali...")

#==================================================================

# def penjualan_tiket():
#     while True:
#         bersih()
#         try:
#             df_jadwal = pd.read_csv('jadwal_bioskop.csv')
#             display_df = df_jadwal.copy()
#             display_df.index = range(1, len(display_df) + 1)

#             print("\n=== PENJUALAN TIKET BIOSKOP ===\n")
#             print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))

#             while True:
#                 # try:
#                     pilih_jadwal = int(input("\nPilih nomor jadwal film [1-{}]: ".format(len(display_df))))

#                     if 1 <= pilih_jadwal <= len(display_df):
#                         jadwal_terpilih = display_df.iloc[pilih_jadwal - 1]

#                         print("\n=== DETAIL TIKET ===")
#                         print(f"Film\t\t: {jadwal_terpilih['Film']}")
#                         print(f"Studio\t\t: {jadwal_terpilih['Studio']}")
#                         print(f"Jam Tayang\t: {jadwal_terpilih['Jam Tayang']}")
#                         print(f"Harga\t\t: Rp {jadwal_terpilih['harga']:,}")

#                         konfirmasi = input("\nLanjutkan pembelian tiket?\n [1] Ya / [2] Tidak\t: ")

#                         if konfirmasi == '1':
#                             print("\n=== INFORMASI PEMBELI ===")
#                             nama = input("Masukkan nama pembeli: ")

#                             # Generate seat layout
#                             seat_layout = generate_kursi(jadwal_terpilih['Studio'])
#                             kursi_terpakai = cek_kursi_terpakai(
#                                 jadwal_terpilih['Film'], 
#                                 jadwal_terpilih['Jam Tayang'], 
#                                 jadwal_terpilih['Studio']
#                             )

#                             # Display seat layout
#                             display_kursi(seat_layout, kursi_terpakai)

#                             kursi_tersedia = [seat for row in seat_layout for seat in row if seat not in kursi_terpakai]

#                             tiket_data = []
#                             harga_makan = 0  # Initialize these variables
#                             harga_fasilitas = 0
#                             while True:
#                                 kursi = input("\nMasukkan nomor kursi (Klik Enter [ Untuk Selesai ]): ").upper()

#                                 if not kursi:
#                                     break

#                                 if kursi not in kursi_tersedia:
#                                     print("\n❌ Kursi tidak tersedia!")
#                                     continue
#                                 kursi_tersedia.remove(kursi)
#                                 kursi_terpakai.append(kursi)  # Update kursi terpakai untuk tampilan
#                                 print(f"\n✅ Tiket untuk kursi {kursi} ditambahkan.")
#                                 display_kursi(seat_layout, kursi_terpakai)
#                                 if not kursi_tersedia:
#                                     print("\n⚠ Tidak ada kursi tersisa!")
#                                     break

#                                 tiket = {
#                                     'nama': nama,
#                                     'film': jadwal_terpilih['Film'],
#                                     'jam': jadwal_terpilih['Jam Tayang'],
#                                     'studio': jadwal_terpilih['Studio'],
#                                     'kursi': kursi,
#                                     'harga': jadwal_terpilih['harga'],
#                                     'harga_makan' : harga_makan,
#                                     'harga_fasilitas' : harga_fasilitas,
#                                     'total_harga':
#                                     #  jadwal_terpilih['harga'] + harga_makan + harga_fasilitas
#                                     # 'total_harga':total_bayar['total_harga']
#                                 }
#                                 tiket_data.append(tiket)
#                                    # total_harga += jadwal_terpilih['harga']
                                
#                                 # pilihan
#                             while True :
#                                 print(" [1] Makanan")
#                                 print(" [2] Fasilitas")
#                                 print(" [3] Batal")
#                                 print(" [4] Konfirmasi")

#                                 lanjutkan = input("Pilih Menu [1/2/3/4]: ")
#                                 match lanjutkan:
#                                     case "1":
#                                         harga_makan = pesan_makanan()
#                                         tiket['harga_makan'] = harga_makan
#                                     case "2":
#                                         harga_fasilitas = pesan_fasilitas()
#                                         tiket['harga_fasilitas'] = harga_fasilitas
#                                     case "3":
#                                         return
#                                     case "4":
#                                         if tiket_data:
#                                             df_tiket = pd.DataFrame(tiket_data)
#                                             try:
#                                                 df_existing = pd.read_csv('Data Rekap.csv')
#                                                 df_final = pd.concat([df_existing, df_tiket], ignore_index=True)
#                                             except FileNotFoundError:
#                                                 df_final = df_tiket

#                                             df_final.to_csv('Data Rekap.csv', index=False)

#                                             total_bayar = tiket['harga']+tiket['harga_makan']+tiket['harga_fasilitas']
#                                             proses_pembayaran(total_bayar)
#                                             print("\n✅ Tiket berhasil dibeli!")
#                                             print(f"Total Tiket: {len(tiket_data)}")
#                                             print(f'Total pembelanjaan anda {total_bayar}')
#                                             input("\nTekan Enter untuk melanjutkan...")
#                                             return True

#                                     case _:
#                                         print("⚠️  Error: Pilihan tidak valid!")
#                                         input("\nTekan Enter untuk mencoba lagi...")
#                                         return True
#                             else:
#                                 print("\n❌ Tidak ada tiket yang dibeli.")
#                                 input("Tekan Enter untuk kembali...")

#                         elif konfirmasi == '2':
#                             break
#                         else:
#                             print("\n❌ Pilihan tidak valid!")
#                             input("Tekan Enter untuk mencoba lagi...")

#                     else:
#                         print("\n❌ Nomor jadwal tidak valid!")
#                         input("Tekan Enter untuk mencoba lagi...")

#                 # except ValueError:
#                 #     print("\n❌ Masukkan angka yang valid!")
#                 #     input("Tekan Enter untuk mencoba lagi...")

#             lanjut = input("\nIngin membeli tiket lagi? (ya/tidak): ").lower()
#             if lanjut != 'ya':
#                 break

#         except FileNotFoundError:
#             print("\n❌ File jadwal_bioskop.csv tidak ditemukan!")
#             input("Tekan Enter untuk kembali...")
#             break
#         # except Exception as error:
#         #     print(f"\n❌ Terjadi kesalahan: {str(error)}")
#         #     input("Tekan Enter untuk kembali...")
#         #     break

# def pesan_makanan():
#     while True:
#         bersih()
#         try:
#             # Get current customer's name
#             nama_pelanggan = get_latest_customer
#             if not nama_pelanggan:
#                 print("\n❌ Tidak ada data pemesanan tiket!")
#                 input("Tekan Enter untuk kembali...")
#                 return 0
            
#             # Read the food menu CSV
#             df_makanan = pd.read_csv('makanan.csv')
    
#             # Create display dataframe with clean numbering
#             display_df = df_makanan.copy()
#             display_df.index = range(1, len(display_df) + 1)
            
#             # Display food menu
#             print(f"\n=== MENU MAKANAN & MINUMAN ===")
#             print(f"\tPelanggan: {'nama_pelanggan'}\n")
#             print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))
            
#             # Initialize order
#             pesanan = []
#             total_harga_makanan = 0
            
#             while True:
#                 try:
#                     pilih_menu = input("\nPilih nomor menu [1-{}] (Klik Enter [Untuk Selesai]): ".format(len(display_df)))
                    
#                     if pilih_menu == "":
#                         break
                    
#                     pilih_menu = int(pilih_menu)
#                     if 1 <= pilih_menu <= len(display_df):
#                         menu_terpilih = display_df.iloc[pilih_menu-1]
                        
#                         if menu_terpilih['Stok'] <= 0:
#                             print("\n❌ Maaf, stok habis!")
#                             continue
                        
#                         while True:
#                             try:
#                                 jumlah = int(input(f"Masukkan jumlah {menu_terpilih['Nama Menu']}: "))
#                                 if jumlah <= 0:
#                                     print("\n❌ Jumlah harus lebih dari 0!")
#                                     continue
#                                 if jumlah > menu_terpilih['Stok']:
#                                     print(f"\n❌ Stok tidak mencukupi! Stok tersedia: {menu_terpilih['Stok']}")
#                                     continue
#                                 break
#                             except ValueError:
#                                 print("\n❌ Masukkan angka yang valid!")
                        
#                         # Calculate subtotal
#                         subtotal = menu_terpilih['Harga'] * jumlah
#                         total_harga_makanan += subtotal
                        
#                         # Add to pesanan list
#                         pesanan.append({
#                             'idproduct': menu_terpilih['IDProduct'],
#                             'nama': 'nama_pelanggan',
#                             'nama_menu': menu_terpilih['Nama Menu'],
#                             'total pesan': jumlah,
#                             'total_bayar': subtotal
#                         })
                    
#                         # Update stock in makanan.csv
#                         df_makanan.loc[df_makanan['IDProduct'] == menu_terpilih['IDProduct'], 'Stok'] -= jumlah
#                         df_makanan.to_csv('makanan.csv', index=False)
                        
#                         print(f"\n✅ {jumlah}x {menu_terpilih['Nama Menu']} ditambahkan ke pesanan")
#                         print(f"Subtotal: Rp {subtotal:,}")

#                         return subtotal
                        
#                     else:
#                         print("\n❌ Nomor menu tidak valid!")
                
#                 except ValueError:
#                     print("\n❌ Masukkan angka yang valid!")
            
#             # Save to data pesan makanan.csv if there are orders
#             if pesanan:
#                 try:
#                     df_pesan_existing = pd.read_csv('data pesan makanan.csv')
#                     df_pesan_new = pd.DataFrame(pesanan)
#                     df_pesan_final = pd.concat([df_pesan_existing, df_pesan_new], ignore_index=True)
#                 except FileNotFoundError:
#                     df_pesan_final = pd.DataFrame(pesanan)
                
#                 df_pesan_final.to_csv('data pesan makanan.csv', index=False)
                
#                 # Update harga_makan in Data Rekap.csv for the current transaction
#                 try:
#                     df_test = pd.read_csv('Data Rekap.csv')
#                     if not df_test.empty:
#                         # Update the last row's harga_makan
#                         df_test.loc[df_test.index[-1], 'harga_makan'] = total_harga_makanan
#                         df_test.to_csv('Data Rekap.csv', index=False)
#                 except FileNotFoundError:
#                     print("\n❌ File Data Rekap.csv tidak ditemukan!")
                
#                 print("\n=== RINGKASAN PESANAN ===")
#                 print(f"Pelanggan: {'nama_pelanggan'}")
#                 print(f"Total Pesanan: Rp {total_harga_makanan:,}")
#                 input("\nTekan Enter untuk melanjutkan...")
#                 return total_harga_makanan
            
#         except FileNotFoundError:
#             print("\n❌ File makanan.csv tidak ditemukan!")
#             input("Tekan Enter untuk kembali...")
#             return 
#         except Exception as error:
#             print(f"\n❌ Terjadi kesalahan: {str(error)}")
#             input("Tekan Enter untuk kembali...")
#             return 

# def pesan_makanan():
#     while True:
#         bersih()

            
#         # Read the food menu CSV
#         df_makanan = pd.read_csv('makanan.csv')

#         # Create display dataframe with clean numbering
#         display_df = df_makanan.copy()
#         display_df.index = range(1, len(display_df) + 1)
        
#         # Display food menu
#         print(f"\n=== MENU MAKANAN & MINUMAN ===")
#         print(f"\tPelanggan: {'nama_pelanggan'}\n")
#         print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))
        
#         # Initialize order
#         pesanan = []
#         total_harga_makanan = 0
        
#         while True:
#             try:
#                 pilih_menu = input("\nPilih nomor menu [1-{}] (Klik Enter [Untuk Selesai]): ".format(len(display_df)))
                
#                 if pilih_menu == "":
#                     break
                
#                 pilih_menu = int(pilih_menu)
#                 if 1 <= pilih_menu <= len(display_df):
#                     menu_terpilih = display_df.iloc[pilih_menu-1]
                    
#                     if menu_terpilih['Stok'] <= 0:
#                         print("\n❌ Maaf, stok habis!")
#                         continue
                    
#                     while True:
#                         try:
#                             jumlah = int(input(f"Masukkan jumlah {menu_terpilih['Nama Menu']}: "))
#                             if jumlah <= 0:
#                                 print("\n❌ Jumlah harus lebih dari 0!")
#                                 continue
#                             if jumlah > menu_terpilih['Stok']:
#                                 print(f"\n❌ Stok tidak mencukupi! Stok tersedia: {menu_terpilih['Stok']}")
#                                 continue
#                             break
#                         except ValueError:
#                             print("\n❌ Masukkan angka yang valid!")
                    
#                     # Calculate subtotal
#                     subtotal = menu_terpilih['Harga'] * jumlah
#                     total_harga_makanan += subtotal
                    
#                     # Add to pesanan list
#                     pesanan.append({
#                         'idproduct': menu_terpilih['IDProduct'],
#                         'nama': 'nama_pelanggan',
#                         'nama_menu': menu_terpilih['Nama Menu'],
#                         'total pesan': jumlah,
#                         'total_bayar': subtotal
#                     })
                    
#                     # Update stock in makanan.csv
#                     df_makanan.loc[df_makanan['IDProduct'] == menu_terpilih['IDProduct'], 'Stok'] -= jumlah
#                     df_makanan.to_csv('makanan.csv', index=False)
                    
#                     print(f"\n✅ {jumlah}x {menu_terpilih['Nama Menu']} ditambahkan ke pesanan")
#                     print(f"Subtotal: Rp {subtotal:,}")
#                     return subtotal
                    
#                 else:
#                     print("\n❌ Nomor menu tidak valid!")
            
#             except ValueError:
#                 print("\n❌ Masukkan angka yang valid!")
            

#             # Save to data pesan makanan.csv if there are orders
#             if pesanan:
#                 try:
#                     # df_pesan_existing = pd.read_csv('data pesan makanan.csv')
#                     # df_pesan_new = pd.DataFrame(pesanan)
#                     df_pesanan = pd.concat([df_pesanan, pd.DataFrame(pesanan)], ignore_index=True)
#                     df_pesanan.to_csv('data pesan fasilitas.csv', index=False)
#                 except FileNotFoundError:
#                     df_pesan_final = pd.DataFrame(pesanan)
                
#                 df_pesan_final.to_csv('data pesan makanan.csv', index=False)
                
                
#                 # Update harga_makan in Data Rekap.csv for the current transaction
#                 try:
#                     df_test = pd.read_csv('Data Rekap.csv')
#                     if not df_test.empty:
#                         # Update the last row's harga_makan
#                         df_test.loc[df_test.index[-1], 'harga_makan'] = total_harga_makanan
#                         df_test.to_csv('Data Rekap.csv', index=False)
#                 except FileNotFoundError:
#                     print("\n❌ File Data Rekap.csv tidak ditemukan!")
                
#                 print("\n=== RINGKASAN PESANAN ===")
#                 print(f"Pelanggan: {'nama_pelanggan'}")
#                 print(f"Total Pesanan: Rp {total_harga_makanan:,}")
#                 input("\nTekan Enter untuk melanjutkan...")
#                 return total_harga_makanan
            
#         # except FileNotFoundError:
#         #     print("\n❌ File makanan.csv tidak ditemukan!")
#         #     input("Tekan Enter untuk kembali...")
#         #     return 
#         # except Exception as error:
#         #     print(f"\n❌ Terjadi kesalahan: {str(error)}")
#         #     input("Tekan Enter untuk kembali...")
#         #     return 

# def pesan_jajan():
#     while True:
#         bersih()
#         try:
#             # Read the food menu CSV
#             df_makanan = pd.read_csv('makanan.csv')
            
#             # Read existing orders CSV
#             try:
#                 df_pesanan = pd.read_csv('data pesan makanan.csv')
#             except FileNotFoundError:
#                 df_pesanan = pd.DataFrame(columns=['idproduct', 'nama', 'nama_menu', 'total pesan', 'total_bayar'])
            
#             # Create display dataframe with clean numbering
#             display_df = df_makanan.copy()
#             display_df.index = range(1, len(display_df) + 1)
            
#             # Display food menu
#             print("\n=== MENU MAKANAN & MINUMAN ===\n")
#             print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))
            
#             # Get customer name
#             nama_pembeli = input("\nMasukkan nama pembeli: ")
            
#             # Initialize order
#             pesanan = []
#             total_harga_total = 0
            
#             while True:
#                 try:
#                     pilih_menu = input("\nPilih nomor menu [1-{}] (kosongkan untuk selesai): ".format(len(display_df)))
                    
#                     if pilih_menu == "":
#                         break
                    
#                     pilih_menu = int(pilih_menu)
#                     if 1 <= pilih_menu <= len(display_df):
#                         menu_terpilih = display_df.iloc[pilih_menu - 1]
                        
#                         if menu_terpilih['Stok'] <= 0:
#                             print("\n❌ Maaf, stok habis!")
#                             continue
                        
#                         while True:
#                             try:
#                                 jumlah = int(input(f"Masukkan jumlah {menu_terpilih['Nama Menu']}: "))
#                                 if jumlah <= 0:
#                                     print("\n❌ Jumlah harus lebih dari 0!")
#                                     continue
#                                 if jumlah > menu_terpilih['Stok']:
#                                     print(f"\n❌ Stok tidak mencukupi! Stok tersedia: {menu_terpilih['Stok']}")
#                                     continue
#                                 break
#                             except ValueError:
#                                 print("\n❌ Masukkan angka yang valid!")

#                         # Calculate total price
#                         total_harga = menu_terpilih['Harga'] * jumlah
#                         total_harga_total += total_harga
                        
#                         # Add to order list
#                         new_order = {
#                             'idproduct': menu_terpilih['IDProduct'],
#                             'nama': nama_pembeli,
#                             'nama_menu': menu_terpilih['Nama Menu'],
#                             'total pesan': jumlah,
#                             'total_bayar': total_harga
#                         }
#                         pesanan.append(new_order)
                        
#                         # Update stock in original dataframe
#                         df_makanan.loc[df_makanan['IDProduct'] == menu_terpilih['IDProduct'], 'Stok'] -= jumlah
                        
#                         print(f"\n✅ {jumlah}x {menu_terpilih['Nama Menu']} ditambahkan ke pesanan")
#                         print(f"total_bayar: Rp {total_harga:,}")
                        
#                     else:
#                         print("\n❌ Nomor menu tidak valid!")
                        
#                 except ValueError:
#                     print("\n❌ Masukkan angka yang valid!")
            
#             if pesanan:
#                 # Add new orders to existing orders
#                 new_orders_df = pd.DataFrame(pesanan)
#                 df_pesanan = pd.concat([df_pesanan, new_orders_df], ignore_index=True)
#                 df_pesanan.to_csv('data pesan makanan.csv', index=False)

#                 # Call payment process function
#                 proses_pembayaran(total_harga_total)

#                 print("\n=== RINGKASAN PESANAN ===")
#                 print(tabulate(pesanan, headers='keys', tablefmt='grid'))
#                 print(f"\nTotal Pembayaran: Rp {total_harga_total:,}")
                
#             input("\nTekan Enter untuk kembali ke menu...")
#             break

#         except FileNotFoundError:
#             print("\n❌ File makanan.csv tidak ditemukan!")
#             input("Tekan Enter untuk kembali...")
#             break
#         except Exception as error:
#             print(f"\n❌ Terjadi kesalahan: {str(error)}")
#             input("Tekan Enter untuk kembali...")
#             break

# def penjualan_tiket():
#     while True:
#         bersih()
#         try:
#             df_jadwal = pd.read_csv('jadwal_bioskop.csv')
#             display_df = df_jadwal.copy()
#             display_df.index = range(1, len(display_df) + 1)

#             print("\n=== PENJUALAN TIKET BIOSKOP ===\n")
#             print(tabulate(display_df, headers='keys', tablefmt='grid', showindex=True))

#             while True:
#                 pilih_jadwal = int(input("\nPilih nomor jadwal film [1-{}]: ".format(len(display_df))))

#                 if 1 <= pilih_jadwal <= len(display_df):
#                     jadwal_terpilih = display_df.iloc[pilih_jadwal - 1]

#                     print("\n=== DETAIL TIKET ===")
#                     print(f"Film\t\t: {jadwal_terpilih['Film']}")
#                     print(f"Studio\t\t: {jadwal_terpilih['Studio']}")
#                     print(f"Jam Tayang\t: {jadwal_terpilih['Jam Tayang']}")
#                     print(f"Harga\t\t: Rp {jadwal_terpilih['harga']:,}")

#                     konfirmasi = input("\nLanjutkan pembelian tiket?\n [1] Ya / [2] Tidak\t: ")

#                     if konfirmasi == '1':
#                         print("\n=== INFORMASI PEMBELI ===")
#                         nama = input("Masukkan nama pembeli: ")

#                         # Generate seat layout
#                         seat_layout = generate_kursi(jadwal_terpilih['Studio'])
#                         kursi_terpakai = cek_kursi_terpakai(
#                             jadwal_terpilih['Film'], 
#                             jadwal_terpilih['Jam Tayang'], 
#                             jadwal_terpilih['Studio']
#                         )

#                         display_kursi(seat_layout, kursi_terpakai)

#                         kursi_tersedia = [seat for row in seat_layout for seat in row if seat not in kursi_terpakai]

#                         tiket_data = []
#                         harga_makan = 0  
#                         harga_fasilitas = 0

#                         while True:
#                             kursi = input("\nMasukkan nomor kursi (Klik Enter [ Untuk Selesai ]): ").upper()

#                             if not kursi:
#                                 break

#                             if kursi not in kursi_tersedia:
#                                 print("\n❌ Kursi tidak tersedia!")
#                                 continue

#                             kursi_tersedia.remove(kursi)
#                             kursi_terpakai.append(kursi)  
#                             print(f"\n✅ Tiket untuk kursi {kursi} ditambahkan.")
#                             display_kursi(seat_layout, kursi_terpakai)

#                             if not kursi_tersedia:
#                                 print("\n⚠ Tidak ada kursi tersisa!")
#                                 break

#                             tiket = {
#                                 'nama': nama,
#                                 'film': jadwal_terpilih['Film'],
#                                 'jam': jadwal_terpilih['Jam Tayang'],
#                                 'studio': jadwal_terpilih['Studio'],
#                                 'kursi': kursi,
#                                 'harga': jadwal_terpilih['harga'],
#                                 'harga_makan': harga_makan,
#                                 'harga_fasilitas': harga_fasilitas,
#                                 'total_harga': 0  # Placeholder
#                             }
#                             tiket_data.append(tiket)

#                         while True:
#                             print(" [1] Makanan")
#                             print(" [2] Fasilitas")
#                             print(" [3] Batal")
#                             print(" [4] Konfirmasi")

#                             lanjutkan = input("Pilih Menu [1/2/3/4]: ")
#                             match lanjutkan:
#                                 case "1":
#                                     harga_makan = pesan_makanan()
#                                     for t in tiket_data:
#                                         t['harga_makan'] = harga_makan

#                                 case "2":
#                                     harga_fasilitas = pesan_fasilitas()
#                                     for t in tiket_data:
#                                         t['harga_fasilitas'] = harga_fasilitas
#                                 case "3":
#                                     return
#                                 case "4":
#                                     if tiket_data:
#                                         # Update total_harga
#                                         for t in tiket_data:
#                                             total_harga = t['harga'] + t['harga_makan'] + t['harga_fasilitas']
#                                             t['total_harga'] = total_harga

#                                         df_tiket = pd.DataFrame(tiket_data)
#                                         try:
#                                             df_existing = pd.read_csv('Data Rekap.csv')
#                                             df_final = pd.concat([df_existing, df_tiket], ignore_index=True)
#                                         except FileNotFoundError:
#                                             df_final = df_tiket

#                                         df_final.to_csv('Data Rekap.csv', index=False)

#                                         total_bayar = sum(t['total_harga'] for t in tiket_data)  # Total all tickets
#                                         proses_pembayaran(total_bayar)
#                                         print("\n✅ Tiket berhasil dibeli!")
#                                         print(f"Total Tiket: {len(tiket_data)}")
#                                         print(f'Total pembelanjaan anda {total_bayar}')
#                                         input("\nTekan Enter untuk melanjutkan...")
#                                         return True

#                                 case _:
#                                     print("⚠️  Error: Pilihan tidak valid!")
#                                     input("\nTekan Enter untuk mencoba lagi...")
#                                     return True
                                
#                     elif konfirmasi == '2':
#                         break
#                     else:
#                         print("\n❌ Pilihan tidak valid!")
#                         input("Tekan Enter untuk mencoba lagi...")

#                 else:
#                     print("\n❌ Nomor jadwal tidak valid!")
#                     input("Tekan Enter untuk mencoba lagi...")

#             lanjut = input("\nIngin membeli tiket lagi? (ya/tidak): ").lower()
#             if lanjut != 'ya':
#                 break

#         except FileNotFoundError:
#             print("\n❌ File jadwal_bioskop.csv tidak ditemukan!")
#             input("Tekan Enter untuk kembali...")
#             break
