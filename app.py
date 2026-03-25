import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração da página da interface
st.set_page_config(page_title="Transcritor de Anotações", page_icon="📝")
st.title("📝Escreve pra mim, por favor!!")
st.write("Faça o upload ou cole (Ctrl+V) a imagem das suas anotações.")

# Campo para a chave da API (para segurança, ela fica oculta)
api_key = st.sidebar.text_input("Chave da API do Google Gemini:", type="password")
st.sidebar.markdown("[Pegue sua chave de API aqui](https://aistudio.google.com/app/apikey)")

# Upload da imagem
uploaded_file = st.file_uploader("Arraste, selecione ou cole a imagem aqui", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Mostra a imagem na tela
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem carregada", use_column_width=True)

    # Botão para iniciar a transcrição
    if st.button("Transcrever Imagem"):
        if not api_key:
            st.error("Por favor, insira a sua chave de API no menu lateral esquerdo.")
        else:
            try:
                # Configura a API com a chave fornecida
                genai.configure(api_key=api_key)
                
                # Usa o modelo Pro, que é o melhor para ler caligrafia complexa
                model = genai.GenerativeModel('gemini-1.5-pro')
                
                # O "cérebro" da operação: o prompt que ensina o robô a contar
                prompt = """
                Transcreva o texto da imagem em formato de lista.
                Os símbolos representam números. Faça a soma para mim usando esta regra estrita:
                - 1 traço solto = 1
                - Formato de "L" ou "Gamma" (2 traços) = 2
                - Formato de "U" ou quadrado sem uma base (3 traços) = 3
                - Quadrado (4 traços) = 4
                - Quadrado com um risco no meio (5 traços) = 5
                
                Me dê apenas o texto da linha e o número final somado correspondente.
                """
                
                with st.spinner("Analisando a caligrafia e contando os palitinhos..."):
                    # Envia a imagem e as instruções para a API
                    response = model.generate_content([prompt, image])
                    
                    # Mostra o resultado na tela
                    st.success("Transcrição concluída!")
                    st.markdown("### Resultado:")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
