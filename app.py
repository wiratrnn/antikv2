import streamlit as st

st.markdown("""
<style>
  .risk-subtitle .highlight {
    color: #2563eb;
    font-weight: 600;
  }
 
  .card-row {
    display: flex;
    gap: 14px;
    margin-bottom: 18px;
  }
 
  .risk-card {
    flex: 1;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px 12px 16px;
    text-align: center;
    cursor: pointer;
    background: #ffffff;
    transition: box-shadow .2s;
  }
  .risk-card:hover { box-shadow: 0 4px 14px rgba(37,99,235,0.12); }
 
  .risk-card.active {
    background: #2563eb;
    border-color: #2563eb;
    box-shadow: 0 4px 16px rgba(37,99,235,0.30);
  }
 
  .card-icon {
    font-size: 36px;
    margin-bottom: 10px;
    display: block;
    line-height: 1;
  }
 
  .card-title {
    font-size: 14px;
    font-weight: 700;
    color: #1a1a2e;
    display: block;
    margin-bottom: 3px;
  }
  .card-subtitle {
    font-size: 11.5px;
    color: #6b7280;
    display: block;
  }
 
  .risk-card.active .card-title  { color: #ffffff; }
  .risk-card.active .card-subtitle { color: rgba(255,255,255,0.80); }
 
  .info-box {
    display: flex;
    align-items: flex-start;
    gap: 9px;
    background: #eff6ff;
    border-radius: 8px;
    padding: 11px 14px;
    font-size: 13px;
    color: #1e40af;
    line-height: 1.5;
  }
            
  .info-box .info-icon {
    font-size: 16px;
    margin-top: 1px;
    flex-shrink: 0;
  }
</style>
""", unsafe_allow_html=True)

@st.dialog("📊 Dashboard AnTikV2", width='medium')
def info():
    st.html("""
        <style>
        .st-key-my_blue_container {
            background-color: rgb(235, 235, 255);
            padding: 20px;
        }

        .st-key-statistika_teori_container {
            background-color: rgb(200, 140, 255);
            border-radius: 5px;
        }
        .st-key-statistika_terapan_container {
            background-color: rgb(140, 255, 140);
            border-radius: 5px;
        }
        .st-key-statistika_komputasi_container {
            background-color: rgb(140, 200, 255);
            border-radius: 5px;
        }
        .st-key-statistika_keuangan_container {
            background-color: rgb(255, 200, 140);
            border-radius: 5px;
        }

        .st-key-warning_container {
            background-color: rgb(255, 255, 100);
            padding: 20px;
            border-radius: 5px;
        }
        </style>
        """)
    
    with st.container(key='my_blue_container', border=True, gap='small'):
        st.markdown("""
                #### 👋 Halo, Sobat Statistika!
                    
                Dashboard ini dikembangkan sebagai bentuk proyek Mata Kuliah :blue-badge[**Teori Pengambilan Keputusan**] 
                dan dirancang untuk membantu mahasiswa terutama mahasiswa statistika UNIMED 😄
                dalam memilih peminatan yang paling sesuai dengan kemampuan akademik yang dimiliki.
                """)
        
    st.markdown("""
             #### 💡 Tidak yakin memilih peminatan?
                
             Dashboard ini akan menganalisis nilai :blue[**mata kuliah**], :green[**minat bakat**] serta :orange[**kemampuan diri**] kamu dan 
             memberikan rekomendasi peminatan yang paling sesuai berdasarkan data yang kamu isi di :green-background[**kuesioner**].
            """)
    
    st.markdown("### Di Prodi Statistika terdapat 4 penjurusan yaitu:")

    col1, col2 = st.columns([0.65,0.35], gap='medium')
    with col1:
        col3, col4 = st.columns(2, gap='xsmall')
        with col3:
            with st.container(key='statistika_teori_container', border=True, gap='xxsmall'):
                st.markdown(":violet[📈 **Statistika Teori**]", text_alignment='center')
            with st.container(key='statistika_terapan_container', border=True, gap='xxsmall'):
                st.markdown(":green[🌍 **Statistika Terapan**]", text_alignment='center')
        with col4:
            with st.container(key='statistika_komputasi_container', border=True, gap='xxsmall'):
                st.markdown(":blue[💻 **Statistika Komputasi**]", text_alignment='center')
            with st.container(key='statistika_keuangan_container', border=True, gap='xxsmall'):
                st.markdown(":orange[💰 **Statistika Keuangan**]", text_alignment='center')

        st.info("🎓 Semoga dashboard ini dapat membantu menemukan peminatan yang paling sesuai dengan potensimu!💪")
        if st.button("🚀 Mulai Sekarang", type='primary'):
            st.rerun()

    with col2.container(key='warning_container', border=True, gap='small'):
        st.markdown("""
             ⚠️ :red-badge[**Perhatian**] ⚠️
                
             Hasil rekomendasi yang diberikan bukan keputusan mutlak, 
             melainkan sebagai bahan pertimbangan dalam memilih peminatan yang paling sesuai dengan kemampuan akademikmu.
            """)

