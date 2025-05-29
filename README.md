# 🕵️‍♂️ Photo Year Estimator

**Photo Year Estimator** adalah aplikasi lokal berbasis Python yang mampu memperkirakan era atau tahun pengambilan foto hanya dari file gambar, **tanpa menggunakan AI atau Machine Learning**. Aplikasi ini menggunakan pendekatan berbasis _visual forensics_, seperti analisis DPI, entropi gambar, metadata EXIF, histogram RGB, ketajaman, dan warna dominan.

---

## 🔍 Fitur Utama

- 📸 **Deteksi Metadata EXIF** (jika tersedia)
- 🎨 **Ekstraksi Warna Dominan** (dalam format HEX)
- 📊 **Analisis Statistik Histogram** (skew & kurtosis RGB)
- 🧠 **Penghitungan Entropi** (keragaman visual)
- 🔎 **Deteksi Ketajaman dan Noise**
- 🌗 **Klasifikasi Warna Dominan (Color Cast)**
- ⏳ **Estimasi Era Foto** dari pola visual
- ✅ **100% Offline & Non-AI** — semua proses lokal

---

## 📁 Struktur Proyek

```
photo_year_estimator/
├── main.py
├── run.sh
├── requirements.txt
├── services/
│   └── image_service.py
├── rules/
│   └── year_classifier.py
└── output/
    └── analysis_results.txt (jika disimpan)
```

---

## 🚀 Cara Menjalankan

### 1. **Clone proyek**
```bash
git clone https://github.com/username/photo_year_estimator.git
cd photo_year_estimator
```

### 2. **Aktifkan Virtual Environment (opsional tapi direkomendasikan)**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install Dependensi**
```bash
pip install -r requirements.txt
```

### 4. **Jalankan Analisa**
```bash
python main.py "/path/to/your/image.jpg"
```

Atau gunakan shell script:

```bash
bash run.sh
```

---

## 💡 Contoh Output

```
📊 ANALYSIS SUMMARY
=====================
📷 Metadata:
  Make: Canon
  Model: Canon EOS 70D
  DateTime: 2020:10:06 16:56:28

📈 Visual Features:
  DPI: (72, 72)
  Entropy: 5.42
  Sharpness: 25.99
  Noise: 0.56
  Brightness: 159.30
  Color Cast: red cast

🎨 Dominant Colors:
  - #F0EFF3
  - #B01111
  - #D0A999

📊 Histogram Stats:
  Red skew: -2.67
  Red kurtosis: 10.21

🕵️ PREDICTION
=====================
From metadata: 2020
```

---

## 🧠 Penjelasan Metodologi

- **Tanpa AI / ML**: Proyek ini murni berbasis statistik visual dan informasi embedded.
- **Heuristik non-AI**: Digunakan _threshold-based rule_ untuk mengelompokkan hasil.
- **Basis deteksi**: DPI rendah + noise tinggi → film era lama; sharpness tinggi + entropi tinggi → era digital.

---

## 📌 Catatan Penting

- Foto hasil **screenshot** atau **AI-generated** sering kali terdeteksi sebagai _ambiguous visual signal_.
- Metadata dapat dimanipulasi, oleh karena itu analisis visual menjadi lebih penting.
- Foto yang terlalu di-*compress* atau diedit ulang dapat kehilangan pola asli.

---

## 💼 Use Case

- Investigasi keaslian foto
- Digital forensics awal
- Edukasi tentang metadata dan visual pattern
- Penelitian fotografi

---

## 🛠️ Teknologi yang Digunakan

| Komponen | Library |
|---------|---------|
| Image Processing | `Pillow`, `OpenCV` |
| Statistik Visual | `scipy`, `numpy` |
| Klasifikasi | Rule-based (pure Python) |
| CLI & I/O | `argparse`, `os`, `sys` |

---

## 📥 Rencana Pengembangan

- [ ] Export ke PDF / CSV
- [ ] GUI untuk pengguna non-teknis
- [ ] Modul benchmark metadata palsu
- [ ] Tambahkan mode batch folder
- [ ] Integrasi command-line-only Android (.sh + Termux-ready)

---

## 📃 Lisensi

Proyek ini dilisensikan di bawah MIT License — silakan gunakan, modifikasi, dan distribusikan dengan bebas.

---

## 👨‍💻 Kontribusi

Kontribusi sangat diterima! Silakan buka pull request atau laporkan bug.

---

## 📬 Kontak

> Mories Deo Hutapea  
> Telegram: [t.me/learningmobileapps](https://t.me/learningmobileapps)  
> Email: moriesdeo574@gmail.com

---
