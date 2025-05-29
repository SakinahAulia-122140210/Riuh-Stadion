# Riuh-Stadion
Nama Tim:
- Khoirul Rijal Wicaksono (122140234)
- Sakinah Aulia (122140210)

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
* **Library Pygame:** Awalnya kami ragu pakai `pygame` untuk proyek ini karena diperbolehkan atau tidak, tapi setelah tanya ke Asisten doses, katanya nggak masalah dan boleh pakai.

  ## Progress kedua
  * **Update final background dan suara:** Menambahkan animasi dan suara yang yang kami rasa sangat cocok untuk filter yang kami buat.

**Rencana Ke Depan**
* **Perbaiki Deteksi Suara:** Harus bikin filter suara lebih stabil dan nggak tumpang tindih.
* **Hentikan Filter Suara:** Saat nggak ada suara, filter harus berhenti otomatis.

