import streamlit as st
import time
import numpy as np

if st.button("Kembali ke Beranda", type='primary'):
    st.switch_page(st.session_state.page_home)

nilai = ["A", "B", "C", "E"]

minat_bakat = [
    "1. Saya tertarik memahami pola dan hubungan yang muncul dari data.",
    "2. Saya merasa puas ketika berhasil menemukan cara kerja suatu metode.",
    "3. Saya senang mengerjakan tugas yang membutuhkan ketelitian tinggi.",
    "4. Saya tertarik menggunakan perangkat lunak untuk mengolah data.",
    "5. Saya senang menyelesaikan masalah yang punya tahapan penyelesaian yang jelas.",
    "6. Saya tertarik mempelajari bagaimana data digunakan untuk mendukung keputusan.",
    "7. Saya suka membandingkan beberapa cara berbeda untuk menyelesaikan masalah.",
    "8. Saya tertarik mempelajari risiko, perubahan, atau ketidakpastian dalam situasi nyata.",
    "9. Saya menikmati tugas yang menghubungkan teori dengan contoh kasus.",
    "10. Saya tertarik pada kegiatan belajar yang melibatkan angka, pola, dan analisis."
]

penilaian_diri = [
    "1. Saya mampu memahami materi yang rumit setelah membaca dan berlatih sendiri.",
    "2. Saya percaya diri mengerjakan soal yang memerlukan beberapa langkah perhitungan.",
    "3. Saya mampu menyelesaikan tugas kuliah meskipun topiknya baru bagi saya.",
    "4. Saya cukup percaya diri menggunakan software statistik atau alat analisis data dasar.",
    "5. Saya cenderung menghindari tugas yang membutuhkan banyak perhitungan.",
    "6. Saya dapat memperbaiki kesalahan setelah mencoba beberapa kali.",
    "7. Saya mampu menjelaskan hasil analisis secara runtut kepada orang lain.",
    "8. Saya bisa membagi masalah besar menjadi langkah-langkah kecil yang lebih mudah dikerjakan.",
    "9. Saya tetap fokus saat mengerjakan tugas akademik yang panjang.",
    "10. Saya mudah menyerah ketika tidak langsung memahami materi yang sulit.",
]

matkul_col1 = [
    ("TP", "violet", "Teori Peluang"),
    ("KD", "green", "Kalkulus Diferensial"),
    ("SM", "blue", "Statistika Matematika"),
    ("MS", "orange", "Metode Statistika"),
    ("PL", "violet", "Program Linier"),
    ("ARW", "green", "Analisis Runtun Waktu"),
    ("AP", "red", "Algoritma Pemrograman")
]

matkul_col2 = [
    ("AL", "blue", "Aljabar Linear"),
    ("KI", "orange", "Kalkulus Integral"),
    ("AR", "green", "Analisis Regresi"),
    ("PDS", "red", "Pengantar Data Sains"),
    ("MR", "green", "Metode Numerik"),
    ("ADK", "blue", "Analisis Data Kategorik"),
    ("ADE", "violet", "Analisis Data Eksploratif")
]

GRADE_MAP = {
    "A": 1.00,
    "B": 0.75,
    "C": 0.50,
    "E": 0.00
}

DIMENSI_MK = {
    "Teori": ["TP", "KD", "KI", "AL", "SM", "MS"],
    "Komputasi": ["AP", "MR", "PDS", "ADE", "ADK"],
    "Terapan": ["MS", "AR", "ADK", "ADE", "PL"],
    "Keuangan": ["AL", "KD", "KI", "PL", "ARW"]
}

def star_score(x):
    return (x + 1) / 5

MINAT_WEIGHT = np.array([
    [0.4,0.2,0.4,0.0],
    [0.5,0.0,0.0,0.5],
    [0.3,0.0,0.4,0.3],
    [0.0,0.8,0.2,0.0],
    [0.2,0.2,0.4,0.2],
    [0.0,0.3,0.7,0.0],
    [0.3,0.3,0.2,0.2],
    [0.1,0.0,0.2,0.7],
    [0.4,0.0,0.4,0.2],
    [0.3,0.3,0.2,0.2]
])

SELF_WEIGHT = np.array([
    [0.4,0.2,0.2,0.2],
    [0.4,0.2,0.0,0.4],
    [0.3,0.2,0.3,0.2],
    [0.0,0.8,0.2,0.0],
    [0.3,0.2,0.3,0.2],
    [0.2,0.3,0.3,0.2],
    [0.4,0.0,0.4,0.2],
    [0.3,0.3,0.2,0.2],
    [0.3,0.1,0.4,0.2],
    [0.2,0.2,0.2,0.4]
])

