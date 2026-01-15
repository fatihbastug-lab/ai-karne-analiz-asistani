import streamlit as st
import google.generativeai as genai
from PIL import Image

# Sayfa yapılandırması
st.set_page_config(page_title="AI Karne Analizörü", layout="wide")

# Kenar çubuğu (Sidebar) tasarımı
st.sidebar.title("🛠️ Ayarlar")
api_key = st.sidebar.text_input("Gemini API Anahtarınızı Girin:", type="password")

st.title("📊 Yapay Zeka Destekli Karne Analizörü")
st.write("Yüklediğiniz görseldeki verileri analiz eder ve gelişim planı sunar.")

if api_key:
    # Yapay zekayı yapılandır
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Dosya yükleme alanı
    uploaded_file = st.file_uploader("Bir performans raporu veya karne görseli seçin...", type=['png', 'jpg', 'jpeg'])
    
    # Kullanıcı talimatı
    user_prompt = st.text_area("Yapay zekaya özel talimatınız (İsteğe bağlı):", 
                              "Bu görseldeki verileri detaylıca analiz et. Başarıları öv, eksiklikler için aksiyon planı çıkar.")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Ekranı ikiye böl (Sol görsel, sağ analiz)
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption='Yüklenen Rapor', use_container_width=True)
        
        if st.button("🚀 Analizi Başlat"):
            with st.spinner('Yapay zeka verileri inceliyor...'):
                try:
                    # Yapay zekaya görseli ve promptu gönder
                    response = model.generate_content([user_prompt, image])
                    
                    with col2:
                        st.subheader("🤖 Analiz Sonucu")
                        st.markdown(response.text)
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
else:
    st.info("💡 Başlamak için sol taraftaki menüye Gemini API anahtarınızı girmeniz gerekiyor.")
