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
        "pertanyaan": "1. Sebuah akuarium berbentuk balok memiliki panjang 80 cm, lebar 40 cm, dan tinggi 50 cm. Jika akuarium diisi air penuh, berapa liter air yang dibutuhkan?",
        "opsi": ["120 liter", "160 liter", "200 liter", "240 liter", "320 liter"],
        "jawaban": "160 liter"
    },
    {
        "pertanyaan": "2. Sebuah tenda pramuka berbentuk prisma segitiga memiliki alas segitiga dengan panjang alas 4 m dan tinggi segitiga 3 m, serta panjang prisma 5 m. Hitung volume tenda tersebut!",
        "opsi": ["25 m³", "30 m³", "35 m³", "40 m³", "45 m³"],
        "jawaban": "30 m³"
    },
    {
        "pertanyaan": "3. Sebuah bak mandi berbentuk kubus dengan panjang rusuk 1 meter. Jika diisi penuh, berapa volume air di dalam bak mandi?",
        "opsi": ["1 liter", "10 liter", "100 liter", "1000 liter", "1 m³"],
        "jawaban": "1 m³"
    },
    {
        "pertanyaan": "4. Sebuah kardus berbentuk balok memiliki ukuran panjang 50 cm, lebar 30 cm, dan tinggi 40 cm. Berapa luas karton yang dibutuhkan untuk menutup seluruh permukaan kardus?",
        "opsi": ["0.52 m²", "0.56 m²", "0.60 m²", "0.64 m²", "0.68 m²"],
        "jawaban": "0.64 m²"
    },
    {
        "pertanyaan": "5. Sebuah menara air berbentuk tabung memiliki jari-jari 1,5 m dan tinggi 4 m. Hitung volume air di dalam menara!",
        "opsi": ["18π m³", "20π m³", "25π m³", "30π m³", "35π m³"],
        "jawaban": "18π m³"
    },
    {
        "pertanyaan": "6. Sebuah kolam renang berbentuk balok berukuran 10 m × 4 m × 2 m. Jika 1 m³ setara dengan 1000 liter, berapa liter air yang dibutuhkan agar kolam penuh?",
        "opsi": ["4000 liter", "8000 liter", "20000 liter", "40000 liter", "80000 liter"],
        "jawaban": "80000 liter"
    },
    {
        "pertanyaan": "7. Sebuah tiang listrik berbentuk tabung dengan jari-jari 0,2 m dan tinggi 6 m. Hitung luas permukaan tiang!",
        "opsi": ["7.2π m²", "7.5π m²", "8π m²", "8.4π m²", "9π m²"],
        "jawaban": "8.4π m²"
    },
    {
        "pertanyaan": "8. Sebuah dus kue berbentuk kubus memiliki panjang sisi 30 cm. Jika akan dilapisi kertas kado seluruhnya, berapa luas kertas minimal yang dibutuhkan?",
        "opsi": ["0.36 m²", "0.40 m²", "0.48 m²", "0.54 m²", "0.60 m²"],
        "jawaban": "0.54 m²"
    },
    {
        "pertanyaan": "9. Sebuah tangki minyak berbentuk prisma segitiga dengan luas alas 2 m² dan tinggi 3 m. Berapa volume tangki minyak?",
        "opsi": ["4 m³", "5 m³", "6 m³", "7 m³", "8 m³"],
        "jawaban": "6 m³"
    },
    {
        "pertanyaan": "10. Sebuah kemasan susu berbentuk balok dengan ukuran 10 cm × 6 cm × 20 cm. Jika 1 cm³ = 1 ml, berapa volume susu tersebut?",
        "opsi": ["100 ml", "600 ml", "1200 ml", "2400 ml", "3000 ml"],
        "jawaban": "1200 ml"
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

