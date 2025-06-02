# Riuh-Stadion
Nama Tim:
- Khoirul Rijal Wicaksono (122140234)
- Sakinah Aulia (122140210)
  
# Link DEMO :
https://drive.google.com/file/d/1gWFmYL0usIp3Ye97u5D_hYQ51VqROOC5/view

Penjelasan:
filter interaktif menggunakan Python yang menciptakan suasana layaknya berada di stadion sepak bola. Sistem akan mendeteksi suara teriakan pengguna —jika volume atau frekuensinya tinggi, maka secara otomatis akan diputar suara sorakan supporter lain yang bergemuruh. Selain itu, filter juga mengenali gestur tangan seperti tepuk tangan dan sorakan tangan melalui kamera. Ketika gerakan tersebut terdeteksi, animasi penonton ikut bertepuk tangan disertai suara crowd.


## Progress Pertama

**Fitur awal (progress)**
* **Deteksi Suara:** Mendeteksi suara teriakan dan tepuk tangan.
* **Respons Suara:** Ketika ada suara teriakan atau tepuk tangan, filter akan membuat suara tersebut ikut bergema, seolah-olah penonton lain ikut terpengaruh.

**Progres dan Masalah**
* **Terlalu Responsif:** Filter saat ini terlalu sensitif, jadi kadang suara bisa tumpang tindih dan menghasilkan suara yang kacau.
* **Lambat Responsif:** Suara filter tidak langsung berhenti ketika berhenti teriak atau tepuk tangan. Seharusnya filter suara berhenti ketika input suara berhenti, tapi masih ada delay.
* **Background/Animasi dan Suara Dummy:** Saat ini, background/animasi dan suara yang digunakan untuk filter masih berupa placeholder (dummy) dan belum sepenuhnya terintegrasi dengan baik. Rencananya, akan ada pembaruan untuk menambahkan animasi dan suara yang lebih realistis.

**Tantangan yang Dihadapi:**
* **Library Pygame:** Awalnya kami ragu pakai `pygame` untuk proyek ini karena diperbolehkan atau tidak, tapi setelah tanya ke Asisten dosen, katanya nggak masalah dan boleh pakai.

## Progress kedua
  * **Update final background dan suara:** Menambahkan animasi dan suara yang yang kami rasa sangat cocok untuk filter yang kami buat.

**Rencana Ke Depan**
* **Perbaiki Deteksi Suara:** Harus bikin filter suara lebih stabil dan nggak tumpang tindih.
* **Hentikan Filter Suara:** Saat nggak ada suara, filter harus berhenti otomatis.

## Progress Ketiga (Akhir)

Proyek ini merupakan aplikasi real-time berbasis Python yang menggabungkan **deteksi suara**, **deteksi gesture tangan**, dan **virtual background** untuk menciptakan efek interaktif seperti di stadion. Aplikasi memanfaatkan kamera laptop dan mikrofon internal untuk mengenali aksi pengguna, lalu menampilkan latar belakang yang sesuai dan memutar efek suara yang relevan.

### 🔧 Teknologi yang Digunakan

* **OpenCV** untuk menangkap video dari webcam dan menampilkan hasil akhir ke layar.
* **NumPy** untuk menghitung volume suara menggunakan Root Mean Square (RMS).
* **SoundDevice** untuk menangkap input audio secara real-time dari mikrofon.
* **MediaPipe** untuk dua fungsi utama: segmentasi tubuh pengguna (untuk mengganti background), dan deteksi gesture tangan (untuk mengenali tepuk tangan).
* **Pygame** untuk memainkan file audio seperti suara sorakan dan tepuk tangan.
* **Threading** untuk menjalankan proses audio dan video secara paralel tanpa saling mengganggu.

### 🧠 Cara Kerja Sistem

1. **Load Gambar dan Suara**
   Sistem memuat tiga gambar latar belakang (idle, cheer, clap) dan dua efek suara (`teriak.wav` untuk sorakan dan `tepuktangan.wav` untuk tepuk tangan), semuanya disesuaikan ukurannya menjadi 640x480 piksel.

2. **Inisialisasi Variabel Status**
   Terdapat tiga status utama: `audio_status`, `gesture_status`, dan `current_status`. Status ini digunakan untuk menentukan apakah pengguna sedang idle, bersorak, atau bertepuk tangan.

3. **Deteksi Suara**
   Input suara dari mikrofon dianalisis setiap saat. Jika volume suara melebihi ambang batas (sekitar -20 dB), sistem menganggap pengguna sedang bersorak dan mengganti latar belakang menjadi gambar stadion penuh sorakan, lalu memutar suara teriak. Sistem menggunakan metode "debounce" agar status tidak langsung kembali idle jika suara hilang sejenak.

4. **Deteksi Gesture Tangan**
   Menggunakan model MediaPipe Hands, sistem akan mendeteksi keberadaan tangan di depan kamera. Jika tangan terdeteksi, status berubah menjadi `clap` dan latar belakang diganti dengan gambar penonton bertepuk tangan, serta suara tepuk tangan akan diputar berulang. Jika tangan tidak terdeteksi selama 0.5 detik, status akan kembali ke `idle`.

