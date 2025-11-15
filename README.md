# evaluasi-bangun-ruang-sisi-datar-story

Streamlit app: Evaluasi Bangun Ruang Sisi Datar (10 soal cerita kehidupan sehari-hari).
- Role: Siswa & Guru (password Guru125)
- Hasil siswa disimpan di folder `rekapan/` dan dapat diunduh sebagai Excel.
- Guru dapat melihat semua rekap dan mengunduh gabungan.
- Jawaban awal siswa kosong (harus dipilih).

## Run locally
1. pip install -r requirements.txt
2. python3 -m streamlit run app.py
3. Buka browser ke http://localhost:8501

## Notes
- Untuk Codespaces / deployment, forward port dan pastikan folder `rekapan` writable.
- Link relatif ke file `rekap/<filename>` disertakan pada panel guru (akses tergantung hosting).

## 📊 Analisis Kemampuan Siswa (Google Colab)

Notebook berikut digunakan untuk menganalisis hasil pekerjaan siswa:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/geviscnd-lab/evaluasi-bangun-ruang-sisi-datar-1/blob/main/analisis_kemampuan_siswa.ipynb)
