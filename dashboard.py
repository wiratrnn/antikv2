import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from utils import *

medali = {1: "🥇", 
          2: "🥈",
          3: "🥉",
          4: "🏅"}

warna = ["#f97316","#3b82f6", "#22c55e", "#8b5cf6"]

if "prob" not in st.session_state:
    st.session_state.prob = np.array([0.108, 0.327, 0.342, 0.223])

keterangan = [
        "Sangat Direkomendasikan",
        "Direkomendasikan",
        "Cukup Direkomendasikan",
        "Kurang Direkomendasikan"
    ]

payoff_matrix = pd.DataFrame({
        "Alternatif" :["Terapan", "Komputasi", "Keuangan", "Teori"],
        "State1": [80,85,70,95],
        "State2": [75,95,75,70],
        "State3": [65,70,95,65],
        "State4": [95,65,60,80]
    }).set_index("Alternatif")

if "df_payoff" not in st.session_state:
    st.session_state.df_payoff = payoff_matrix

ev_values, ranking = calculate_ev(st.session_state.df_payoff, st.session_state.prob)

st.session_state.rekomendasi = f"Statistika {ranking[ranking == 1].index[0]}"
st.session_state.skor_tertinggi = np.max(ev_values)

if "hasil_kuesioner" not in st.session_state:
    st.session_state.ipk = 3.87
    st.session_state.sks = 104

st.title("📊 Dashboard AnTikV2", text_alignment='center')

if st.button("Kembali ke Beranda", type='primary'):
    st.switch_page(st.session_state.page_home)

st.caption("Jika sebelumnya anda tidak mengisi kuesioner, maka nilai yang tampil disini adalah nilai *default*. Untuk hasil yang lebih akurat, pastikan untuk mengisi kuesioner terlebih dahulu.")

tab1, tab2, tab3 = st.tabs(["Hasil Keputusan", "Decision Under Risk", "Simulasi Monte Carlo"])

