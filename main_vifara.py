import login_vifara as lovi
import dashboard_vifara as dasi


def print_banner():
    banner = """
 ██╗   ██╗██╗███████╗ █████╗ ██████╗  █████╗ 
 ██║   ██║██║██╔════╝██╔══██╗██╔══██╗██╔══██╗
 ██║   ██║██║█████╗  ███████║██████╔╝███████║
 ╚██╗ ██╔╝██║██╔══╝  ██╔══██║██╔══██╗██╔══██║
  ╚████╔╝ ██║██║     ██║  ██║██║  ██║██║  ██║
   ╚═══╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
        Created By: Kelompok - 4 
    """
    menu = """
╔══════════════════════════════════════════╗
║           🌟 Selamat Datang 🌟           ║
║                                          ║
║ ┌──────────────────────────────────────┐ ║
║ │            SISTEM VIFARA             │ ║
║ ├──────────────────────────────────────┤ ║
║ │                                      │ ║
║ │    [1] 📍 Login                      │ ║
║ │    [2] 📝 Register                   │ ║
║ │    [3] 📒 About VIFARA               │ ║
║ │    [4] 🚪 Keluar                     │ ║
║ │                                      │ ║
║ ├──────────────────────────────────────┤ ║
║ │        2024 VIFARA Movie System      │ ║
║ └──────────────────────────────────────┘ ║
║                                          ║
╚══════════════════════════════════════════╝
    """
    print(banner)
    print(menu)

def main():
    while True:
        lovi.bersih()
        print_banner()
        
        pilihan_menu = input('Silahkan Pilih Menu [ 1 | 2 | 3 | 4 ] = ')
        match pilihan_menu:
            case "1":
                user_data=lovi.login()
                while lovi.login_status:
                    dasi.tampilkan_dashboard(user_data)
            case "2":
                lovi.register()
            case "3":
                lovi.about()
            case "4":
                lovi.bersih()
                print("""
╔════════════════════════════════════════╗
║     Terima Kasih Sudah Menggunakan     ║
║           Layanan VIFARA  😊           ║
╚════════════════════════════════════════╝
""")
                break
            case _ :
                print ("⚠️  Error: Mohon masukkan pilihan yang valid (1-4)!")
                input ("Tekan Enter untuk mencoba kembali")
                
main()