def calculate_probability_state(akademik,MinBak,PenDir):
    # AKADEMIK
    ipk_score = akademik["IPK"] / 4
    sks_score = akademik["SKS"] / 144

    akademik_score = []

    for matkul in DIMENSI_MK.values():
        nilai_matkul = np.mean([
            GRADE_MAP[akademik[kode]]
            for kode in matkul
        ])

        skor = (
            0.65 * nilai_matkul +
            0.25 * ipk_score +
            0.1 * sks_score
        )
        akademik_score.append(skor)

    akademik_score = np.array(akademik_score)

    # MINAT & BAKAT
    minat_vector = np.array([(v + 1) / 5 for v in MinBak.values()])
    minat_score = minat_vector @ MINAT_WEIGHT
    minat_score /= MINAT_WEIGHT.sum(axis=0)

    # PENILAIAN DIRI
    self_vector = np.array([(v + 1) / 5 for v in PenDir.values()])
    # reverse item
    self_vector[[4, 9]] = 1 - self_vector[[4, 9]]
    self_score = self_vector @ SELF_WEIGHT
    self_score /= SELF_WEIGHT.sum(axis=0)

    # =====================
    # SKOR AKHIR
    # =====================
    raw_score = (0.5 * akademik_score + 0.25 * minat_score + 0.25 * self_score)
    prob = raw_score / raw_score.sum()
    return np.array(prob)


with st.form("form_kuesioner", clear_on_submit=False):
    st.title("Form Kuesioner", text_alignment='center')

    st.header('Akademik')
    col1, col2 = st.columns(2)
    IPK = col1.number_input("Berapa IPK anda saat ini?", min_value=0.00, max_value=4.00, step=0.1)
    SKS = col2.number_input("Berapa Jumlah SKS yang sudah anda tempuh?", min_value=1, max_value=144, step=1)

    jawaban_akademik = {
        "IPK":IPK,
        "SKS":SKS
    }

    with col1:
        for kode, warna, nama in matkul_col1:
            jawaban_akademik[kode] = st.segmented_control(
                f"Berapa nilai mata kuliah :{warna}[**{nama}**] Anda?", 
                options=nilai,
                key=f"input_{kode}"
            )

    with col2:
        for kode, warna, nama in matkul_col2:
            jawaban_akademik[kode] = st.segmented_control(
                f"Berapa nilai mata kuliah :{warna}[**{nama}**] Anda?", 
                options=nilai,
                key=f"input_{kode}"
            )
    
    st.divider()

    st.header("Minat dan Bakat")
    jawaban_MinBak = {}
    col3, col4 = st.columns(2, gap='medium')
    for i, pertanyaan1 in enumerate(minat_bakat):
        if i%2 == 0:
            with col3.container(height=130, border=False):
                st.write(f"**{pertanyaan1}**")
                jawaban_MinBak[pertanyaan1] = st.feedback("stars", key=f"q1_{i}")
        else:
            with col4.container(height=130, border=False):
                st.write(f"**{pertanyaan1}**")
                jawaban_MinBak[pertanyaan1] = st.feedback("stars", key=f"q1_{i}")

    st.divider()

    st.header("Penilaian Diri")
    jawaban_PenDir = {}
    col3, col4 = st.columns(2, gap='medium')
    for i, pertanyaan2 in enumerate(penilaian_diri):
        if i%2 == 0:
            with col3.container(height=130, border=False):
                st.write(f"**{pertanyaan2}**")
                jawaban_PenDir[pertanyaan2] = st.feedback("stars", key=f"q2_{i}")
        else:
            with col4.container(height=130, border=False):
                st.write(f"**{pertanyaan2}**")
                jawaban_PenDir[pertanyaan2] = st.feedback("stars", key=f"q2_{i}")

    if st.form_submit_button("✅SUBMIT", width='stretch', type="primary"):
        if None in jawaban_akademik.values() or None in jawaban_MinBak.values() or None in jawaban_PenDir.values():
            st.error("Mohon berikan rating bintang dan nilai mata kuliah pada semua kriteria sebelum menyimpan!")
        else:
            prob = calculate_probability_state(jawaban_akademik, jawaban_MinBak, jawaban_PenDir)
            
            with st.status("Proses data...", expanded=True) as status:
                st.write("Proses Data Akademik...")
                st.session_state.ipk = jawaban_akademik["IPK"]
                time.sleep(1)
                st.write("Proses Data Minat dan Bakat...")
                st.session_state.sks = jawaban_akademik["SKS"]
                time.sleep(1)
                st.write("Proses Data Penilaian Diri...")
                st.session_state.hasil_kuesioner = True
                time.sleep(1)
                status.update(
                    label="Berhasil Menyimpan!", state="complete", expanded=True
                )
                
            st.session_state.prob = prob
            with st.spinner("Mengarahkan ke dashboard utama..."):
                time.sleep(2)
            st.switch_page(st.session_state.page_dashboard)