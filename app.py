import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import plotly.express as px

# 1. Sayfa Yapılandırması
st.set_page_config(page_title="Pro AI Analiz Platformu", layout="wide", page_icon="📈")

# 2. Sidebar Ayarları
st.sidebar.title("🔑 Erişim ve Ayarlar")
api_key = st.sidebar.text_input("Gemini API Key:", type="password")
st.sidebar.markdown("---")
st.sidebar.write("🚀 **Geliştirici Modu Aktif**")

st.title("📊 Profesyonel AI Veri & Görsel Analizörü")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Hata ihtimaline karşı en kararlı model ismini seçiyoruz
        # 404 hatalarını önlemek için alternatif model ismi denemesi
        model_name = 'gemini-1.5-flash' 
        model = genai.GenerativeModel(model_name)

        # 3. Dosya Yükleme Paneli
        uploaded_file = st.file_uploader("Dosyanızı buraya bırakın (PNG, JPG, XLSX, CSV)", type=['png', 'jpg', 'jpeg', 'xlsx', 'csv'])
        
        prompt_custom = st.text_area("Yapay Zeka Talimatı:", 
                                   "Verileri detaylı analiz et, trendleri belirle ve aksiyon planı öner.")

        if uploaded_file:
            file_ext = uploaded_file.name.split('.')[-1].lower()
            
            # --- MODÜL 1: GÖRSEL (KARNE) ANALİZİ ---
            if file_ext in ['png', 'jpg', 'jpeg']:
                img = Image.open(uploaded_file)
                st.image(img, caption='Analiz Edilecek Görsel', use_container_width=True)
                
                if st.button("🖼️ Görseli Analiz Et"):
                    with st.spinner('AI inceliyor...'):
                        try:
                            response = model.generate_content([prompt_custom, img])
                            st.subheader("🤖 AI Görsel Analiz Raporu")
                            st.markdown(response.text)
                            st.download_button("Raporu Metin Olarak İndir", response.text, "ai_rapor.txt")
                        except Exception as e:
                            st.error(f"Model hatası: {e}. Lütfen API anahtarınızın aktif olduğunu kontrol edin.")

            # --- MODÜL 2: EXCEL / CSV VE GRAFİK ANALİZİ ---
            elif file_ext in ['xlsx', 'csv']:
                try:
                    df = pd.read_excel(uploaded_file, engine='openpyxl') if file_ext == 'xlsx' else pd.read_csv(uploaded_file)
                    
                    st.success("Veriler başarıyla yüklendi!")
                    tab_data, tab_chart = st.tabs(["📋 Veri Tablosu", "📊 İnteraktif Grafikler"])
                    
                    with tab_data:
                        st.dataframe(df, use_container_width=True)
                    
                    with tab_chart:
                        st.subheader("Veri Görselleştirme Merkezi")
                        num_cols = df.select_dtypes(include=['number']).columns.tolist()
                        if num_cols:
                            x_axis = st.selectbox("X Ekseni (Kategorik):", df.columns)
                            y_axis = st.selectbox("Y Ekseni (Sayısal):", num_cols)
                            chart_type = st.radio("Grafik Türü:", ["Sütun", "Çizgi", "Alan"], horizontal=True)
                            
                            if chart_type == "Sütun":
                                fig = px.bar(df, x=x_axis, y=y_axis, color=y_axis, template="plotly_dark")
                            elif chart_type == "Çizgi":
                                fig = px.line(df, x=x_axis, y=y_axis, markers=True, template="plotly_dark")
                            else:
                                fig = px.area(df, x=x_axis, y=y_axis, template="plotly_dark")
                                
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("Grafik çizmek için tabloda sayısal veri bulamadım.")

                    if st.button("📈 Verileri AI İle Yorumla"):
                        with st.spinner('Veri madenciliği yapılıyor...'):
                            df_sample = df.to_string()
                            full_input = f"Aşağıdaki verileri analiz et:\n\n{df_sample}\n\nTalimat: {prompt_custom}"
                            response = model.generate_content(full_input)
                            st.subheader("🤖 AI Veri Analiz Raporu")
                            st.markdown(response.text)
                            st.download_button("Analiz Dosyasını İndir", response.text, "veri_analiz_raporu.txt")
                
                except Exception as e:
                    st.error(f"Excel işleme hatası: {e}")

    except Exception as e:
        st.error(f"Beklenmedik bir hata oluştu: {e}")
else:
    st.info("💡 Lütfen sol panelden API anahtarınızı girerek sistemi aktif edin.")
