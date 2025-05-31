# Tugas Besar DSP: Monitor Sinyal Vital Real-time Berbasis Visi Komputer

## Deskripsi Proyek

Monitor Sinyal Vital Real-time adalah sebuah aplikasi desktop inovatif yang dirancang untuk mendeteksi dan memvisualisasikan dua sinyal vital penting manusia secara non-invasif menggunakan kamera web standar: laju pernapasan dan sinyal photoplethysmography jarak jauh (rPPG). Aplikasi ini memanfaatkan teknik pemrosesan sinyal digital (DSP) dan visi komputer untuk menganalisis frame video secara real-time, mengekstraksi informasi fisiologis, dan menampilkannya dalam antarmuka pengguna grafis (GUI) yang intuitif dan modern.

**Fitur Utama:**
* **Deteksi Pernapasan Non-Kontak:** Menganalisis perubahan intensitas piksel pada area bahu atau dada yang disebabkan oleh gerakan pernapasan untuk memperkirakan laju pernapasan.
* **Estimasi Sinyal rPPG:** Mendeteksi perubahan halus warna kulit pada wajah (khususnya dari kanal hijau) yang berkorelasi dengan variasi volume darah akibat detak jantung, guna mengestimasi sinyal rPPG.
* **Visualisasi Real-time Interaktif:** Menampilkan feed video langsung dari kamera bersama dengan plot dinamis sinyal pernapasan dan rPPG. Pengguna dapat melihat data mentah yang diekstraksi dalam bentuk grafik.
* **Antarmuka Pengguna Grafis (GUI) Modern:** Dibangun menggunakan Tkinter dengan tema kustom untuk pengalaman pengguna yang lebih baik. Menyediakan kontrol yang mudah untuk memulai dan menghentikan proses monitoring.
* **Teknologi yang Digunakan:**
    * **OpenCV:** Untuk akuisisi dan pemrosesan frame video.
    * **MediaPipe:** Untuk deteksi landmark wajah (rPPG) dan pose tubuh (pernapasan) guna menentukan Region of Interest (ROI) secara dinamis.
    * **NumPy:** Untuk operasi numerik pada data sinyal dan gambar.
    * **Matplotlib:** Untuk membuat dan menampilkan plot sinyal yang divisualisasikan.
    * **Tkinter:** Untuk membangun antarmuka pengguna grafis.
    * **Pillow (PIL):** Untuk manipulasi gambar dan integrasi dengan Tkinter.

Proyek ini bertujuan untuk mendemonstrasikan penerapan praktis teknik pemrosesan sinyal digital dalam domain analisis sinyal biomedis yang diperoleh melalui metode optik (visi komputer). Hal ini membuka potensi untuk solusi pemantauan kesehatan jarak jauh yang lebih mudah diakses dan nyaman bagi pengguna.

## Nama Anggota
* Ahmad Zain Mahmud (121140232) ID:AhmadZain121140232
* Muhammad Rafif Vivaldi (122140026) ID:REDFOXX-APRIL
* Joshia Fernandes Sectio Purba (122140170) ID:Joshia05

## Logbook
* 09/05/2025 – Membuat repository GitHub, mengundang kolaborator. (Oleh: Ahmad Zain Mahmud)
* 24/05/2025 – Push file awal proyek ke repository, serta pengerjaan laporan bagian Pendahuluan dan Landasan Teori. (Oleh: Ahmad Zain Mahmud)
* 25/05/2025 – Revisi dan penyempurnaan bagian Landasan Teori dalam laporan. (Oleh: Muhammad Rafif Vivaldi)
* 26/05/2025 – Pembaruan komentar dalam kode, penambahan docstring, dan perbaikan README.md. (Oleh: Semua anggota)
* 30/05/2025 – Pengerjaan bagian Metodologi dan Hasil Pengujian dalam laporan. (Oleh: Muhammad Rafif Vivaldi)
* 31/05/2025 – Pengerjaan bagian Evaluasi Sistem dan Kesimpulan. (Oleh: Joshia Fernandes Sectio Purba)

## Instruksi Instalasi

Pastikan Anda memiliki Python 3.7 atau versi lebih baru terinstal di sistem Anda.

1.  **Clone Repository (Jika Proyek Ada di Git Repository Online):**
    ```bash
    git clone https://github.com/AhmadZain121140232/Tugas-Besar-DSP.git
    cd Tugas-Besar-DSP
    ```
    Jika Anda hanya memiliki file proyek secara lokal, lewati langkah ini dan pastikan Anda berada di direktori utama proyek.

