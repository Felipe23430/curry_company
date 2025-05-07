#libraries
from  haversine import haversine
import plotly.express as px

#bibliotecas necessarias
import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config( page_title='Visão Empresa', layout='wide') 


# ------------------------------ funções -------------------------------------
def pedidos_por_dia (df1):
           
    cols = ['ID', 'Order_Date']
     #selecao de linhas
    df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index()
     #desenhar grafico
    fig=(px.bar(df_aux, x='Order_Date', y='ID'))
    return fig
    """ Esta função tem como objetivo descobrir a quantidade de pedidos por dia.
    1 - Selecionar as colunas 'ID' e 'Order_Date' do DataFrame.
    2 - Agrupar os dados por 'Order_Date', contando a quantidade de 'ID' por data e resetando o índice.
    3 - Montar um gráfico de barras com 'Order_Date' no eixo X e a contagem de 'ID' no eixo Y.
    Input: DataFrmae (DF1)
    output: Gráfico de barras (fig)
    """

def distribuicao_tipo_trafico(df1):
    columns = ['ID', 'Road_traffic_density']
    df_aux = df1.loc[:, columns].groupby('Road_traffic_density').count().reset_index()
    df_aux['perc_ID'] = 100 * (df_aux['ID'] / df_aux['ID'].sum())
    fig = px.pie(df_aux, values='perc_ID', names='Road_traffic_density')
    return fig
    """ Esta função tem como objetivo mostrar a distribuição percentual dos pedidos por tipo de densidade de tráfego.
    1 - Selecionar as colunas 'ID' e 'Road_traffic_density' do DataFrame.
    2 - Agrupar os dados por 'Road_traffic_density', contando a quantidade de 'ID' por categoria e resetando o índice.
    3 - Calcular o percentual de cada categoria em relação ao total de pedidos
    4 - Montar um gráfico de pizza (pie chart) com o percentual de pedidos por tipo de tráfego.
    Input: DataFrmae (DF1)
    output: Gráfico de pizza (fig)
    """

def volume_pedido_cidade_trafico(df1):
                
    df_aux = (df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                            .groupby(['City', 'Road_traffic_density']).count().reset_index())
    df_aux = df_aux[df_aux['City'].notna()]
    df_aux = df_aux[df_aux['Road_traffic_density'].notna()]
    # Gráfico de barras agrupadas
    fig = (px.bar(df_aux, x='City', y='ID', color='Road_traffic_density', barmode='group',
                  labels={'ID': 'Quantidade de Entregas'})  )             
    return fig    
    """ Esta função tem como objetivo calcular o volume de pedidos por tipo de cidade e densidade de tráfego.
    1 - Selecionar as colunas 'ID', 'City', 'Road_traffic_density' do DataFrame.
    2 - Remover registros com valores nulos em 'City' ou 'Road_traffic_density'.
    3 - Agrupar os dados por 'City' e 'Road_traffic_density', contando a quantidade de 'ID' por categoria.
    4 -Montar um gráfico de barras agrupadas com 'City' no eixo X, contagem de 'ID' no eixo Y,
        e cores representando os diferentes níveis de densidade de tráfego
    Input: DataFrmae (DF1)
    output: Gráfico de barra (fig)
    """

def pedidos_por_semana(df1):
            
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" ) #criando nova coluna
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index() 
    fig= px.line( df_aux, x='week_of_year', y='ID' )
    return fig
    """ Esta função tem como objetivo mostrar a quantidade de pedidos por semana.
    1 - Criar uma nova coluna chamada 'week_of_year' com o número da semana do ano, extraído de 'Order_Date'.
    2 - Selecionar as colunas 'ID' e 'week_of_year', agrupar por 'week_of_year' e contar a quantidade de 'ID'.
    3 - Montar um gráfico de linha com 'week_of_year' no eixo X e a contagem de 'ID' no eixo Y.
    Input: DataFrmae (DF1)
    output: Gráfico de linha (fig)
    """

