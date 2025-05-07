import streamlit as st 
from PIL import Image 

st.set_page_config(
    page_title="Home",
    page_icon=":rocket:"
)

#image_path = 'C:/Users/Felipe/Documents/Repos/Python/logo.png'
image = Image.open('logo.png')
st.sidebar.image( image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write('# Curry Company Painel de Analise')

st.markdown(
    """
    O Painel de Análise foi construido para acompanhar as métricas de crescimento dos Entregadores.
    ### Como utilizar esse Painel de Análise?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes
    """)    