import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Dashboard Tema ve Sayfa Ayarı
st.set_page_config(page_title="AI Business Intelligence Dashboard", layout="wide", page_icon="📈")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar & API
st.sidebar.title("💳 AI İşlem Merkezi")
api_key = st.sidebar.text_input("Gemini API Key:", type="password")

st.title("🏛️ Otomatik Veri Analiz ve Dashboard Sistemi")
st.write("Dosyanızı yükleyin, yapay zeka saniyeler içinde profesyonel raporunuzu hazırlasın.")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 3. Dosya Yükleme
        uploaded_file = st.file_uploader("Dosya Sürükleyin (PNG, JPG, XLSX, CSV)", type=['png', 'jpg', 'jpeg', 'xlsx', 'csv'])

        if uploaded_file:
            ext = uploaded_file.name.split('.')[-1].lower()
            
            # --- OTOMATİK ANALİZ MODÜLÜ ---
            with st.status("🚀 Veriler işleniyor ve dashboard hazırlanıyor...", expanded=True) as status:
                
                # A: GÖRSEL KARNE ANALİZİ (Örn: Ahmet Yılmaz Raporu)
                if ext in ['png', 'jpg', 'jpeg']:
                    img = Image.open(uploaded_file)
                    st.image(img, caption='Yüklenen Analiz Görseli', use_container_width=True)
                    
                    # Dashboard tipi analiz sorgusu
                    auto_prompt = """
                    Bu görseli bir Business Intelligence uzmanı gibi analiz et:
                    1. Kişi ve Rol bilgisi nedir?
                    2. Kritik KPI'lar (Kalite, AHT, FCR vb.) nelerdir? Sayısal olarak ver.
                    3. 'Hata Analizi' ve 'Gelişim Önerileri' kısımlarını madde madde özetle.
                    4. Yönetici için 3 maddelik acil aksiyon planı çıkar.
                    """
                    response = model.generate_content([auto_prompt, img])
                    
                    st.subheader("📋 Otomatik Dashboard Raporu")
                    st.markdown(response.text)
                    status.update(label="Analiz Tamamlandı!", state="complete")

                # B: EXCEL / CSV ANALİZİ
                elif ext in ['xlsx', 'csv']:
                    df = pd.read_excel(uploaded_file, engine='openpyxl') if ext == 'xlsx' else pd.read_csv(uploaded_file)
                    
                    # Üst Panel: Otomatik Metrikler
                    num_cols = df.select_dtypes(include=['number']).columns.tolist()
                    if num_cols:
                        cols = st.columns(len(num_cols[:4]))
                        for i, col_name in enumerate(num_cols[:4]):
                            with cols[i]:
                                st.metric(label=col_name, value=round(df[col_name].mean(), 2), delta="Ortalama")

                    # Orta Panel: Otomatik Grafik
                    st.subheader("📊 Otomatik Veri Görselleştirme")
                    if len(num_cols) >= 1:
                        fig = px.histogram(df, x=df.columns[0], y=num_cols[0], color_discrete_sequence=['#636EFA'], barmode='group')
                        st.plotly_chart(fig, use_container_width=True)

                    # Alt Panel: AI Yorumu
                    st.subheader("🤖 Yapay Zeka Veri Yorumu")
                    data_summary = df.head(20).to_json(orient="records")
                    auto_data_prompt = f"Bu verilerdeki gizli trendleri ve anormallikleri bul: {data_summary}"
                    data_res = model.generate_content(auto_data_prompt)
                    st.info(data_res.text)
                    status.update(label="Veri Analizi Hazır!", state="complete")

            # --- PAYLAŞIM VE ÇIKTI ---
            st.divider()
            col_down1, col_down2 = st.columns(2)
            with col_down1:
                st.button("📧 Raporu E-posta Olarak Taslakla")
            with col_down2:
                st.button("📥 PDF Olarak İndir (Yakında)")

    except Exception as e:
        if "429" in str(e):
            st.error("⚠️ Kota doldu. Lütfen 1 dakika bekleyin.")
        else:
            st.error(f"Sistem Hatası: {e}")
else:
    st.warning("🔑 Lütfen devam etmek için sol menüye API anahtarınızı girin.")
