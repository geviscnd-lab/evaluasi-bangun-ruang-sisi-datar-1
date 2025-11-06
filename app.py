import streamlit as st
import pandas as pd
import os

# === Konfigurasi awal ===
st.set_page_config(page_title="Evaluasi Bangun Ruang Sisi Datar", layout="centered")
PASSWORD_GURU = "Guru125"
EXCEL_PATH = "rekapan/hasil_evaluasi.xlsx"

# === Data Soal (soal cerita kehidupan sehari-hari) ===
soal_list = [
    {
        "pertanyaan": "1. Sebuah akuarium berbentuk balok berukuran panjang 60 cm, lebar 40 cm, dan tinggi 50 cm. Akuarium akan diisi air penuh. Berapa volume air yang dapat ditampung akuarium tersebut dalam liter? (1 liter = 1000 cm³) ?",
        "opsi": ["100 liter", "120 liter", "130 liter", "140 liter", "150 liter"],
        "jawaban": "120 liter"
    },
    {
        "pertanyaan": "2. Sebuah kotak kue berbentuk kubus memiliki panjang sisi 25 cm. Jika akan dilapisi kertas kado seluruh permukaan, berapa luas kertas minimal yang dibutuhkan?",
        "opsi": ["2500 cm³", "3750 cm³", "4000 cm³", "4500 cm³", "5000 cm³"],
        "jawaban": "4500 m³"
    },
    {
        "pertanyaan": "3. Seorang tukang membuat atap rumah berbentuk limas segi empat beraturan dengan panjang sisi alas 6 m dan tinggi limas 4 m. Berapa volume atap yang dibuat?",
        "opsi": ["36 m³", "40 m³", "48 m³", "50m³", "60 m³"],
        "jawaban": "48 m³"
    },
    {
        "pertanyaan": "4. Sebuah wadah mainan berbentuk balok memiliki ukuran 50 cm × 30 cm × 20 cm. Jika wadah ingin dicat seluruh sisinya bagian luar, berapa luas permukaan yang akan dicat?",
        "opsi": ["4.600 cm²", "5000 m²", "5200 m²", "5600 m²", "6000 m²"],
        "jawaban": "5600 m²"
    },
    {
        "pertanyaan": "5. Sebuah tenda pramuka berbentuk prisma segitiga memiliki alas segitiga dengan alas 4 m, tinggi 3 m, dan panjang prisma 5 m. Berapa volume tenda tersebut?",
        "opsi": ["25 m³", "27 m³", "28 m³", "30 m³", "35 m³"],
        "jawaban": "30 m³"
    },
    {
        "pertanyaan": "6. Sebuah miniatur menara berbentuk limas segi empat mempunyai panjang sisi alas 10 cm dan tinggi 15 cm. Berapa volume miniatur tersebut?",
        "opsi": ["400 cm³", "450 cm³", "500 cm³", "550 cm³", "600 cm³"],
        "jawaban": "500 cm³"
    },
    {
        "pertanyaan": "7. Seorang tukang membuat tenda pesta berbentuk prisma segitiga. Jika luas alasnya 12 m² dan panjang prisma 8 m, berapa volume udara di dalam tenda?",
        "opsi": ["80 m³", "85 m³", "90 m³", "96 m³", "100 m³"],
        "jawaban": "96 m³"
    },
    {
        "pertanyaan": "8. Sebuah atap limas segitiga memiliki alas berbentuk segitiga sama kaki dengan alas 10 m, tinggi segitiga 6 m, dan tinggi limas 8 m. Hitung volume atap tersebut!",
        "opsi": ["80 m³", "100 m³", "120 m³", "160 m³", "200 m³"],
        "jawaban": "100 m³"
    },
    {
        "pertanyaan": "9. Sebuah lemari berbentuk balok memiliki panjang 1,2 m, lebar 0,8 m, dan tinggi 2 m. Tukang kayu ingin menutup seluruh sisi luar lemari dengan lembaran kayu. Berapa luas kayu yang diperlukan?",
        "opsi": ["7,68 m²", "8,0 m²", "8,32 m²", "8,64 m²", "9,0 m²"],
        "jawaban": "7,68 m²"
    },
    {
        "pertanyaan": "10. Sebuah hiasan meja berbentuk kubus kecil dengan rusuk 10 cm akan dicat seluruh sisinya. Jika satu kaleng cat bisa menutupi 600 cm², berapa banyak kaleng cat minimal yang dibutuhkan untuk 10 hiasan meja?",
        "opsi": ["2", "3", "4", "5", "6"],
        "jawaban": "5"
    }
]

# === Input login role ===
st.title("🧮 Evaluasi Bangun Ruang Sisi Datar")

role = st.radio("Pilih peran:", ["Siswa", "Guru"])

# === Mode Guru ===
if role == "Guru":
    password = st.text_input("Masukkan Password:", type="password")
    if password == PASSWORD_GURU:
        st.success("Login Guru berhasil ✅")
        if os.path.exists(EXCEL_PATH):
            df = pd.read_excel(EXCEL_PATH)
            st.dataframe(df)
            with open(EXCEL_PATH, "rb") as f:
                st.download_button("📥 Download Rekapan Excel", f, file_name="hasil_evaluasi.xlsx")
        else:
            st.warning("Belum ada data hasil siswa.")
    else:
        st.error("Password salah atau belum diisi.")

# === Mode Siswa ===
elif role == "Siswa":
    nama = st.text_input("Nama Lengkap:")
    absen = st.text_input("Nomor Absen:")
    st.info("Jawablah semua soal berikut, pastikan semua jawaban terisi sebelum dikirim.")
    
    # Input jawaban siswa
    jawaban_siswa = []
    for i, soal in enumerate(soal_list):
        jawaban = st.radio(soal["pertanyaan"], soal["opsi"], index=None, key=f"soal_{i}")
        jawaban_siswa.append(jawaban)
    
    if st.button("Kirim Jawaban"):
        if "" in [j if j else "" for j in jawaban_siswa]:
            st.error("❌ Harap isi semua jawaban terlebih dahulu!")
        elif not nama or not absen:
            st.error("❌ Harap isi nama dan nomor absen!")
        else:
            hasil = []
            benar = 0
            for i, soal in enumerate(soal_list):
                status = "Benar" if jawaban_siswa[i] == soal["jawaban"] else "Salah"
                hasil.append(status)
                if status == "Benar":
                    benar += 1
            
            skor = round((benar / len(soal_list)) * 100, 2)
            st.success(f"✅ Jawaban terkirim! Nilai Anda: {skor}")
            
            # Simpan ke Excel (1 file untuk semua siswa)
            data = {
                "Nama": [nama],
                "Absen": [absen],
                "Nilai": [skor],
                **{f"Soal {i+1}": [hasil[i]] for i in range(len(soal_list))}
            }

            df_new = pd.DataFrame(data)
            if os.path.exists(EXCEL_PATH):
                df_existing = pd.read_excel(EXCEL_PATH)
                df_final = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_final = df_new
            
            os.makedirs("rekapan", exist_ok=True)
            df_final.to_excel(EXCEL_PATH, index=False)
            st.info("Jawaban Anda telah disimpan. Guru akan menilai keseluruhan hasil.")

