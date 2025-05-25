from main_dashboard import VitalDashboard # Mengimpor kelas VitalDashboard dari file main_dashboard.py
import tkinter as tk # Mengimpor modul tkinter sebagai tk untuk membuat GUI

# Titik masuk utama aplikasi
if __name__ == "__main__":
    """
    Fungsi utama yang akan dieksekusi ketika skrip dijalankan.
    Fungsi ini menginisialisasi root window Tkinter, membuat instance dari VitalDashboard,
    dan memulai event loop utama Tkinter.
    """
    root = tk.Tk()  # Membuat instance utama (root window) dari Tkinter
    app = VitalDashboard(root)  # Membuat instance dari aplikasi VitalDashboard, meneruskan root window
    root.mainloop()  # Memulai event loop Tkinter, membuat jendela tetap terbuka dan responsif