if 'visited' not in st.session_state:
    st.session_state.visited = True
    info()

def halaman_utama():
    st.markdown(
        f"""
        <div style="
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
        ">
            <h1 style="
                margin-left:18px;
                font-weight:bold;
                letter-spacing:0;
                line-height:0;
                white-space:nowrap;
                font-size:90px;
            ">
                <span style="color:#2563eb">An</span><span style="color:#16a34a">Tik</span><span style="color:#f97316">V2</span>
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<h5 style='text-align: center; color: black'>(Anak Statistik Versi 2)</h5>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Asisten Penentuan Penjurusan Mahasiswa Statistika👋</h4>", unsafe_allow_html=True)
    st.markdown("✨ Berdasarkan nilai :orange[**mata kuliah**], :green[**minat-bakat**], dan :blue[**kemampuan diri**]", text_alignment='center')
    if st.button("❓ Tentang Dashboard", type="secondary", key="info"):
        info()

    col_menu, col_test = st.columns(2, border=True, gap='small')
    
    with col_menu:
        st.markdown("<h3 style='text-align: center;'>🚀 Mulai Analisis</h3>", unsafe_allow_html=True)
        colGbr, colCap = st.columns([0.4,0.6])
        colGbr.image('icon/analisis.png')
        with colCap:
            st.write("Masuk ke dashboard utama untuk melihat fitur lengkap dan coba simulasi yang interaktif sesuai keinginan mu.")
            if st.button("🚀 Mulai", type="primary", key="dashboard"):
                st.switch_page(page_dashboard)

    with col_test:
        st.markdown("<h3 style='text-align: center;'>🧠 Kuesioner</h3>", unsafe_allow_html=True)
        colGbr, colCap = st.columns([0.4,0.6])
        colGbr.image('icon/kuesioner.png')
        with colCap:
            st.write("belum yakin dengan peminatanmu? Yuk kenali potensi dan minatmu melalui tes singkat ini. :blue-badge[ hanya 30 pertanyaan saja ]")
            if st.button("📝 Mulai Tes", type="primary", key="kuesioner"):
                st.switch_page(page_kuesioner)

    st.markdown(":violet-background[🌱 Tidak ada pilihan yang sempurna, yang ada adalah pilihan yang paling cocok untukmu. Kenali potensimu dan tentukan arah terbaikmu.✨]",
                text_alignment='center')
    st.caption("Made with ❤️ by Wira Triono")


page_home = st.Page(halaman_utama, title="Halaman Utama", icon="🏠", default=True)
page_dashboard = st.Page("dashboard.py", title="Dashboard Utama", icon="📊")
page_kuesioner = st.Page("kuesioner.py", title="Kuesioner Minat Bakat", icon="📝")

st.session_state.page_home = page_home
st.session_state.page_dashboard = page_dashboard
pg = st.navigation([page_home, page_dashboard, page_kuesioner], position='hidden')

pg.run()