def distribuição_pedidos_por_entregador (df1):
                        
    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index() 
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()
    df_aux = pd.merge( df_aux1, df_aux2, how='inner' ) 
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID'] 
    fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )
    return fig   
    """ Esta função tem como objetivo mostrar a média de pedidos por entregador em cada semana.
    1 - Selecionar as colunas 'ID' e 'week_of_year', agrupar por 'week_of_year' e contar a quantidade de pedidos.
    2 - Selecionar as colunas 'Delivery_person_ID' e 'week_of_year', agrupar por 'week_of_year' e contar a quantidade única de entregadores.
    3 - Juntar os dois resultados anteriores em um único DataFrame.
    4 - Calcular a média de pedidos por entregador, dividindo o número de pedidos pela quantidade de entregadores.
    5 - Montar um gráfico de linha com 'week_of_year' no eixo X e a média de pedidos por entregador no eixo Y.
    Input: DataFrmae (DF1)
    output: Gráfico de linha (fig)
    """
        
        
def clean_code(df1):
    """ Esta funcao tem a responsabilidade delimpar o dataframe
    1 - Remoção dos dados NaN
    2 - Mundaça do tipo da coluna de dados
    3 - Remoção dos espaços das variaveis de texto
    4 - Formatação das colunas de datas
    5 - limpeza da coluna tempo(remoção do texto da variavel numérica)
    Input: DataFrmae
    output: DataFrame
    """
    linhas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas,:].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    linhas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas,:].copy()
    linhas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas,:].copy()
    linhas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas,:].copy()

    #Alterando a coluna Delivery_person_Ratings para float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    #Alterando a coluna Order Date para data e hora
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')#Alterando a coluna multiple_deliveries	 para inteiro
    linhas2 = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas2,:].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    #tirar os espaçoes da coluna ID, Road_traffic_density, Type_of_order, Type_of_vehicle, City  
    df1['ID'] = df1.loc[:,'ID'].str.strip()
    df1['Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1['Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1['Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1['City'] = df1.loc[:, 'City'].str.strip()     

    #limpando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'] .apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int) 
    
    return df1
# ---------------------------- Estrutura lógica do código ----------------------------------------
#------------------------------Import Dataset ----------------------------------------------------
df = pd.read_csv('Python/train.csv')
# ----------------------------- limpando os dados ---------------------------------------------- 
df1 = clean_code(df)


#========================================================
# Barra lateral
#========================================================
st.header('Marketplace - Visão Cliente')
#image_path = 'C:/Users/Felipe/Documents/Repos/Python/logo.png'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value = pd.datetime( 2022, 4, 13),
    min_value=pd.datetime( 2022, 2, 11),
    max_value=pd.datetime( 2022, 4, 6),
    format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")

Weatherconditions_options = st.sidebar.multiselect(
    'Quais as condições do clima',
    ['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms',
       'conditions Cloudy', 'conditions Fog', 'conditions Windy',
       'conditions'],
    default=['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms',
       'conditions Cloudy', 'conditions Fog', 'conditions Windy',
       'conditions'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Felipe Laurentino')
#filtro data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]
#filtro transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]
#filtro clima
linhas_selecionadas =df1['Weatherconditions'].isin(Weatherconditions_options)
df1 = df1.loc[linhas_selecionadas,:]
#========================================================
# Layout no Streamlit
#========================================================
tab1, tab2 =  st.tabs(['Visão Gerencial', 'Visão Tática'])

with tab1:
    with st.container():
        
        fig = pedidos_por_dia(df1)
        st.header('Pedidos por dia')
        st.plotly_chart(fig, use_container_width=True)
                    
    with st.container():
        col1, col2 = st.columns(2)
    
        with col1:
            fig = distribuicao_tipo_trafico(df1)
            st.markdown(" ##### Distribuição por Tipo de Tráfico")
            st.plotly_chart(fig, use_container_width=True)
              

        with col2:
            fig = volume_pedido_cidade_trafico(df1)
            st.markdown(" ##### Volume de pedidos por Cidade e tipo de Tráfego")
            st.plotly_chart(fig, use_container_width=True)
            
with tab2:        
    with st.container():
        st.markdown('### Pedidos por semana')
        fig = pedidos_por_semana(df1)
        st.plotly_chart(fig, use_container_width=True)       
        
    with st.container():
        st.markdown('###  Distribuição de pedidos por entregador por semana')
        fig = distribuição_pedidos_por_entregador(df1)
        st.plotly_chart(fig, use_container_width=True) 
        


            
            