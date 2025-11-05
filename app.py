# app.py
import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime

st.set_page_config(page_title="Evaluasi Bangun Ruang Sisi Datar", layout="wide")

# ---------- CONFIG ----------
GURU_PASSWORD = "Guru125"
REKAP_FOLDER = "rekapan"

os.makedirs(REKAP_FOLDER, exist_ok=True)

# ---------- QUESTIONS (10 soal cerita kehidupan sehari-hari) ----------
QUESTIONS = [
    {
        "no": 1,
        "soal": "Rina ingin membuat kotak penyimpanan buku dari kayu dengan ukuran panjang 60 cm, lebar 30 cm, tinggi 20 cm. Berapa volume kotak tersebut (cm³)?",
        "options": ["36000 cm³", "3600 cm³", "360000 cm³", "7200 cm³"],
        "answer": "36000 cm³"
    },
    {
        "no": 2,
        "soal": "Sebuah bak tanaman di balkon berukuran 0.8 m × 0.5 m × 0.4 m. Berapa kapasitasnya dalam liter?",
        "options": ["16 L", "160 L", "1600 L", "1.6 L"],
        "answer": "160 L"
    },
    {
        "no": 3,
        "soal": "Pak Budi membuat tenda berbentuk limas segiempat dengan luas alas 2 m² dan tinggi 1,5 m. Berapa volume udara yang bisa masuk (m³)?",
        "options": ["1.0 m³", "0.75 m³", "3.0 m³", "0.5 m³"],
        "answer": "1.0 m³"
    },
    {
        "no": 4,
        "soal": "Sebuah kubus kardus untuk hadiah memiliki diagonal ruang 12 cm. Berapa panjang sisi kardus tersebut (cm)?",
        "options": ["4√3 cm", "6 cm", "12 cm", "8 cm"],
        "answer": "4√3 cm"
    },
    {
        "no": 5,
        "soal": "Sebuah bak mandi berukuran 1.8 m × 0.8 m × 0.5 m diisi 50% saja. Berapa volume air di dalamnya (liter)?",
        "options": ["360 L", "720 L", "180 L", "36 L"],
        "answer": "360 L"
    },
    {
        "no": 6,
        "soal": "Sebuah prisma dengan alas persegi panjang 2 m × 1 m dan tinggi 3 m dijadikan wadah. Berapa luas permukaan seluruhnya (m²)?",
        "options": ["22 m²", "18 m²", "20 m²", "24 m²"],
        "answer": "22 m²"
    },
    {
        "no": 7,
        "soal": "Sebuah kerucut topi ulang tahun memiliki jari-jari 10 cm dan tinggi 24 cm. Volume kerucut kira-kira berapa? (pakai π ≈ 3.14)",
        "options": ["2512 cm³", "1256 cm³", "5024 cm³", "785 cm³"],
        "answer": "2512 cm³"
    },
    {
        "no": 8,
        "soal": "Sebuah botol silinder berdiameter 8 cm dan tinggi 30 cm harus dikemas berdiri. Minimum lebar kotak agar muat adalah?",
        "options": ["8 cm", "16 cm", "30 cm", "4 cm"],
        "answer": "8 cm"
    },
    {
        "no": 9,
        "soal": "Atap limas segiempat mempunyai tiap sisi segitiga dengan alas 5 m dan tinggi 3 m. Berapa luas total 4 sisi atap tersebut (m²)?",
        "options": ["30 m²", "15 m²", "60 m²", "12 m²"],
        "answer": "30 m²"
    },
    {
        "no": 10,
        "soal": "Paket berbentuk kubus sisi 40 cm akan dibungkus. Jika satu lembar kertas 0.5 m × 0.7 m, berapa lembar minimum diperlukan?",
        "options": ["2 lembar", "3 lembar", "1 lembar", "4 lembar"],
        "answer": "3 lembar"
    }
]

# ---------- Helpers ----------
def compute_results(answers_list):
    """
    answers_list: list of selected answers in same order as QUESTIONS
    returns list of booleans and score (count correct)
    """
    correct_flags = []
    correct_count = 0
    for i, q in enumerate(QUESTIONS):
        ans = answers_list[i]
        is_correct = (ans == q["answer"])
        correct_flags.append(is_correct)
        if is_correct:
            correct_count += 1
    return correct_flags, correct_count

def df_from_submission(name, kelas, answers_list, reasons_list):
    flags, correct_count = compute_results(answers_list)
    rows = []
    for i, q in enumerate(QUESTIONS):
        rows.append({
            "Nama": name,
            "Kelas": kelas,
            "No": q["no"],
            "Soal": q["soal"],
            "Jawaban Siswa": answers_list[i],
            "Jawaban Benar": q["answer"],
            "Benar": "YA" if flags[i] else "TIDAK",
            "Alasan": reasons_list[i]
        })
    df = pd.DataFrame(rows)
    df["Skor_Benar"] = df["Benar"].map({"YA": 1, "TIDAK": 0})
    total_correct = flags.count(True)
    df_summary = {
        "total_correct": total_correct,
        "total_questions": len(QUESTIONS),
        "percent": round(total_correct / len(QUESTIONS) * 100, 2)
    }
    return df, df_summary

def excel_bytes_from_df(df):
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)
    return buffer

# ---------- UI ----------
st.title("Evaluasi: Bangun Ruang Sisi Datar — 10 Soal (Cerita)")
st.write("Pilih peran dan ikuti instruksi. Jawaban awal **kosong**; siswa harus memilih setiap soal sebelum mengirim.")