with tab1:
    st.title("🎓 Rekomendasi Penjurusan Anda", text_alignment='center')
    col_A, col_B = st.columns([0.35,0.65], gap='small')
    col_A.metric_card("IPK anda", st.session_state.ipk, bg_color="#e38ef8", accent_color="#880092", 
                      subtext=("Cumlaude" if st.session_state.ipk >= 3.75 else "Sangat baik" if st.session_state.ipk >= 3.50 else "Memuaskan" if st.session_state.ipk >= 3.00 else"Cukup"),
                    icon="<img width='48' height='48' src='https://img.icons8.com/forma-light-sharp/48/C850F2/graduation-cap.png' alt='graduation-cap'/>")
    col_A.metric_card("Total SKS", st.session_state.sks, bg_color="#22C3E6", accent_color="#0000FF", subtext="SKS",
                    icon="<img width='50' height='50' src='https://img.icons8.com/ios/50/22C3E6/open-book--v1.png' alt='open-book--v1'/>")
    col_B.metric_card("Skor Kecocokan Tertinggi", f"{st.session_state.skor_tertinggi:.2f}", bg_color="#9FDDAA", accent_color="#40C057", subtext="Expected Value",
                    icon="<img width='48' height='48' src='https://img.icons8.com/forma-regular/48/40C057/graph.png' alt='graph'/>")
    col_B.metric_card("Rekomendasi Utama", st.session_state.rekomendasi, bg_color="#FFB67A", accent_color="#FF7D00", subtext="Penjurusan Terbaik Untuk Anda",
                    icon="<img width='48' height='48' src='https://img.icons8.com/softteal-line/48/FD7E14/star.png' alt='star'/>")

    ### rekomendasi peminatan
    col1, col2 = st.columns(2, gap='small', border=True)
    col1.subheader("🏆 Rekomendasi Peminatan")
    sorted_idx = np.argsort(ev_values)[::-1]
    rec_score = softmax(ev_values, 35)*100

    for rank, idx in enumerate(sorted_idx, start=1):
        col1.recommendation_card(
            medali[rank],
            st.session_state.df_payoff.index[idx],
            rec_score[idx],
            warna[rank-1],
            keterangan[rank-1]
        )

    ### probabilitas karir
    fig = px.pie(
        names=[
            "Akademisi",
            "Data Science",
            "Quality Control",
            "Aktuaris"
        ],
        values=st.session_state.prob*10,
        hole=0.55
    )

    fig.update_traces(
        textinfo="percent",
        textposition="inside",
        marker=dict(
            colors=px.colors.qualitative.G10[:4]
        )
    )

    fig.update_layout(
        title="Peluang karir (state)",
        height=200,
        margin=dict(t=50, b=0, l=0, r=1),

        legend=dict(
            orientation="v",
            y=0.5,
            yanchor="middle",
            x=1,
            xanchor="left"
        ),

        annotations=[
            dict(
                text="Karir",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=20)
            )
        ]
    )

    col2.plotly_chart(fig)

    # Data
    df = pd.DataFrame({
        "Komponen": [
            "Terapan",
            "Komputasi",
            "Keuangan",
            "Teori",
            "Terapan"
        ],
        "Profil Anda": [*ev_values, ev_values[0]],
        "Rata-rata Mahasiswa": [60, 75, 40, 65, 60]
    })

    # Ubah ke format long
    df_long = df.melt(
        id_vars="Komponen",
        var_name="Kelompok",
        value_name="Skor"
    )

    ### Radar Map
    fig = px.line_polar(
        df_long,
        r="Skor",
        theta="Komponen",
        color="Kelompok",
        line_close=True,
        color_discrete_map={
            "Profil Anda": "#3B82F6",
            "Rata-rata Mahasiswa": "#333A44"
        }
    )
    fig.update_traces(fill="toself")
    fig.update_layout(
        title="Radar Kompetensi",
        height=280,
        margin=dict(
            l=10,
            r=10,
            t=40,
            b=40
        ),
        polar=dict(
            domain=dict(
                x=[0.1, 0.9],
                y=[0.1, 0.9]
            ),
            radialaxis=dict(
                range=[0, 100],
                dtick=25,
                showticklabels=False,
                ticks="",
                gridcolor="#E5E7EB",
                gridwidth=1
            ),
            angularaxis=dict(
                gridcolor="#E5E7EB",
                linecolor="#E5E7EB",
                tickfont=dict(size=11)
            )
        ),
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.1
        )
    )

    col2.plotly_chart(fig)

