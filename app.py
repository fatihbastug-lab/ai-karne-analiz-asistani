import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import plotly.express as px

# 1. Sayfa Ayarları
st.set_page_config(page_title="AI Veri Analizörü v3", layout="wide")

st.sidebar.title("🔑 Ayarlar")
api_key = st.sidebar.text_input("Gemini API Key:", type="password")

st.title("🚀 Kesintisiz AI Veri Analiz Platformu")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- KRİTİK GÜNCELLEME: Model Seçim Algoritması ---
        # Mevcut modelleri listele ve en uygun olanı otomatik bul
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Tercih sırasına göre model belirle
        target_model = ""
        for m in ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-1.0-pro"]:
            if m in available_models:
                target_model = m
                break
        
        if not target_model:
            target_model = available_models[0] # Hiçbiri yoksa ilk bulduğunu seç
            
        model = genai.GenerativeModel(target_model)
        st.sidebar.success(f"Aktif Model: {target_model}")

        # 2. Dosya Yükleme
        uploaded_file = st.file_uploader("Dosya Seç (PNG, JPG, XLSX, CSV)", type=['png', 'jpg', 'jpeg', 'xlsx', 'csv'])
        prompt = st.text_area("Analiz Talimatı:", "Bu verideki kritik noktaları ve gelişim önerilerini listele.")

        if uploaded_file:
            ext = uploaded_file.name.split('.')[-1].lower()
            
            # --- GÖRSEL ANALİZ ---
            if ext in ['png', 'jpg', 'jpeg']:
                img = Image.open(uploaded_file)
                st.image(img, use_container_width=True)
                if st.button("🖼️ Görseli Analiz Et"):
                    res = model.generate_content([prompt, img])
                    st.markdown(res.text)

            # --- EXCEL ANALİZ ---
            elif ext in ['xlsx', 'csv']:
                df = pd.read_excel(uploaded_file, engine='openpyxl') if ext == 'xlsx' else pd.read_csv(uploaded_file)
                st.dataframe(df.head())
                
                # Grafik Alanı
                num_cols = df.select_dtypes(include=['number']).columns.tolist()
                if num_cols:
                    col_choice = st.selectbox("Grafik Sütunu:", num_cols)
                    st.plotly_chart(px.bar(df, y=col_choice))

                if st.button("📊 Veriyi Yorumla"):
                    # Tabloyu JSON formatında gönderiyoruz (AI için okuması daha kolaydır)
                    data_json = df.to_json(orient="records")
                    full_query = f"Aşağıdaki JSON verisini analiz et ve özetle:\n\n{data_json}\n\nTalimat: {prompt}"
                    res = model.generate_content(full_query)
                    st.markdown(res.text)

    except Exception as e:
        st.error(f"Sistem Hatası: {e}")
else:
    st.info("Devam etmek için API anahtarınızı girin.")
