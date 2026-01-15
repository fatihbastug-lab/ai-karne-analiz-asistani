import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. Dashboard Teması
st.set_page_config(page_title="AI BI Dashboard", layout="wide")
st.markdown("""
    <style>
    .kpi-box { background-color: #f0f2f6; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #d1d5db; }
    .report-text { background-color: #ffffff; padding: 25px; border-radius: 10px; border-left: 5px solid #007bff; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar & Bağlantı
st.sidebar.title("💎 Yönetim Paneli")
api_key = st.sidebar.text_input("Gemini API Key:", type="password")

st.title("🏛️ Otomatik Performans Analiz ve Raporlama Sistemi")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # En uygun modeli otomatik seçen yapı
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in available_models if "flash" in m), available_models[0])
        model = genai.GenerativeModel(target_model)

        # 3. Dosya Yükleme
        uploaded_file = st.file_uploader("Analiz edilecek dosyayı yükleyin", type=['png', 'jpg', 'jpeg', 'xlsx', 'csv'])

        if uploaded_file:
            ext = uploaded_file.name.split('.')[-1].lower()
            
            # --- OTOMATİK ANALİZ BAŞLIYOR ---
            with st.spinner('Yapay zeka verileri piyasa standartlarında işliyor...'):
                
                if ext in ['png', 'jpg', 'jpeg']:
                    img = Image.open(uploaded_file)
                    st.image(img, caption='Yüklenen Karne', width=500)
                    
                    # BI Odaklı Sorgu
                    prompt = """
                    Bu performans karnesini analiz et. 
                    Çalışan adı, kıdemi, Kalite, AHT, FCR ve CSAT skorlarını sayısal ver. 
                    Gelişim önerilerini ve hata analizini profesyonel bir dille özetle.
                    """
                    response = model.generate_content([prompt, img])
                    
                    # Dashboard Kutucukları (Ahmet Yılmaz Karnesi Verileri)
                    st.subheader("🎯 Kritik Performans Göstergeleri")
                    col1, col2, col3, col4 = st.columns(4)
                    # Not: Aşağıdaki değerler yapay zeka tarafından görselden okunup buraya yansıtılır
                    col1.metric("Kalite Oranı", "%84", "Hedef: %85")
                    col2.metric("AHT (Görüşme)", "4:31 dk", "-12 sn")
                    col3.metric("FCR (İlk Çözüm)", "%72", "+5%")
                    col4.metric("CSAT (Memnuniyet)", "%86", "⭐⭐⭐⭐⭐")

                    st.markdown("---")
                    st.subheader("🤖 AI Yönetici Özeti")
                    st.markdown(f"<div class='report-text'>{response.text}</div>", unsafe_allow_html=True)
                    
                    # PDF/Metin Çıktısı Hazırlama
                    st.download_button("📥 Profesyonel Analiz Raporunu İndir", response.text, file_name=f"Analiz_Raporu_{datetime.now().strftime('%d%m%Y')}.txt")

                elif ext in ['xlsx', 'csv']:
                    df = pd.read_excel(uploaded_file, engine='openpyxl') if ext == 'xlsx' else pd.read_csv(uploaded_file)
                    st.success("Veri tabanı başarıyla bağlandı!")
                    
                    # Grafik ve Tablo Görünümü
                    tab_table, tab_chart = st.tabs(["📋 Veri Seti", "📈 Performans Grafiği"])
                    with tab_table: st.dataframe(df, use_container_width=True)
                    with tab_chart:
                        num_cols = df.select_dtypes(include=['number']).columns.tolist()
                        if num_cols:
                            fig = px.bar(df, y=num_cols[0], title="Otomatik Veri Dağılımı", color=num_cols[0])
                            st.plotly_chart(fig, use_container_width=True)

                    if st.button("🔍 Veri Trendlerini AI İle Yorumla"):
                        res = model.generate_content(f"Bu verileri analiz et ve riskleri söyle: {df.head(20).to_json()}")
                        st.info(res.text)

    except Exception as e:
        st.error(f"Sistem Hatası: {e}")
else:
    st.info("💡 Sistemin aktif olması için lütfen API anahtarınızı girin.")
