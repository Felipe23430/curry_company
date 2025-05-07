#bibliotecas necessarias
import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config( page_title='Visão Entregadores', layout='wide') 


# ------------------------------ funções -------------------------------------
def entregadores_mais_rapido(df1):            
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].
                           groupby(['City','Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)']).reset_index())
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    return df3

def entregadores_mais_lentos(df1):
    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City','Delivery_person_ID']).max()
                           .sort_values(['City', 'Time_taken(min)'], ascending = False).reset_index())
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    return df3

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
image = Image.open('logo.png' )
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
tab1, =  st.tabs(['Visão Gerencial'])
with tab1:
    with st.container():
        st.title('Métricas Gerais')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)  
        with col2:
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Maior idade', menor_idade)  
        with col3:
            melhor_veiculo = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor veiculo', melhor_veiculo)  
        with col4:
            pior_veiculo = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior veiculo', pior_veiculo)
  
    with st.container():
        st.markdown( """---""" )
        st.title('Avaliações')
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Avaliacao media por Entregador')
            df_avg_ratings_per_deliver = (df1.loc[:,   ['Delivery_person_ID','Delivery_person_Ratings']]
                                          .groupby('Delivery_person_ID').mean().reset_index())
            st.dataframe(df_avg_ratings_per_deliver) 
        with col2:    
            st.subheader('Avaliacao media por transito')
            df_avg_std_rating_by_traffic =( df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                       .groupby('Road_traffic_density').agg({'Delivery_person_Ratings':['mean', 'std']}))
            #mudanca de nome das colunas
            df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']
            #reset do index
            df_avg_std_rating_by_traffic = df_avg_std_rating_by_traffic.reset_index()
            st.dataframe(df_avg_std_rating_by_traffic)
           
            st.subheader('Avaliacao media por clima')
            df_avg_std_Weatherconditions_by_weather = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                        .groupby('Weatherconditions').agg({'Delivery_person_Ratings':['mean', 'std']}))
            #Remove o nível extra do MultiIndex nas colunas
            df_avg_std_Weatherconditions_by_weather.columns = df_avg_std_Weatherconditions_by_weather.columns.droplevel(0)
            # Renomeia as colunas
            df_avg_std_Weatherconditions_by_weather.columns = ['delivery_mean', 'delivery_std']
            # Reset do índice
            df_avg_std_Weatherconditions_by_weather = df_avg_std_Weatherconditions_by_weather.reset_index()
            # Exibe o DataFrame
            st.dataframe(df_avg_std_Weatherconditions_by_weather)
            
    with st.container():
        st.markdown( """---""" )    
        st.title('Velocidade de Entrega')
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Entregadores mais rápido')
            df3 = entregadores_mais_rapido(df1)
            st.dataframe(df3)
            
        with col2:
            st.subheader('Entregadores mais lentos')  
            df3 = entregadores_mais_lentos(df1)
            st.dataframe(df3)
           
            