with tab2:
    ### payoff matrix
    colData, colInfo = st.columns([0.65,0.35])
    with colData:
        st.title("📈 Matriks Payoff", text_alignment='center')
        st.session_state.df_payoff = st.data_editor(
            st.session_state.df_payoff,
            width=450,
            height=178,
            key="payoff_DUR"
        )
        st.button("Generate Random Payoff", 
                  on_click=lambda: st.session_state.update(
                      {"df_payoff": pd.DataFrame({"Alternatif" :["Terapan", "Komputasi", "Keuangan", "Teori"],
                                                    "State1": np.random.randint(0, 100, 4),
                                                    "State2": np.random.randint(0, 100, 4),
                                                    "State3": np.random.randint(0, 100, 4),
                                                    "State4": np.random.randint(0, 100, 4)}).set_index("Alternatif")}
                                                )
                )

    with colInfo.container(border=True, height=320):
        st.markdown("##### Informasi Tambahan")
        with st.expander("📖 Keterangan State", expanded=False):
            st.markdown("""
            **State** merupakan kondisi atau kemungkinan jalur karir yang dapat ditempuh oleh mahasiswa setelah lulus. 
            Pada sistem ini, state digunakan sebagai representasi ketidakpastian masa depan yang menjadi dasar dalam perhitungan *Expected Value (EV)* dan *Expected Utility (EU)*.

            Probabilitas setiap state diperoleh dari hasil pengisian kuesioner yang mencerminkan profil akademik, minat, dan penilaian diri mahasiswa.

            **Keterangan setiap state:**
            - **State 1 – Akademisi/Peneliti**  
            Cocok bagi mahasiswa yang memiliki ketertarikan pada teori statistika, penelitian, pendidikan, dan pengembangan ilmu pengetahuan.

            - **State 2 – Data Science**  
            Cocok bagi mahasiswa yang tertarik pada pemrograman, data mining, machine learning, kecerdasan buatan, dan analisis data berskala besar.

            - **State 3 – Quality Control**  
            Cocok bagi mahasiswa yang tertarik pada pengendalian kualitas, optimasi proses, analisis produksi, dan pengambilan keputusan berbasis data di industri.

            - **State 4 – Aktuaris**  
            Cocok bagi mahasiswa yang tertarik pada analisis risiko, keuangan, asuransi, investasi, dan pemodelan probabilistik.

            **Catatan:**  
            State bukan merupakan pilihan peminatan, melainkan gambaran kemungkinan arah karir di masa depan. Sistem akan mengevaluasi setiap alternatif peminatan terhadap seluruh state untuk menghasilkan rekomendasi yang paling sesuai.
            """)

        with st.expander("ℹ️ Bagaimana Rekomendasi Dihasilkan?", expanded=False):
            st.markdown("""
            Sistem menghitung tingkat kecocokan setiap alternatif peminatan menggunakan matriks payoff dan probabilitas state yang diperoleh dari hasil kuesioner.

            Alternatif yang dievaluasi:
            - Statistika Terapan
            - Statistika Komputasi
            - Statistika Keuangan
            - Statistika Teori

            Semakin tinggi nilai EV atau EU yang diperoleh suatu alternatif, semakin tinggi tingkat rekomendasinya terhadap profil mahasiswa yang bersangkutan.
            """)

    st.title("Perhitungan EV dan EU", text_alignment='center')
    with st.expander("📊 Apa itu Expected Value (EV) dan Expected Utility (EU)?", expanded=False):
        st.markdown("""
        ### Expected Value (EV)

        **Expected Value (EV)** adalah metode untuk menghitung nilai harapan dari setiap alternatif peminatan berdasarkan peluang terjadinya setiap state (jalur karir).

        Secara sederhana, EV menjawab pertanyaan:

        > *"Jika saya memilih peminatan ini, berapa nilai rata-rata yang saya harapkan berdasarkan kemungkinan karir yang dapat terjadi di masa depan?"*

        Perhitungan EV dilakukan dengan mengalikan setiap nilai payoff dengan probabilitas state, kemudian menjumlahkannya.

        **Rumus EV:**

        EV = Σ (Probabilitas State × Payoff)

        Semakin besar nilai EV, semakin baik alternatif tersebut secara rata-rata.

        ---

        ### Expected Utility (EU)

        **Expected Utility (EU)** merupakan pengembangan dari Expected Value. Selain mempertimbangkan nilai payoff, EU juga mempertimbangkan bagaimana seseorang memandang risiko.

        Secara sederhana, EU menjawab pertanyaan:

        > *"Jika saya memiliki karakter tertentu dalam menghadapi risiko, alternatif mana yang paling sesuai untuk saya?"*

        Pada dashboard ini terdapat tiga tipe sikap terhadap risiko:

        - **Risk Averse** 🛡️  
        Cenderung menghindari risiko dan lebih menyukai pilihan yang stabil.

        - **Risk Neutral** ⚖️  
        Bersikap netral terhadap risiko dan hanya melihat nilai hasil yang diperoleh.

        - **Risk Seeking** 🚀  
        Lebih berani mengambil risiko demi mendapatkan hasil yang lebih tinggi.

        ---

        ### Apa Bedanya EV dan EU?

        Misalnya terdapat dua pilihan:

        | Pilihan | Nilai |
        |----------|-------:|
        | A | 80 |
        | B | 100 |

        Pada EV, pilihan B akan lebih disukai karena memiliki nilai yang lebih besar.

        Namun pada EU, hasil dapat berbeda tergantung sikap terhadap risiko. Seseorang yang sangat menghindari risiko mungkin lebih memilih alternatif yang lebih stabil meskipun nilainya sedikit lebih rendah.

        ---

        ### Kapan EV dan EU Sama?

        Jika Anda memilih **Risk Neutral**, maka nilai utilitas sama dengan nilai payoff.

        Dengan kata lain:

        > EU ≈ EV

        Oleh karena itu hasil rekomendasi EV dan EU sering kali sama ketika pengguna memilih Risk Neutral.

        ---

        ### Bagaimana Hubungannya Dengan Dashboard Ini?

        1. Hasil kuesioner digunakan untuk menentukan probabilitas setiap state.
        2. Probabilitas state digunakan dalam perhitungan EV dan EU.
        3. Setiap peminatan dievaluasi terhadap seluruh state menggunakan matriks payoff.
        4. Alternatif dengan nilai EV atau EU tertinggi akan menjadi rekomendasi utama.

        Semakin tinggi nilai EV atau EU suatu peminatan, semakin tinggi tingkat kecocokannya terhadap profil Anda berdasarkan data akademik, minat, dan penilaian diri yang telah diisi.
        """)
    colState, colUtil = st.columns([0.4,0.6], gap='small')

    ### Probabilitas State
    with colState.container(border=True):
        with st.form("probabilitas_state", border=False):
            st.subheader("Probabilitas State")
            st.badge("Total Probabilitas State = 1", color="blue")

            A0, B0, C0, D0 = st.session_state.prob
            col1, col2 = st.columns(2)

            A = col1.number_input("Akademisi", value=A0, min_value=0.0, max_value=1.0, step=0.01)
            B = col2.number_input("Data Science", value=B0, min_value=0.0, max_value=1.0, step=0.01)
            C = col1.number_input("Quality Control", value=C0, min_value=0.0, max_value=1.0, step=0.01)
            D = col2.number_input("Aktuaris", value=D0, min_value=0.0, max_value=1.0, step=0.01)

            btn1, btn2 = st.columns(2)
            submit = btn1.form_submit_button("Hitung")
            random_btn = btn2.form_submit_button("🎲 Acak")

            if random_btn:
                prob = np.round(np.random.dirichlet(np.ones(4)), 3)
                prob[-1] = round(1 - prob[:-1].sum(), 3)
                st.session_state.prob = prob
                st.rerun()

            if submit:
                prob = np.array([A, B, C, D])

                if not np.isclose(prob.sum(), 1):
                    st.warning(f"Total probabilitas harus 1. Saat ini = {prob.sum():.3f}")
                    st.stop()

                st.session_state.prob = prob

    ### Bobot Utilitas
    with colUtil.container(border=True):
        if "risk_attitude" not in st.session_state:
            st.session_state.risk_attitude = "Risk Neutral"
        
        st.subheader("Pengambilan Resiko")
        st.badge("Atur bobot untuk setiap state",color='orange')
        col1, col2, col3 = st.columns([0.34,0.33,0.33], gap='xxsmall')
    
        with col1:
            st.markdown(card_button("Risk Averse", "🛡️", "Risk Averse", "(Menghindari Risiko)"),
                        unsafe_allow_html=True)
            if st.button("Pilih Risk Averse", key="btn_averse", use_container_width=True):
                st.session_state.risk_attitude = "Risk Averse"
                st.rerun()
        
        with col2:
            st.markdown(card_button("Risk Neutral", "⚖️", "Risk Neutral", "(Netral)"),
                        unsafe_allow_html=True)
            if st.button("Pilih Risk Neutral", key="btn_neutral", use_container_width=True):
                st.session_state.risk_attitude = "Risk Neutral"
                st.rerun()
        
        with col3:
            st.markdown(card_button("Risk Seeking", "🚀", "Risk Seeking", "(Mencari Risiko)"),
                        unsafe_allow_html=True)
            if st.button("Pilih Risk Seeking", key="btn_seeking", use_container_width=True):
                st.session_state.risk_attitude = "Risk Seeking"
                st.rerun()
    
        st.markdown("""
            <style>
            /* Push the Streamlit buttons behind the visual cards */
            div[data-testid="column"] > div > div > div > div:last-child button {
                opacity: 0;
                height: 0px;
                padding: 0;
                margin: 0;
                border: none;
                overflow: hidden;
            }
            </style>
            """, unsafe_allow_html=True)

    ### Expected Value
    st.title("📊 Expected Value", text_alignment='center')
    formulas = create_ev_formula(st.session_state.df_payoff, st.session_state.prob, ev_values)

    expected_value = pd.DataFrame({
        "Alternatif" :["Terapan", "Komputasi", "Keuangan", "Teori"],
        "Perhitungan EV": formulas,
        "EV (Hasil)": [f"{fn(val)}" for val in ev_values],
        "Ranking": [f"{r}"+medali[r] for r in ranking]
        }).set_index("Alternatif").sort_values(by="EV (Hasil)",ascending=False)
    
    st.dataframe(expected_value.style.map(lambda x: "background-color: lightblue", subset=["EV (Hasil)"]))

    ### Expected Utility
    st.title("📊 Expected Utility", text_alignment='center')

    utility_matrix, eu_values, ranking = calculate_eu(st.session_state.df_payoff, st.session_state.prob, risk_attitude=st.session_state.risk_attitude)
    eu_formula = create_eu_formula(utility_matrix, st.session_state.prob)

    expected_utility = pd.DataFrame({
        "Alternatif": ["Terapan", "Komputasi", "Keuangan", "Teori"],
        "Utilitas per State (U(x))": [str(tuple(map(float, np.round(utility_matrix[i], 2)))) for i in range(len(st.session_state.df_payoff))],
        "Perhitungan EU": eu_formula,
        "EU (Hasil)": [f"{fn(val)}" for val in eu_values],
        "Ranking": [f"{r}"+medali[r] for r in ranking]
        }).set_index("Alternatif").sort_values(by="EU (Hasil)",ascending=False)

    st.dataframe(expected_utility.style.map(lambda x: "background-color: lightgreen", subset=["EU (Hasil)"]))


    ### perbandingan EV dan EU
    st.title("📊 Perbandingan EV dan EU", text_alignment='center')
    comparison_df = pd.DataFrame({
        "Alternatif": [
            "Statistika Terapan",
            "Statistika Komputasi",
            "Statistika Keuangan",
            "Statistika Teori"
        ],
        "EV": ev_values,
        "EU": eu_values
    })

    df_plot = comparison_df.melt(
        id_vars="Alternatif",
        var_name="Metode",
        value_name="Nilai"
    )

    fig = px.bar(
        df_plot,
        y="Alternatif",
        x="Nilai",
        color="Metode",
        orientation="h",
        barmode="group",
        text="Nilai",
        color_discrete_map={
            "EV": "#3B82F6",
            "EU": "#22C55E"
        }
    )

    fig.update_traces(
        texttemplate="%{x:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        bargap=0.55,
        legend=dict(
            orientation="h",
            y=1.1,
            x=0.1
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="#E5E7EB"
        ),
        yaxis=dict(
            autorange="reversed"
        )
    )

    st.plotly_chart(fig)

    ### kesimpulan
    st.title("📌 Kesimpulan", text_alignment='center')
    st.markdown(f"""
        Berdasarkan perhitungan EV dan EU, alternatif dengan nilai tertinggi adalah :blue[**{st.session_state.rekomendasi}**]. 
        Hal ini menunjukkan bahwa :blue[**{st.session_state.rekomendasi}**] adalah pilihan yang paling menguntungkan secara finansial (EV) dan paling sesuai dengan preferensi risiko Anda (EU).
        """)

with tab3:
    st.warning("Mohon maaf, fitur masih dalam tahap pengembangan")