5. **Prioritas Status**
   Sistem selalu memberikan prioritas pada gesture `clap` dibanding `cheer`. Jadi, jika kedua input (suara dan tangan) terdeteksi secara bersamaan, maka gesture tepuk tangan akan menjadi prioritas.

6. **Virtual Background**
   MediaPipe Selfie Segmentation digunakan untuk mendeteksi bagian tubuh pengguna dan mengganti latar belakang aslinya dengan salah satu dari tiga gambar yang telah disiapkan, sesuai dengan status saat ini (`idle`, `cheer`, atau `clap`).

7. **Loop Utama**
   Program menampilkan hasil akhir ke jendela OpenCV bernama “Filter Stadion”. Loop ini terus berjalan hingga pengguna menekan tombol `q`.

8. **Multithreading**
   Agar suara dan video bisa berjalan bersamaan tanpa lag, proses audio dijalankan di thread terpisah dari proses tampilan video webcam.

### 📈 Fitur Utama yang Sudah Selesai

* Deteksi suara keras (teriakan) dengan kontrol ambang batas.
* Deteksi gesture tangan menggunakan MediaPipe.
* Pergantian background secara real-time berdasarkan status.
* Pemutaran audio otomatis sesuai aksi pengguna.
* Implementasi debounce untuk kestabilan interaksi.
* Threading untuk menjalankan webcam dan mikrofon secara bersamaan.

## 🛠️ Instruksi Instalasi

### 1. Persyaratan Sistem

* Sistem operasi: Windows, Linux, atau macOS.
* Webcam dan mikrofon internal aktif.
* Python 3.8 atau lebih baru.
* Jupyter Notebook telah terinstal (bisa melalui Anaconda atau `pip install notebook`).

### 2. Instalasi Library yang Dibutuhkan

Jalankan perintah berikut di terminal atau Jupyter Notebook cell untuk menginstal dependensi:

```bash
pip install opencv-python mediapipe numpy sounddevice pygame
```

### 3. Struktur Folder

Pastikan semua file berada dalam satu folder:

```
- stadion.ipynb                # Notebook utama
- stadion.jpg                  # Gambar latar default
- teriak.jpg                   # Gambar saat suara keras (teriakan)
- tepuktangan.jpg              # Gambar saat gesture tangan terdeteksi
- teriak.wav                   # Efek suara sorakan
- tepuktangan.wav              # Efek suara gesture tangan
```

---

## ▶️ Cara Menjalankan Program

1. Buka terminal atau Anaconda Navigator.
2. Arahkan ke direktori tempat file berada.
3. Jalankan Jupyter Notebook:

```bash
jupyter notebook
```

4. Buka file **`stadion.ipynb`**.
5. Jalankan seluruh sel secara berurutan.
6. Jendela kamera akan muncul dengan latar virtual.
   
   ![Screenshot 2025-05-31 152926](https://github.com/user-attachments/assets/4e22d63a-565c-4bef-bf87-90dbc6ce6c95)

7. **Tekan tombol `q` pada jendela kamera untuk keluar.**


## 📢 Cara Penggunaan Program

### 🎤 1. Deteksi Sorakan Melalui Suara

* Pastikan mikrofon aktif dan berada dalam jarak 30–50 cm dari wajah.
* **Atur input volume mikrofon pada rentang 30–40%** dari pengaturan sistem agar deteksi suara lebih akurat.
  
![volume](https://github.com/user-attachments/assets/ef2f200c-88c8-4097-9909-a3eb8f5893dc)

* Program akan merespons jika suara melebihi ambang batas (\~-20 dB).
* Untuk memicu efek sorakan:

  * Teriakkan secara **berulang dan penuh semangat**, misalnya:

    > "GOAL! GOAL! GOAL!"
  * Semakin emosional dan heboh, semakin realistis efek yang ditampilkan.

![Screenshot 2025-05-31 152912](https://github.com/user-attachments/assets/e6e27437-7c0c-4e2d-b8db-1bb2d2f44cc0)

### ✋ 2. Deteksi Gesture Tangan

* Program mendeteksi keberadaan **tangan apa pun di depan kamera**.
* Anda bisa mengangkat satu atau dua tangan, bertepuk tangan, atau melakukan gerakan sorakan tangan seperti mengangkat dan mengepalkan tangan.
* Saat gesture tangan terdeteksi:

  * Latar belakang akan berubah menyesuaikan kondisi penonton yang bersorak/bertepuk tangan.
  * Efek audio tepuk tangan otomatis diputar selama tangan masih terlihat.
* **Tidak perlu tepuk tangan secara sempurna**, karena program mendeteksi keberadaan tangan, bukan suara tepuknya.

![Screenshot 2025-05-31 152808](https://github.com/user-attachments/assets/c8e001c2-63a5-4195-ad40-704006215645)
![Screenshot 2025-05-31 152848](https://github.com/user-attachments/assets/572549f9-be5b-42cd-9f4a-a1cf5eca3ae9)

