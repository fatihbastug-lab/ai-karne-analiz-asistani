import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import plotly.express as px

# 1. Dashboard Başlığı ve Stil
st.set_page_config(page_title="AI Business Intelligence", layout="wide")
st.title("📈 Profesyonel Veri Analiz Dashboard")

# 2. Sidebar - Güvenli Bağlantı
st.sidebar.title("🔑 Bağlantı Ayarları")
api_key = st.sidebar.text_input("Gemini API Anahtarınız:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- HATA ÇÖZÜCÜ: Otomatik Model Bulma ---
        with st.sidebar:
            with st.spinner("Uygun yapay zeka modeli aranıyor..."):
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                # En kararlı modeli seç (Önce flash, yoksa ilk bulduğunu al)
                selected_model_name = next((m for m in available_models if "flash" in m), available_models[0])
                model = genai.GenerativeModel(selected_model_name)
                st.success(f"Bağlantı Başarılı! \nModel: {selected_model_name}")

        # 3. Dosya Yükleme Paneli
        uploaded_file = st.file_uploader("Dosyayı buraya bırakın (Resim, Excel, CSV)", type=['png', 'jpg', 'jpeg', 'xlsx', 'csv'])

        if uploaded_file:
            ext = uploaded_file.name.split('.')[-1].lower()
            
            # --- MODÜL A: GÖRSEL ANALİZ (AHMET YILMAZ KARNESİ GİBİ) ---
            if ext in ['png', 'jpg', 'jpeg']:
                image = Image.open(uploaded_file)
                st.image(image, caption='Yüklenen Analiz Dosyası', use_container_width=True)
                
                if st.button("🚀 Otomatik Analiz Başlat"):
                    with st.spinner('Yapay zeka verileri okuyor...'):
                        prompt = "Bu bir performans karnesidir. İsim, KPI değerleri (Kalite, AHT, FCR), hata analizleri ve gelişim önerilerini profesyonel bir rapor olarak sun."
                        response = model.generate_content([prompt, image])
                        st.subheader("🤖 Yapay Zeka Analiz Sonucu")
                        st.info(response.text)

            # --- MODÜL B: EXCEL / CSV ANALİZİ ---
            elif ext in ['xlsx', 'csv']:
                df = pd.read_excel(uploaded_file, engine='openpyxl') if ext == 'xlsx' else pd.read_csv(uploaded_file)
                
                # Otomatik Metrikler (Piyasadaki Dashboardlar gibi)
                num_cols = df.select_dtypes(include=['number']).columns.tolist()
                if num_cols:
                    st.subheader("📊 Temel Metrikler (Ortalama)")
                    m_cols = st.columns(len(num_cols[:4]))
                    for i, col in enumerate(num_cols[:4]):
                        m_cols[i].metric(label=col, value=f"{df[col].mean():.2f}")

                # İnteraktif Tablo ve Grafik
                tab1, tab2 = st.tabs(["📋 Ham Veri", "📈 Grafik"])
                with tab1: st.dataframe(df, use_container_width=True)
                with tab2:
                    if num_cols:
                        fig = px.bar(df, y=num_cols[0], title="Otomatik Performans Grafiği", template="plotly_white")
                        st.plotly_chart(fig, use_container_width=True)

                if st.button("🔍 Veri Trendlerini Analiz Et"):
                    with st.spinner('AI sayısal verileri yorumluyor...'):
                        data_json = df.head(20).to_json(orient="records")
                        prompt = f"Aşağıdaki verilerdeki önemli başarıları ve riskli trendleri açıkla: {data_json}"
                        response = model.generate_content(prompt)
                        st.success("Analiz Tamamlandı!")
                        st.write(response.text)

    except Exception as e:
        st.error(f"⚠️ Bir sorun oluştu: {e}")
        st.info("İpucu: Eğer 404 hatası alıyorsanız, API anahtarınızın Google AI Studio'da aktif olduğundan emin olun.")
else:
    st.warning("👈 Lütfen devam etmek için sol tarafa API anahtarınızı girin.")
