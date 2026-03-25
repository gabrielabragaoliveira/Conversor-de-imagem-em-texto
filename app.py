import streamlit as st
import google.generativeai as genai
from PIL import Image
# Importamos a nova biblioteca para suporte a Ctrl+V
from streamlit_paste_button import paste_image_button

# Configuração da página da interface
st.set_page_config(page_title="ContaPalito & Transcritor", page_icon="📝")
st.title("📝Escreve pra mim, por favor!!")
st.write("Faça o upload ou cole (Ctrl+V) a imagem.")

# Campo para a chave da API (para segurança, ela fica oculta)
api_key = st.sidebar.text_input("Chave da API do Google Gemini:", type="password")
st.sidebar.markdown("[Pegue sua chave de API aqui](https://aistudio.google.com/app/apikey)")

# --- ÁREA DE INPUT DE IMAGEM ---
# Dividimos em duas colunas para dar opções ao usuário
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Opção 1: Upload")
    uploaded_file = st.file_uploader("Selecione um arquivo", type=["png", "jpg", "jpeg"])

with col2:
    st.markdown("#### Opção 2: Colar")
    # Este botão especial captura o Ctrl+V
    pasted_image_data = paste_image_button(
        label="📋 Colar Imagem da Área de Transferência",
        background_color="#FF4B4B",
        hover_background_color="#D33636",
        color="#FFFFFF",
    )

# --- PROCESSAMENTO DA IMAGEM ---
image_to_process = None

# Verifica qual método de entrada foi usado
if uploaded_file is not None:
    # Caso tenha feito upload
    image_to_process = Image.open(uploaded_file)
    st.image(image_to_process, caption="Imagem carregada por upload", use_container_width=True)
elif pasted_image_data is not None:
    # Caso tenha colado (a biblioteca já devolve o formato Pillow pronto)
    image_to_process = pasted_image_data.image_pil
    st.image(image_to_process, caption="Imagem colada com sucesso", use_container_width=True)

# Se houver uma imagem pronta para processar
if image_to_process is not None:
    # Botão para iniciar a transcrição
    if st.button("Transcrever e Contar Palitinhos"):
        if not api_key:
            st.error("Por favor, insira a sua chave de API no menu lateral esquerdo.")
        else:
            try:
                # Configura a API com a chave fornecida
                genai.configure(api_key=api_key)
                
                # Usa o modelo Flash, que é mais rápido e econômico para essa tarefa
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Prompt revisado e mais robusto
                prompt = """
                Aja como um especialista em OCR e análise de dados manuscritos.
                Transcreva o texto da imagem em formato de lista Markdown.

                REGRAS DE CONTAGEM DE SÍMBOLOS (TRAÇOS/PALITINHOS):
                Identifique os grupos de símbolos ao lado de cada texto. Cada símbolo desenhado representa um número de acordo com esta regra estrita:
                - 1 único traço solto (|) = 1
                - Formato de "L" ou "Gamma" (__) (2 traços) = 2
                - Formato de "U" ou quadrado sem o topo ou base (__) (3 traços) = 3
                - Quadrado perfeito (__) (4 traços) = 4
                - Quadrado com um risco diagonal ou no meio (__) (5 traços) = 5

                Some todos os símbolos associados àquela linha de texto.

                FORMATO DE SAÍDA:
                Retorne apenas uma lista simples: "**Texto da Linha:** [Número Total Somado]"
                """
                
                with st.spinner("Analisando a imagem... Por favor aguarde."):
                    # Envia a imagem e as instruções para a API
                    response = model.generate_content([prompt, image_to_process])
                    
                    # Mostra o resultado na tela
                    st.success("Análise concluída!")
                    st.markdown("### Resultado:")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"Ocorreu um erro durante a análise: {e}")