2.  **Buat dan Aktifkan Lingkungan Virtual (Sangat Direkomendasikan):**
    Ini membantu mengisolasi dependensi proyek Anda.
    ```bash
    python -m venv venv
    ```
    Aktifkan lingkungan virtual:
    * **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Instal Dependensi Proyek:**
    Semua pustaka pihak ketiga yang dibutuhkan tercantum dalam file `requirements.txt`. Instal menggunakan pip:
    ```bash
    pip install -r requirements.txt
    ```
    Pustaka utama yang akan diinstal meliputi:
    * `opencv-python`: Untuk fungsi-fungsi visi komputer.
    * `tensorflow`: Sebagai backend atau dependensi untuk beberapa fungsionalitas (terkadang dibutuhkan oleh MediaPipe secara implisit, meskipun tidak secara langsung digunakan dalam kode yang terlihat).
    * `mediapipe`: Untuk deteksi wajah dan landmark tubuh.
    * `numpy`: Untuk komputasi numerik.
    * `scipy`: Untuk fungsi saintifik, seperti filter sinyal.
    * `matplotlib`: Untuk plotting grafik sinyal.

    Jika Anda menggunakan sistem operasi Linux dan Tkinter belum terinstal, Anda mungkin perlu menginstalnya secara manual:
    ```bash
    sudo apt-get update
    sudo apt-get install python3-tk
    ```

## Dokumentasi Penggunaan Program

1.  **Menjalankan Aplikasi:**
    * Pastikan semua dependensi telah terinstal dan lingkungan virtual (jika digunakan) telah diaktifkan.
    * Navigasikan ke direktori root proyek Anda di terminal.
    * Jalankan skrip utama:
        ```bash
        python main.py
        ```

2.  **Antarmuka Pengguna Utama:**
    * Setelah dijalankan, jendela aplikasi dengan judul "Monitor Sinyal Vital Real-time" akan muncul.
    * **Judul Aplikasi:** Terdapat di bagian atas jendela.
    * **Tombol Kontrol:** Dua tombol utama tersedia:
        * `Mulai Monitoring`: Mengaktifkan kamera, memulai deteksi, dan visualisasi sinyal.
        * `Hentikan Monitoring`: Menghentikan proses monitoring dan mematikan kamera.
    * **Area Tampilan:**
        * **Video Kamera Langsung (Kiri):** Menampilkan feed video dari kamera default sistem Anda. Di atas video, akan muncul kotak penanda Region of Interest (ROI):
            * Kotak **hijau** menunjukkan area yang digunakan untuk estimasi sinyal pernapasan (sekitar bahu/dada).
            * Kotak **biru** menunjukkan area wajah yang digunakan untuk estimasi sinyal rPPG.
        * **Visualisasi Sinyal (Kanan):** Menampilkan dua plot grafik secara real-time:
            * Sinyal **Pernapasan** (warna hijau terang/lime).
            * Sinyal **rPPG** (warna cyan terang).
            Sumbu X merepresentasikan frame atau waktu, dan sumbu Y merepresentasikan intensitas sinyal.

3.  **Langkah-langkah Penggunaan:**
    * **Mulai Monitoring:**
        * Klik tombol "**Mulai Monitoring**". Tombol ini akan menjadi nonaktif, dan tombol "Hentikan Monitoring" akan aktif.
        * Alternatif: Tekan tombol '**s**' pada keyboard untuk memulai monitoring jika jendela aplikasi aktif.
        * Pastikan wajah dan area bahu/dada Anda terlihat jelas oleh kamera dalam kondisi pencahayaan yang cukup. Pergerakan minimal akan menghasilkan sinyal yang lebih baik.
    * **Selama Monitoring:**
        * Amati feed video dan perubahan ROI yang dideteksi.
        * Perhatikan plot sinyal yang diperbarui secara dinamis di sebelah kanan.
    * **Hentikan Monitoring:**
        * Klik tombol "**Hentikan Monitoring**". Tombol ini akan menjadi nonaktif, dan tombol "Mulai Monitoring" akan aktif kembali.
        * Alternatif: Tekan tombol '**x**' pada keyboard untuk menghentikan monitoring.
    * **Menutup Aplikasi:**
        * Klik tombol 'X' standar pada bar judul jendela aplikasi.
        * Alternatif: Tekan tombol '**q**' pada keyboard untuk menutup aplikasi.

4.  **Pesan Error dan Troubleshooting:**
    * Jika kamera tidak dapat diakses atau gagal menangkap frame, pesan error akan dicetak ke konsol/terminal tempat Anda menjalankan aplikasi. Pastikan kamera tidak digunakan oleh aplikasi lain.
    * Kualitas deteksi dan sinyal sangat dipengaruhi oleh kondisi pencahayaan, jarak ke kamera, dan minimnya gerakan subjek.
