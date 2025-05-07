#libraries
from  haversine import haversine

#bibliotecas necessarias
import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config( page_title='Visão Restaurantes', layout='wide') 


# ------------------------------ funções -------------------------------------

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
df = pd.read_csv('train.csv')
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
tab1, = st.tabs(['Visão Gerencial'])
with tab1:
        with st.container():
            st.title('Métricas Gerais')
            col1, col2, col3 = st.columns(3)
            
            with col1:
                delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
                col1.metric('Entregadores Únicos', delivery_unique)
                
            with col2:
                cols = (['Restaurant_latitude', 'Restaurant_longitude', 
                         'Delivery_location_latitude', 'Delivery_location_longitude'])
                df1['Distance'] =df1['distance'] = df1.loc[:, cols].apply(lambda x:
                haversine(
                (x['Restaurant_latitude'], x['Restaurant_longitude']),
                (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
                ), axis=1)
                avg_distance = round(df1['Distance'].mean(),2)
                col2.metric('Distância média restaurante/local de entrega', avg_distance)
                
        with col3:
                df_aux = (df1.loc[:, ['Time_taken(min)', 'Festival']]
                          .groupby('Festival')
                          .agg({'Time_taken(min)': ['mean', 'std']}))

                df_aux.columns = ['avg_time', 'std_time']
                df_aux = df_aux.reset_index()
                df_aux['Festival'] = df_aux['Festival'].str.strip()
                # Filtra e arredonda o valor
                tempo_medio = round(df_aux.loc[df_aux['Festival'] == 'Yes', 'avg_time'].values[0], 2)
                col3.metric('Tempo médio entrega Festivais', tempo_medio )        
                
        with st.container():
            st.markdown("""---""")
            col1, = st.columns(1)
            
            with col1:
                st.markdown('##### Tempo médio/Desvio padrão entrega por cidade/tipo de pedido')
                cols = ['Time_taken(min)', 'City', 'Type_of_order']
                df_aux = df1.loc[:, cols].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)' : ['mean', 'std']})
                df.coluns = ['avg_time', 'std_time']
                df_aux = df_aux.reset_index()
                st.dataframe(df_aux)
        with st.container():
            st.markdown("""---""")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('###### Tempo médio/desvio padrão  por cidade')
                cols = ['Time_taken(min)', 'City']
                df_aux = df1.loc[:,cols].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
                df_aux.columns = ['avg_time', 'std_time']
                df_aux = df_aux.reset_index()
                st.dataframe(df_aux)
            with col2:
                st.markdown('##### Tempo médio/desvio padrão por cidade/tipo de tráfico')
                cols = ['Time_taken(min)', 'City', 'Road_traffic_density']
                df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)' : ['mean', 'std']})
                df.coluns = ['avg_time', 'std_time']
                df_aux = df_aux.reset_index()
                st.dataframe(df_aux)
                
            
                
                
                
                
