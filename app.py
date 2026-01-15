import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import io

# 1. Sayfa Ayarları
st.set_page_config(page_title="AI Karne & Veri Analizörü", layout="wide", page_icon="🚀")

# 2. Sidebar - API Anahtarı
st.sidebar.title("🔑 Erişim Paneli")
api_key = st.sidebar.text_input("Gemini API Anahtarınızı Yapıştırın:", type="password")
st.sidebar.info("API anahtarınızı Google AI Studio'dan alabilirsiniz.")

# 3. Ana Başlık
st.title("📊 AI Görsel & Excel Veri Analiz Asistanı")
st.markdown("Hem resimlerdeki verileri hem de Excel dosyalarındaki sayısal verileri analiz eder.")

if api_key:
    try:
        # Yapay Zeka Yapılandırması (En güncel model sürümü kullanıldı)
        genai.configure(api_key=api_key)
        # Hata aldığın satırı 'gemini-1.5-flash-latest' olarak güncelledik
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # 4. Dosya Yükleme Alanı
        uploaded_file = st.file_uploader("Dosya Yükleyin (PNG, JPG, XLSX, CSV)", type=['png', 'jpg', 'jpeg', 'xlsx', 'csv'])
        
        user_prompt = st.text_area("Yapay Zekaya Özel Talimatınız:", 
                                  "Bu dosyadaki verileri incele, önemli trendleri bul ve profesyonel bir gelişim raporu hazırla.")

        if uploaded_file is not None:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # --- DURUM A: GÖRSEL ANALİZİ (Karne Resmi vb.) ---
            if file_extension in ['png', 'jpg', 'jpeg']:
                image = Image.open(uploaded_file)
                st.image(image, caption='Yüklenen Görsel', width=600)
                
                if st.button("Resmi AI İle Analiz Et"):
                    with st.spinner('Yapay zeka resmi okuyor...'):
                        response = model.generate_content([user_prompt, image])
                        st.success("Analiz Tamamlandı!")
                        st.subheader("🤖 AI Raporu")
                        st.write(response.text)

            # --- DURUM B: VERİ ANALİZİ (Excel/CSV) ---
            elif file_extension in ['xlsx', 'csv']:
                try:
                    if file_extension == 'xlsx':
                        # openpyxl motoru requirements.txt'de yüklü olmalı
                        df = pd.read_excel(uploaded_file)
                    else:
                        df = pd.read_csv(uploaded_file)
                    
                    st.write("📋 Veri Önizlemesi (İlk 5 Satır):")
                    st.dataframe(df.head())
                    
                    if st.button("Verileri AI İle Analiz Et"):
                        with st.spinner('Sayısal veriler işleniyor...'):
                            # Veriyi metne çevirip AI'a gönderiyoruz
                            df_context = df.to_string()
                            full_query = f"Aşağıdaki tablo verilerini analiz et:\n\n{df_context}\n\nKullanıcı Talimatı: {user_prompt}"
                            
                            response = model.generate_content(full_query)
                            st.success("Veri Analizi Başarılı!")
                            st.subheader("🤖 Sayısal Analiz Raporu")
                            st.write(response.text)
                except Exception as e:
                    st.error(f"Dosya okunurken hata oluştu: {e}. Lütfen requirements.txt dosyanızda 'openpyxl' olduğundan emin olun.")

    except Exception as e:
        st.error(f"Yapay zeka bağlantısında hata: {e}")
else:
    st.warning("⚠️ Devam etmek için lütfen sol taraftaki menüye geçerli bir API Anahtarı girin.")
