import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import plotly.express as px # Grafik için ekledik

# 1. Sayfa Ayarları
st.set_page_config(page_title="Pro AI Analizör", layout="wide", page_icon="📈")

# 2. Stil ve Sidebar
st.sidebar.title("🛠️ Gelişmiş Ayarlar")
api_key = st.sidebar.text_input("Gemini API Anahtarınız:", type="password")

st.title("🚀 Pro AI Görsel & Veri Analiz Platformu")
st.markdown("---")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 3. Dosya Yükleme Paneli
        col_file, col_prompt = st.columns([1, 1])
        with col_file:
            uploaded_file = st.file_uploader("Analiz edilecek dosyayı seçin", type=['png', 'jpg', 'jpeg', 'xlsx', 'csv'])
        with col_prompt:
            user_prompt = st.text_area("Yapay Zekaya Özel Komut:", 
                                      "Verileri özetle, kritik başarı ve riskleri listele, somut tavsiyeler ver.")

        if uploaded_file:
            file_ext = uploaded_file.name.split('.')[-1].lower()
            
            # --- MODÜL 1: GÖRSEL ANALİZ ---
            if file_ext in ['png', 'jpg', 'jpeg']:
                image = Image.open(uploaded_file)
                st.image(image, caption='Yüklenen Karne/Rapor', use_container_width=True)
                
                if st.button("🖼️ Görseli Yapay Zeka ile Çözümle"):
                    with st.spinner('AI görseli tarıyor...'):
                        response = model.generate_content([user_prompt, image])
                        st.subheader("🤖 AI Görsel Analiz Raporu")
                        st.info(response.text)
                        st.download_button("Raporu İndir (.txt)", response.text, file_name="ai_rapor.txt")

            # --- MODÜL 2: EXCEL & GRAFİK ANALİZİ ---
            elif file_ext in ['xlsx', 'csv']:
                df = pd.read_excel(uploaded_file, engine='openpyxl') if file_ext == 'xlsx' else pd.read_csv(uploaded_file)
                
                tab1, tab2 = st.tabs(["📋 Veri Tablosu", "📊 Otomatik Grafikler"])
                
                with tab1:
                    st.dataframe(df, use_container_width=True)
                
                with tab2:
                    st.subheader("Veri Görselleştirme")
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    if numeric_cols:
                        selected_col = st.selectbox("Grafik için bir sütun seçin:", numeric_cols)
                        fig = px.bar(df, y=selected_col, title=f"{selected_col} Dağılım Grafiği", color=selected_col)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("Grafik oluşturmak için sayısal veri bulunamadı.")

                if st.button("📈 Verileri AI İle Yorumla"):
                    with st.spinner('Sayısal trendler analiz ediliyor...'):
                        df_str = df.to_string()
                        full_query = f"Bu tablo verilerini analiz et:\n{df_str}\n\nTalimat: {user_prompt}"
                        response = model.generate_content(full_query)
                        st.subheader("🤖 Veri Analiz Raporu")
                        st.success(response.text)
                        st.download_button("Veri Analizini İndir", response.text, file_name="veri_analiz.txt")

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
else:
    st.warning("⚠️ Lütfen sol taraftaki panelden API anahtarınızı girerek oturum açın.")
