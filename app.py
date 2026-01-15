import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import io

# Sayfa yapılandırması
st.set_page_config(page_title="AI Hibrit Analizör", layout="wide")

st.sidebar.title("🛠️ Ayarlar")
api_key = st.sidebar.text_input("Gemini API Anahtarınızı Girin:", type="password")

st.title("📊 AI Görsel & Veri Analiz Asistanı")
st.write("Resim yükleyerek görsel analiz, Excel yükleyerek sayısal veri analizi yapabilirsiniz.")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Dosya yükleme alanı (Artık Excel ve CSV desteği var!)
    uploaded_file = st.file_uploader("Dosya seçin (PNG, JPG, XLSX, CSV)", type=['png', 'jpg', 'jpeg', 'xlsx', 'csv'])
    
    user_prompt = st.text_area("Yapay zekaya talimatınız:", 
                              "Bu dosyadaki verileri incele, önemli trendleri bul ve özetle.")

    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1]
        
        # --- DURUM 1: RESİM ANALİZİ ---
        if file_type in ['png', 'jpg', 'jpeg']:
            image = Image.open(uploaded_file)
            st.image(image, caption='Yüklenen Resim', width=500)
            
            if st.button("Resmi Analiz Et"):
                with st.spinner('Resim inceleniyor...'):
                    response = model.generate_content([user_prompt, image])
                    st.subheader("🤖 Resim Analiz Sonucu")
                    st.write(response.text)

        # --- DURUM 2: EXCEL/CSV ANALİZİ ---
        elif file_type in ['xlsx', 'csv']:
            if file_type == 'xlsx':
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            
            st.write("📊 Yüklenen Veri Önizlemesi:")
            st.dataframe(df.head()) # Verinin ilk 5 satırını gösterir
            
            if st.button("Verileri Analiz Et"):
                with st.spinner('Veriler işleniyor...'):
                    # Tabloyu metne dönüştürüp yapay zekaya gönderiyoruz
                    df_string = df.to_string()
                    full_prompt = f"Aşağıdaki verileri analiz et:\n\n{df_string}\n\nTalimat: {user_prompt}"
                    
                    response = model.generate_content(full_prompt)
                    st.subheader("🤖 Veri Analiz Raporu")
                    st.write(response.text)
else:
    st.info("💡 Devam etmek için API anahtarınızı girin.")