role = st.sidebar.selectbox("Peran", ["Siswa", "Guru"])

# ----------------- SISWA -----------------
if role == "Siswa":
    st.header("🧑‍🎓 Form Siswa")
    name = st.text_input("Nama lengkap")
    kelas = st.text_input("Kelas / ID (opsional)")

    st.markdown("---")
    st.write("Jawaban awal diset **kosong**. Pilih jawaban pada setiap soal lalu tekan tombol kirim.")

    # use selectbox with initial blank option so answer is empty initially
    answers = []
    reasons = []
    for q in QUESTIONS:
        st.subheader(f"Soal {q['no']}")
        st.write(q["soal"])
        options = [""] + q["options"]  # blank first so initial = ""
        sel = st.selectbox("Pilih jawaban:", options, key=f"q_{q['no']}")
        reason = st.text_area("Tuliskan alasan singkat (opsional):", key=f"r_{q['no']}", height=80)
        answers.append(sel)
        reasons.append(reason)
        st.markdown("---")

    if st.button("Kirim Jawaban"):
        # validation
        if not name.strip():
            st.warning("Mohon isi nama terlebih dahulu.")
        elif any(a == "" for a in answers):
            st.warning("Masih ada soal yang belum dijawab. Mohon jawab semua soal sebelum mengirim.")
        else:
            # build df and save to disk for guru
            df, summary = df_from_submission(name, kelas, answers, reasons)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
            filename = f"{safe_name}_{kelas}_{timestamp}.xlsx" if kelas.strip() else f"{safe_name}_{timestamp}.xlsx"
            filepath = os.path.join(REKAP_FOLDER, filename)
            df.to_excel(filepath, index=False, engine="openpyxl")

            # provide student download (single submission file)
            excel_buf = excel_bytes_from_df(df)
            st.success(f"Jawaban terkirim. Skor: {summary['total_correct']} / {summary['total_questions']} ({summary['percent']}%)")
            st.info("Hasil disimpan. Hanya guru yang dapat melihat rekap semua siswa.")
            st.download_button("📥 Unduh Hasilmu (Excel)", data=excel_buf, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ----------------- GURU -----------------
else:
    st.header("👩‍🏫 Panel Guru (Akses dilindungi)")
    if "guru_authed" not in st.session_state:
        st.session_state.guru_authed = False

    if not st.session_state.guru_authed:
        pwd = st.text_input("Masukkan password guru:", type="password")
        if st.button("Masuk sebagai Guru"):
            if pwd == GURU_PASSWORD:
                st.session_state.guru_authed = True
                st.success("Password benar. Selamat datang, Guru.")
            else:
                st.error("Password salah.")
        st.stop()

    # authenticated: show rekap
    st.success("Anda login sebagai Guru.")
    files = sorted([f for f in os.listdir(REKAP_FOLDER) if f.endswith(".xlsx")])
    if len(files) == 0:
        st.info("Belum ada hasil siswa yang terkumpul.")
    else:
        st.subheader("Daftar file hasil siswa")
        selected = st.selectbox("Pilih file:", ["(gabungan semua)"] + files)
        if selected == "(gabungan semua)":
            # combine all files into one DF
            combined = []
            for f in files:
                try:
                    dfi = pd.read_excel(os.path.join(REKAP_FOLDER, f))
                    combined.append(dfi)
                except Exception as e:
                    st.warning(f"Gagal membaca {f}: {e}")
            if combined:
                df_all = pd.concat(combined, ignore_index=True)
                # compute per-student summary
                summary = df_all.groupby(["Nama", "Kelas"]).agg(
                    total_correct=pd.NamedAgg(column="Skor_Benar", aggfunc="sum"),
                    total_questions=pd.NamedAgg(column="No", aggfunc="count")
                ).reset_index()
                summary["percent"] = (summary["total_correct"] / summary["total_questions"] * 100).round(2)
                st.write("Ringkasan per siswa:")
                st.dataframe(summary)
                # download combined excel
                buf = excel_bytes_from_df(df_all)
                st.download_button("📥 Unduh Semua Rekap (Excel)", data=buf, file_name="rekap_semua_siswa.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                st.markdown("---")
                st.write("Rekap detail (gabungan semua siswa):")
                st.dataframe(df_all)
            else:
                st.info("Tidak ada file yang bisa digabungkan.")
        else:
            path = os.path.join(REKAP_FOLDER, selected)
            try:
                df = pd.read_excel(path)
                st.subheader(f"Isi file: {selected}")
                st.dataframe(df)
                # compute simple stats
                correct_total = int(df["Skor_Benar"].sum()) if "Skor_Benar" in df.columns else df["Benar"].map({"YA":1,"TIDAK":0}).sum()
                total_q = len(QUESTIONS)
                percent = round(correct_total / total_q * 100, 2)
                st.write(f"Skor total (per file): {correct_total} / {total_q} → {percent}%")
                # download selected file
                with open(path, "rb") as f:
                    st.download_button("📥 Unduh File Ini (Excel)", data=f, file_name=selected, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                # also provide direct relative link (berfungsi jika server/host mengizinkan akses file)
                st.markdown(f"**Link file (relatif):** [rekap/{selected}](rekap/{selected})")
            except Exception as e:
                st.error(f"Gagal membuka file: {e}")

st.markdown("---")
st.caption("Evaluasi Bangun Ruang Sisi Datar — dibuat untuk pembelajaran berpikir kritis")
