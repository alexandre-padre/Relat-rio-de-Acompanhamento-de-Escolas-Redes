# imports e definições
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import streamlit as st
import math
from PIL import Image
import plotly.express as px
from funcoes import *

######################## Configuração da página ########################

st.set_page_config(
    page_title="Relatório de Acompanhamento de Escolas/Redes", layout="centered", page_icon="[LOGO] Eduqo 4.png"
)

######################## Namespaces a serem analisados ########################

namespaces = pd.read_csv('./CSV/produto_namespace.csv')
#st.dataframe(namespaces)
namespace_rede = pd.read_csv('./CSV/namespace_rede.csv')

######################## Informações de licenças, produto, gestor de conta e receita ########################

informacoes_hubspot = pd.read_csv('./CSV/informacoes_hubspot.csv')
#st.dataframe(informacoes_hubspot)

######################## Cabeçalho do Relatório ########################

st.image('[LOGO] Eduqo.png')
st.title('Relatório de Acompanhamento de Escolas/Redes')

st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: #4A8AE8;
        }
        </style>""",
        unsafe_allow_html=True,
    )

######################## Barra lateral ########################

image = Image.open('[LOGO] Eduqo.png')
st.sidebar.image(image,caption='Eduqo - Plataforma QMágico',use_column_width=True)
st.sidebar.markdown('Feito por : Alexandre Fernandes (Padre)')

######################## Introdução ########################

st.subheader('**Período de análise**: *08/06/2021 e 06/09/2021*')

######################## Junção namespaces e informações do Hubspot ########################

namespaces_x_hubspot = pd.merge(namespaces, informacoes_hubspot, on = ['namespace','Produto'], how = 'left')
namespaces_x_hubspot2 = namespaces_x_hubspot.drop(columns = ['Unnamed: 0_x','Unnamed: 0_y','Interações A.A','Interações Cadernos'])
namespaces_x_hubspot3 = pd.merge(namespaces_x_hubspot2, namespace_rede, on = 'namespace', how = 'left')

######################## Descrição do Relatório ########################

"""
    ### 🎯 **Objetivo do Relatório**
    Esse relatório objetiva reduzir o tempo necessário para analisar o uso da plataforma por escolas e redes.

    O primeiro pilar consiste das **Rotinas Pedagógicas Digitais**.
"""
######################## Informações sobre os dados ########################

"""
    ### 🔍 **Informações sobre os dados analisados**
"""

st.write('**Total de namespaces analisados**: '+str(namespaces_x_hubspot2['namespace'].nunique()))

with st.expander("Por produto -> (clique aqui 🖱️)"):
    namespaces_x_hubspot2_diagnostico = namespaces_x_hubspot2[namespaces_x_hubspot2['Produto'] == 'Diagnóstico']
    st.write('**Diagnóstiqo**: '+str(namespaces_x_hubspot2_diagnostico['namespace'].nunique()))
    namespaces_x_hubspot2_pedagogico = namespaces_x_hubspot2[namespaces_x_hubspot2['Produto'] == 'Pedagógico']
    st.write('**Pedagógiqo**: '+str(namespaces_x_hubspot2_pedagogico['namespace'].nunique()))

with st.expander("Por faixa de licenças -> (clique aqui 🖱️)"):
    namespaces_x_hubspot2_030 = namespaces_x_hubspot2[namespaces_x_hubspot2['licenças'] == '0 - 30']
    st.write('**Entre 0 e 30 alunos**: '+str(namespaces_x_hubspot2_030['namespace'].nunique()))
    namespaces_x_hubspot2_30400 = namespaces_x_hubspot2[namespaces_x_hubspot2['licenças'] == '30 - 400']
    st.write('**Entre 30 e 400 alunos**: '+str(namespaces_x_hubspot2_30400['namespace'].nunique()))
    namespaces_x_hubspot2_400800 = namespaces_x_hubspot2[namespaces_x_hubspot2['licenças'] == '400 - 800']
    st.write('**Entre 400 e 800 alunos**: '+str(namespaces_x_hubspot2_400800['namespace'].nunique()))
    namespaces_x_hubspot2_8001200 = namespaces_x_hubspot2[namespaces_x_hubspot2['licenças'] == '800 - 1200']
    st.write('**Entre 800 e 1200 alunos**: '+str(namespaces_x_hubspot2_8001200['namespace'].nunique()))
    namespaces_x_hubspot2_1200x = namespaces_x_hubspot2[namespaces_x_hubspot2['licenças'] == '1200 - x']
    st.write('**Mais de 1200 alunos**: '+str(namespaces_x_hubspot2_1200x['namespace'].nunique()))

with st.expander("Por gestor de conta -> (clique aqui 🖱️)"):
    namespaces_x_hubspot2_gestor = namespaces_x_hubspot2.groupby('Deal Owner').nunique().reset_index()
    namespaces_x_hubspot2_gestor['Deal Owner'].replace('0','Sem informação no Hubspot', inplace = True)
    for i in range(len(namespaces_x_hubspot2_gestor['Deal Owner'])):
        st.write('**'+str(namespaces_x_hubspot2_gestor['Deal Owner'][i])+'**: '+str(namespaces_x_hubspot2_gestor['namespace'][i]))

######################## Rotinas Pedagógicas Digitais ########################

st.header('**Rotinas Pedagógicas Digitais**')
st.image('Rotinas Pedagógicas Digitais.png', use_column_width=True, caption='Rotinas Pedagógicas Digitais')

######################## Filtros na barra lateral ########################

###### Redes ######
rede = namespaces_x_hubspot3.sort_values(by = 'name')
rede2 = inserir_linha(pd.DataFrame(data = rede['name'].unique()),pd.DataFrame({0: 'Rede'}, index=[-1]))
rede_select = st.sidebar.selectbox('Selecione uma rede', rede2)

###### Grupo ######
if rede_select != 'Rede':
    grupo_ = rede[rede['name'] == rede_select]
    grupo = grupo_.sort_values(by = 'grupo')
else:
    grupo = rede.sort_values(by = 'grupo')
grupo2 = inserir_linha(pd.DataFrame(data = grupo['grupo'].unique()),pd.DataFrame({0: 'Grupo'}, index=[-1]))
grupo_select = st.sidebar.selectbox('Selecione um grupo', grupo2)

###### Gestor de contas ######
if grupo_select != 'Grupo':
    gestor_ = grupo[grupo['grupo'] == grupo_select]
    gestor = gestor_.sort_values(by = 'Deal Owner')
else:
    gestor = grupo.sort_values(by = 'Deal Owner')
gestor2 = inserir_linha(pd.DataFrame(data = gestor['Deal Owner'].unique()),pd.DataFrame({0: 'Gestor'}, index=[-1]))
gestor_select = st.sidebar.selectbox('Selecione um gestor', gestor2)

###### Produto ######
if gestor_select != 'Gestor':
    produto_ = gestor[gestor['Deal Owner'] == gestor_select]
    produto = produto_.sort_values(by = 'Produto')
else:
    produto = gestor.sort_values(by = 'Produto')
produto2 = inserir_linha(pd.DataFrame(data = produto['Produto'].unique()),pd.DataFrame({0: 'Produto'}, index=[-1]))
produto_select = st.sidebar.selectbox('Selecione um produto', produto2)

###### Faixa de licenças ######
if produto_select != 'Produto':
    licenças_ = produto[produto['Produto'] == produto_select]
    licenças = licenças_.sort_values(by = 'licenças')
else:
    licenças = produto.sort_values(by = 'licenças')
licenças2 = inserir_linha(pd.DataFrame(data = licenças['licenças'].unique()),pd.DataFrame({0: 'Faixa de licenças'}, index=[-1]))
licenças_select = st.sidebar.selectbox('Selecione uma faixa de licenças', licenças2)

###### Namespace ######
if licenças_select != 'Faixa de licenças':
    namespace_ = licenças[licenças['licenças'] == licenças_select]
    namespace = namespace_.sort_values(by = 'namespace')
else:
    namespace = licenças.sort_values(by = 'namespace')
namespace2 = inserir_linha(pd.DataFrame(data = namespace['namespace'].unique()),pd.DataFrame({0: 'Namespace'}, index=[-1]))
namespace_select = st.sidebar.selectbox('Selecione um namespace', namespace2)

######################## Resultados gerais por rotina ########################
if namespace_select != 'Namespace':
    st.subheader('**Resultados gerais por Rotina Pedagógica Digital**')

    ############## Avaliação Diagnóstica ##############

    ###### Leitura dos dados de cada rotina por namespace ######
    avaliacao_diagnostica_namespace = pd.read_csv('./CSV/Avaliação Diagnóstica/Resultados por namespace/avaliacao_diagnostica_namespace.csv')
    avaliacao_diagnostica_namespace2 = pd.merge(namespaces_x_hubspot3['namespace'],avaliacao_diagnostica_namespace, on = 'namespace', how = 'left')
    avaliacao_diagnostica_namespace3 = avaliacao_diagnostica_namespace2.groupby('namespace').mean().reset_index()
    avaliacao_diagnostica_namespace4 = avaliacao_diagnostica_namespace3.drop(columns = ['Unnamed: 0'])

    ###### Leitura dos dados de cada rotina por ano escolar ######
    avaliacao_diagnostica_anoescolar = pd.read_csv('./CSV/Avaliação Diagnóstica/Resultados por ano escolar/avaliacao_diagnostica_anoescolar.csv')
    avaliacao_diagnostica_anoescolar2 = pd.merge(namespaces_x_hubspot3['namespace'],avaliacao_diagnostica_anoescolar, on = 'namespace', how = 'left')
    #st.dataframe(avaliacao_diagnostica_anoescolar2)
    ###### Normalização dos dados ######
    for coluna in avaliacao_diagnostica_namespace4.columns:
        if coluna in ('Nº de AAs aplicadas da estante','Média de exercícios em relatórios de AD por turma'):
            avaliacao_diagnostica_namespace4 = normalizacao(avaliacao_diagnostica_namespace4,coluna,0.1, 0.9)
        if coluna in ('Média de exercícios em relatórios de AD por turma'):
            avaliacao_diagnostica_anoescolar2 = normalizacao(avaliacao_diagnostica_anoescolar2,coluna,0.1, 0.9)

    ###### Média Final ######
    col = avaliacao_diagnostica_namespace4.loc[: , "Porcentagem de exercícios de AAs em relatórios de AD":"Porcentagem de administradores que visualizaram relatórios de AD"]
    avaliacao_diagnostica_namespace4['Média'] = col.mean(axis=1)
    col = avaliacao_diagnostica_anoescolar2.loc[: , "Porcentagem de exercícios de AAs em relatórios de AD":"Porcentagem de visualização dos relatórios de AD por alunos"]
    avaliacao_diagnostica_anoescolar2['Média'] = col.mean(axis=1)
    avaliacao_diagnostica_anoescolar3 = avaliacao_diagnostica_anoescolar2.drop(columns = ['Unnamed: 0'])

    ###### Quartis ######
    avaliacao_diagnostica_namespace5 = quartis(avaliacao_diagnostica_namespace4,'Média')
    avaliacao_diagnostica_namespace_select = avaliacao_diagnostica_namespace5[avaliacao_diagnostica_namespace5['namespace'] == namespace_select].reset_index(drop = True)
    avaliacao_diagnostica_anoescolar4 = quartis(avaliacao_diagnostica_anoescolar3,'Média')
    avaliacao_diagnostica_anoescolar_select = avaliacao_diagnostica_anoescolar4[avaliacao_diagnostica_anoescolar4['namespace'] == namespace_select].reset_index(drop = True)

    ###### Média do namespace x média Eduqo ######
    if avaliacao_diagnostica_namespace_select['Média'][0] >= avaliacao_diagnostica_namespace5['Média'].mean():
        comparativo_media_avaliacao_diagnostica = ' 🟩'
    else:
        comparativo_media_avaliacao_diagnostica = ' 🟨'
    st.subheader('**Avaliação Diagnóstica'+' (Pontuação: '+str(round(100*avaliacao_diagnostica_namespace_select['Média'][0], 2))+')**')
    st.markdown('O namespace '+namespace_select+ ' está no **'+avaliacao_diagnostica_namespace_select['Quartil'][0]+ ' quartil**!') 
    st.progress(avaliacao_diagnostica_namespace_select['Média'][0])
    st.write('Pontuação **Média Eduqo: '+str(round(100*avaliacao_diagnostica_namespace5['Média'].mean(), 2))+comparativo_media_avaliacao_diagnostica+'**')

    ###### Junção Hubspot para pegar média das escolas que tem o mesmo produto e mesma faixa de licenças ######
    juncao_hubspot_diagnostica_namespace = pd.merge(namespaces_x_hubspot3,avaliacao_diagnostica_namespace5, on = 'namespace', how = 'left')
    avaliacao_diagnostica_namespace_select_juncao = juncao_hubspot_diagnostica_namespace[juncao_hubspot_diagnostica_namespace['namespace'] == namespace_select].reset_index(drop = True)
    juncao_hubspot_diagnostica_namespace2 = juncao_hubspot_diagnostica_namespace[juncao_hubspot_diagnostica_namespace['Produto'] == avaliacao_diagnostica_namespace_select_juncao['Produto'][0]]
    juncao_hubspot_diagnostica_namespace3 = juncao_hubspot_diagnostica_namespace2[juncao_hubspot_diagnostica_namespace2['licenças'] == avaliacao_diagnostica_namespace_select_juncao['licenças'][0]]
    if avaliacao_diagnostica_namespace_select['Média'][0] >= juncao_hubspot_diagnostica_namespace3['Média'].mean():
        comparativo_media_avaliacao_diagnostica_juncao = ' 🟩'
    else:
        comparativo_media_avaliacao_diagnostica_juncao = ' 🟨'
    st.write('Pontuação **Média '+avaliacao_diagnostica_namespace_select_juncao['Produto'][0]+' com faixa de licenças de '+avaliacao_diagnostica_namespace_select_juncao['licenças'][0]+': '+str(round(100*juncao_hubspot_diagnostica_namespace3['Média'].mean(), 2))+comparativo_media_avaliacao_diagnostica_juncao+'**')

    ###### Gráfico por ano escolar ######
    juncao_hubspot_diagnostica_anoescolar = pd.merge(namespaces_x_hubspot3,avaliacao_diagnostica_anoescolar4, on = 'namespace', how = 'left')
    avaliacao_diagnostica_anoescolar_select_juncao = juncao_hubspot_diagnostica_anoescolar[juncao_hubspot_diagnostica_anoescolar['namespace'] == namespace_select].reset_index(drop = True)
    juncao_hubspot_diagnostica_anoescolar2 = juncao_hubspot_diagnostica_anoescolar[juncao_hubspot_diagnostica_anoescolar['Produto'] == avaliacao_diagnostica_anoescolar_select_juncao['Produto'][0]]
    juncao_hubspot_diagnostica_anoescolar3 = juncao_hubspot_diagnostica_anoescolar2[juncao_hubspot_diagnostica_anoescolar2['licenças'] == avaliacao_diagnostica_anoescolar_select_juncao['licenças'][0]]

    with st.expander("Visualizar a média de Avaliação Diagnóstica por ano escolar -> (clique aqui 🖱️)"):
        avaliacao_diagnostica_anoescolar_select['Média'] = 100*avaliacao_diagnostica_anoescolar_select['Média']
        avaliacao_diagnostica_anoescolar_select2 = avaliacao_diagnostica_anoescolar_select.sort_values(by = 'grade')
        avaliacao_diagnostica_anoescolar5 = avaliacao_diagnostica_anoescolar4.groupby('grade').mean().reset_index()
        avaliacao_diagnostica_anoescolar6 = avaliacao_diagnostica_anoescolar5.sort_values(by = 'grade')
        juncao_hubspot_diagnostica_anoescolar4 = juncao_hubspot_diagnostica_anoescolar3.groupby('grade').mean().reset_index()
        juncao_hubspot_diagnostica_anoescolar5 = juncao_hubspot_diagnostica_anoescolar4.sort_values(by = 'grade')
        juncao_auxiliar_diagnostica = pd.merge(avaliacao_diagnostica_anoescolar6,juncao_hubspot_diagnostica_anoescolar5, on = 'grade', how = 'left')
        juncao_auxiliar_diagnostica2 = pd.merge(juncao_auxiliar_diagnostica,avaliacao_diagnostica_anoescolar_select2, on = 'grade', how = 'left')
        juncao_auxiliar_diagnostica3 = juncao_auxiliar_diagnostica2[juncao_auxiliar_diagnostica2['grade'] != '0']
        fig2 = px.bar(juncao_auxiliar_diagnostica3, x = juncao_auxiliar_diagnostica3['grade'], y = juncao_auxiliar_diagnostica3['Média'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(juncao_auxiliar_diagnostica3))
        fig2.add_scatter(x = juncao_auxiliar_diagnostica3['grade'], y = 100*juncao_auxiliar_diagnostica3['Média_x'], name = 'Média Eduqo', line=dict(color="red"))
        fig2.add_scatter(x = juncao_auxiliar_diagnostica3['grade'], y = 100*juncao_auxiliar_diagnostica3['Média_y'], name = 'Média '+avaliacao_diagnostica_anoescolar_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_diagnostica_anoescolar_select_juncao['licenças'][0], line=dict(color="black"))
        fig2.update_layout(title = "Pontuação média em Avaliação Diagnóstica por ano escolar")
        fig2.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
        st.plotly_chart(fig2)

    st.write('---')

    ############## Avaliação Somativa ##############

    ###### Leitura dos dados de cada rotina por namespace ######
    avaliacao_somativa_namespace = pd.read_csv('./CSV/Avaliação Somativa/Resultados por namespace/avaliacao_somativa_namespace.csv')
    avaliacao_somativa_namespace2 = pd.merge(namespaces_x_hubspot3['namespace'],avaliacao_somativa_namespace, on = 'namespace', how = 'left')

    ###### Leitura dos dados de cada rotina temporal ######
    avaliacao_somativa_temporal = pd.read_csv('./CSV/Avaliação Somativa/Resultados temporais/avaliacao_somativa_temporal.csv')
    avaliacao_somativa_temporal2 = pd.merge(namespaces_x_hubspot3['namespace'],avaliacao_somativa_temporal, on = 'namespace', how = 'left')

    ###### Leitura dos dados de cada rotina por ano escolar ######
    avaliacao_somativa_anoescolar = pd.read_csv('./CSV/Avaliação Somativa/Resultados por ano escolar/avaliacao_somativa_anoescolar.csv')
    avaliacao_somativa_anoescolar2_aux = pd.merge(namespaces_x_hubspot3['namespace'],avaliacao_somativa_anoescolar, on = 'namespace', how = 'left')
    avaliacao_somativa_anoescolar2 = avaliacao_somativa_anoescolar2_aux.groupby(['namespace','grade']).mean().reset_index()
    
    ###### Normalização dos dados por namespace ######
    for coluna in avaliacao_somativa_namespace2.columns:
        if coluna in ('Número de AAs por turma','Média de exercícios de AA por turma'):
            avaliacao_somativa_namespace2 = normalizacao(avaliacao_somativa_namespace2,coluna,0.1, 0.9)
        if coluna in ('Tempo médio entre publicação e ínicio de AA'):
            avaliacao_somativa_namespace2 = normalizacao_datetime(avaliacao_somativa_namespace2,coluna,0.1, 0.9)
        if coluna in ('Tempo de correção por aluno por questão','Tempo médio entre criação e publicação de AA por questão'):
            avaliacao_somativa_namespace2 = normalizacao_datetime_inversa(avaliacao_somativa_namespace2,coluna,0.1, 0.9)
    avaliacao_somativa_namespace3 = avaliacao_somativa_namespace2.drop(columns = ['Unnamed: 0'])

    ###### Normalização dos dados temporais ######
    for coluna in avaliacao_somativa_temporal2.columns:
        if coluna in ('Número de AAs por turma','Média de exercícios de AA por turma'):
            avaliacao_somativa_temporal2 = normalizacao(avaliacao_somativa_temporal2,coluna,0.1, 0.9)
        if coluna in ('Tempo médio entre publicação e ínicio de AA'):
            avaliacao_somativa_temporal2 = normalizacao_datetime(avaliacao_somativa_temporal2,coluna,0.1, 0.9)
        if coluna in ('Tempo de correção por aluno por questão','Tempo médio entre criação e publicação de AA por questão'):
            avaliacao_somativa_temporal2 = normalizacao_datetime_inversa(avaliacao_somativa_temporal2,coluna,0.1, 0.9)
    avaliacao_somativa_temporal3 = avaliacao_somativa_temporal2.drop(columns = ['Unnamed: 0'])

    ###### Normalização dos dados temporais ######
    for coluna in avaliacao_somativa_anoescolar2.columns:
        if coluna in ('Número de AAs por turma','Média de exercícios de AA por turma'):
            avaliacao_somativa_anoescolar2 = normalizacao(avaliacao_somativa_anoescolar2,coluna,0.1, 0.9)
        if coluna in ('Tempo médio entre publicação e ínicio de AA'):
            avaliacao_somativa_anoescolar2 = normalizacao_datetime(avaliacao_somativa_anoescolar2,coluna,0.1, 0.9)
        if coluna in ('Tempo de correção por aluno por questão','Tempo médio entre criação e publicação de AA por questão'):
            avaliacao_somativa_anoescolar2 = normalizacao_datetime_inversa(avaliacao_somativa_anoescolar2,coluna,0.1, 0.9)
    avaliacao_somativa_anoescolar3 = avaliacao_somativa_anoescolar2.drop(columns = ['Unnamed: 0'])
    
    ###### Média Final ######
    col = avaliacao_somativa_namespace3.loc[: , "Porcentagem de engajamento em AAs":"Porcentagem de administrantes que visualizaram relatórios de AA"]
    avaliacao_somativa_namespace3['Média'] = col.mean(axis=1)
    col = avaliacao_somativa_temporal3.loc[: , "Porcentagem de engajamento em AAs":"Porcentagem de relatórios de AA visualizados por docente"]
    avaliacao_somativa_temporal3['Média'] = col.mean(axis=1)
    col = avaliacao_somativa_anoescolar3.loc[: , "Porcentagem de engajamento em AAs":"Porcentagem de visualização de relatórios de AA"]
    avaliacao_somativa_anoescolar3['Média'] = col.mean(axis=1)
    
    ###### Quartis ######
    avaliacao_somativa_namespace4 = quartis(avaliacao_somativa_namespace3,'Média')
    avaliacao_somativa_namespace_select = avaliacao_somativa_namespace4[avaliacao_somativa_namespace4['namespace'] == namespace_select].reset_index(drop = True)
    avaliacao_somativa_temporal4 = quartis(avaliacao_somativa_temporal3,'Média')
    avaliacao_somativa_temporal_select = avaliacao_somativa_temporal4[avaliacao_somativa_temporal4['namespace'] == namespace_select].reset_index(drop = True)
    avaliacao_somativa_anoescolar4 = quartis(avaliacao_somativa_anoescolar3,'Média')
    avaliacao_somativa_anoescolar_select = avaliacao_somativa_anoescolar4[avaliacao_somativa_anoescolar4['namespace'] == namespace_select].reset_index(drop = True)
    
    ###### Média do namespace x média Eduqo ######
    if avaliacao_somativa_namespace_select['Média'][0] >= avaliacao_somativa_namespace4['Média'].mean():
        comparativo_media_avaliacao_somativa = ' 🟩'
    else:
        comparativo_media_avaliacao_somativa = ' 🟨'
    st.subheader('**Avaliação Somativa'+' (Pontuação: '+str(round(100*avaliacao_somativa_namespace_select['Média'][0], 2))+')**')
    st.markdown('O namespace '+namespace_select+ ' está no **'+avaliacao_somativa_namespace_select['Quartil'][0]+ ' quartil**!') 
    st.progress(avaliacao_somativa_namespace_select['Média'][0])
    st.write('Pontuação **Média Eduqo: '+str(round(100*avaliacao_somativa_namespace4['Média'].mean(), 2))+comparativo_media_avaliacao_somativa+'**')

    ###### Junção Hubspot para pegar média das escolas que tem o mesmo produto e mesma faixa de licenças ######
    juncao_hubspot_somativa_namespace = pd.merge(namespaces_x_hubspot3,avaliacao_somativa_namespace4, on = 'namespace', how = 'left')
    avaliacao_somativa_namespace_select_juncao = juncao_hubspot_somativa_namespace[juncao_hubspot_somativa_namespace['namespace'] == namespace_select].reset_index(drop = True)
    juncao_hubspot_somativa_namespace2 = juncao_hubspot_somativa_namespace[juncao_hubspot_somativa_namespace['Produto'] == avaliacao_somativa_namespace_select_juncao['Produto'][0]]
    juncao_hubspot_somativa_namespace3 = juncao_hubspot_somativa_namespace2[juncao_hubspot_somativa_namespace2['licenças'] == avaliacao_somativa_namespace_select_juncao['licenças'][0]]
    if avaliacao_somativa_namespace_select['Média'][0] >= juncao_hubspot_somativa_namespace3['Média'].mean():
        comparativo_media_avaliacao_somativa_juncao = ' 🟩'
    else:
        comparativo_media_avaliacao_somativa_juncao = ' 🟨'
    st.write('Pontuação **Média '+avaliacao_somativa_namespace_select_juncao['Produto'][0]+' com faixa de licenças de '+avaliacao_somativa_namespace_select_juncao['licenças'][0]+': '+str(round(100*juncao_hubspot_somativa_namespace3['Média'].mean(), 2))+comparativo_media_avaliacao_somativa_juncao+'**')
    
    ###### Gráfico temporal ######
    juncao_hubspot_somativa_temporal = pd.merge(namespaces_x_hubspot3,avaliacao_somativa_temporal4, on = 'namespace', how = 'left')
    avaliacao_somativa_temporal_select_juncao = juncao_hubspot_somativa_temporal[juncao_hubspot_somativa_temporal['namespace'] == namespace_select].reset_index(drop = True)
    juncao_hubspot_somativa_temporal2 = juncao_hubspot_somativa_temporal[juncao_hubspot_somativa_temporal['Produto'] == avaliacao_somativa_temporal_select_juncao['Produto'][0]]
    juncao_hubspot_somativa_temporal3 = juncao_hubspot_somativa_temporal2[juncao_hubspot_somativa_temporal2['licenças'] == avaliacao_somativa_temporal_select_juncao['licenças'][0]]

    with st.expander("Visualizar o histórico semanal da média de Avaliação Somativa -> (clique aqui 🖱️)"):
        avaliacao_somativa_temporal_select['Média'] = 100*avaliacao_somativa_temporal_select['Média']
        fig = px.bar(avaliacao_somativa_temporal_select, x = avaliacao_somativa_temporal_select['Semana'], y = avaliacao_somativa_temporal_select['Média'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(avaliacao_somativa_temporal_select))
        avaliacao_somativa_temporal5 = avaliacao_somativa_temporal4.groupby('Semana').mean().reset_index()
        fig.add_scatter(x = avaliacao_somativa_temporal5['Semana'], y = 100*avaliacao_somativa_temporal5['Média'],mode='lines', name = 'Média Eduqo', line=dict(color="red"))
        juncao_hubspot_somativa_temporal4 = juncao_hubspot_somativa_temporal3.groupby('Semana').mean().reset_index()
        fig.add_scatter(x = juncao_hubspot_somativa_temporal4['Semana'], y = 100*juncao_hubspot_somativa_temporal4['Média'],mode='lines', name = 'Média '+avaliacao_somativa_temporal_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_somativa_temporal_select_juncao['licenças'][0], line=dict(color="black"))
        fig.update_layout(title = "Pontuação média em Avaliação Somativa por semana")
        fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
        st.plotly_chart(fig)

    ###### Gráfico por ano escolar ######
    juncao_hubspot_somativa_anoescolar = pd.merge(namespaces_x_hubspot3,avaliacao_somativa_anoescolar4, on = 'namespace', how = 'left')
    avaliacao_somativa_anoescolar_select_juncao = juncao_hubspot_somativa_anoescolar[juncao_hubspot_somativa_anoescolar['namespace'] == namespace_select].reset_index(drop = True)
    juncao_hubspot_somativa_anoescolar2 = juncao_hubspot_somativa_anoescolar[juncao_hubspot_somativa_anoescolar['Produto'] == avaliacao_somativa_anoescolar_select_juncao['Produto'][0]]
    juncao_hubspot_somativa_anoescolar3 = juncao_hubspot_somativa_anoescolar2[juncao_hubspot_somativa_anoescolar2['licenças'] == avaliacao_somativa_anoescolar_select_juncao['licenças'][0]]

    with st.expander("Visualizar a média de Avaliação Somativa por ano escolar -> (clique aqui 🖱️)"):
        avaliacao_somativa_anoescolar_select['Média'] = 100*avaliacao_somativa_anoescolar_select['Média']
        avaliacao_somativa_anoescolar_select2 = avaliacao_somativa_anoescolar_select.sort_values(by = 'grade')
        avaliacao_somativa_anoescolar5 = avaliacao_somativa_anoescolar4.groupby('grade').mean().reset_index()
        avaliacao_somativa_anoescolar6 = avaliacao_somativa_anoescolar5.sort_values(by = 'grade')
        juncao_hubspot_somativa_anoescolar4 = juncao_hubspot_somativa_anoescolar3.groupby('grade').mean().reset_index()
        juncao_hubspot_somativa_anoescolar5 = juncao_hubspot_somativa_anoescolar4.sort_values(by = 'grade')
        juncao_auxiliar = pd.merge(avaliacao_somativa_anoescolar6,juncao_hubspot_somativa_anoescolar5, on = 'grade', how = 'left')
        juncao_auxiliar2 = pd.merge(juncao_auxiliar,avaliacao_somativa_anoescolar_select2, on = 'grade', how = 'left')
        fig2 = px.bar(juncao_auxiliar2, x = juncao_auxiliar2['grade'], y = juncao_auxiliar2['Média'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(juncao_auxiliar2))
        fig2.add_scatter(x = juncao_auxiliar2['grade'], y = 100*juncao_auxiliar2['Média_x'], name = 'Média Eduqo', line=dict(color="red"))
        fig2.add_scatter(x = juncao_auxiliar2['grade'], y = 100*juncao_auxiliar2['Média_y'], name = 'Média '+avaliacao_somativa_anoescolar_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_somativa_anoescolar_select_juncao['licenças'][0], line=dict(color="black"))
        fig2.update_layout(title = "Pontuação média em Avaliação Somativa por ano escolar")
        fig2.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
        st.plotly_chart(fig2)
        
        

    ######################## Resultados detalhados por rotina ########################

    st.subheader('**Resultados detalhados por Rotina Pedagógica Digital**')

    ############## Avaliação Diagnóstica ##############

    st.markdown('**Avaliação Diagnóstica**')

    ###### Namespaces destaques ######
    avaliacao_diagnostica_namespace6 = avaliacao_diagnostica_namespace5.copy()
    avaliacao_diagnostica_namespace6['Média'] = round(100*avaliacao_diagnostica_namespace6['Média'],2)
    avaliacao_diagnostica_namespace6.rename(columns = {'Média':'Média (0 a 100)'}, inplace = True)
    avaliacao_diagnostica_namespace7 = pd.DataFrame()
    avaliacao_diagnostica_namespace7['namespace'] = avaliacao_diagnostica_namespace6['namespace']
    avaliacao_diagnostica_namespace7['Média (0 a 100)'] = avaliacao_diagnostica_namespace6['Média (0 a 100)']
    avaliacao_diagnostica_namespace7['Quartil'] = avaliacao_diagnostica_namespace6['Quartil']
    avaliacao_diagnostica_namespace8 = avaliacao_diagnostica_namespace7.groupby('namespace').mean()
    avaliacao_diagnostica_namespace9 = quartis(avaliacao_diagnostica_namespace8,'Média (0 a 100)').reset_index()
    avaliacao_diagnostica_namespace10 = avaliacao_diagnostica_namespace9.sort_values(by = 'Média (0 a 100)', ascending = False)
    with st.expander("Visualizar as escolas destaque em Avaliação Somativa -> (clique aqui 🖱️)"):
        avaliacao_diagnostica_namespace11 = destaques_rotina(avaliacao_diagnostica_namespace10)
        st.table(avaliacao_diagnostica_namespace11)

    ###### Visualizar um quartil ######
    ver_quartil_avaliacao_diagnostica = st.radio('Escolha o quartil que deseja ver os resultados de Avaliação Diagnóstica 📈',('Nenhum','1º','2º','3º','4º'))
    if ver_quartil_avaliacao_diagnostica != 'Nenhum':
        avaliacao_diagnostica_namespace_quartil = visualizacao_resultado_quartil(ver_quartil_avaliacao_diagnostica,avaliacao_diagnostica_namespace10)
        st.table(avaliacao_diagnostica_namespace_quartil)

    ###### Visualização das métricas do namespace selecionado ######
    with st.expander("Visualizar os resultados de Avaliação Diagnóstica do namespace selecionado por métrica -> (clique aqui 🖱️)"):
        for coluna in avaliacao_diagnostica_namespace_select.columns:
            if (coluna != 'namespace' and coluna != 'Média' and coluna != 'Quartil'):
                if avaliacao_diagnostica_namespace_select[coluna][0] >= avaliacao_diagnostica_namespace6[coluna].mean():
                    comparativo_media_avaliacao_diagnostica = ' 🟩'
                else:
                    comparativo_media_avaliacao_diagnostica = ' 🟨'
                st.markdown('**'+coluna+' (Pontuação: '+str(round(100*avaliacao_diagnostica_namespace_select[coluna][0], 2))+')**')
                st.progress(avaliacao_diagnostica_namespace_select[coluna][0])
                st.write('**Média Eduqo: '+str(round(100*avaliacao_diagnostica_namespace6[coluna].mean(), 2))+comparativo_media_avaliacao_diagnostica+'**')
                if avaliacao_diagnostica_namespace_select[coluna][0] >= juncao_hubspot_diagnostica_namespace3[coluna].mean():
                    comparativo_media_avaliacao_diagnostica_juncao = ' 🟩'
                else:
                    comparativo_media_avaliacao_diagnostica_juncao = ' 🟨'
                st.write('**Média '+avaliacao_diagnostica_namespace_select_juncao['Produto'][0]+' com faixa de licenças de '+avaliacao_diagnostica_namespace_select_juncao['licenças'][0]+': '+str(round(100*juncao_hubspot_diagnostica_namespace3[coluna].mean(), 2))+comparativo_media_avaliacao_diagnostica_juncao+'**')
                if coluna in ('Porcentagem de exercícios de AAs em relatórios de AD','Média de exercícios em relatórios de AD por turma','Porcentagem de AAs com classificação de habilidades iniciada','Porcentagem de AAs com classificação de habilidades finalizada','Porcentagem de AAs com classificação de habilidades finalizada (ao menos foi iniciada)','Porcentagem de visualização dos relatórios de AD por alunos'):
                    beta = st.checkbox('Visualizar resultados por ano escolar de '+coluna+' -> (clique aqui 🖱️)')
                    if beta == True:
                        juncao_auxiliar_diagnostica3[coluna] = 100*juncao_auxiliar_diagnostica3[coluna]
                        fig2 = px.bar(juncao_auxiliar_diagnostica3, x = juncao_auxiliar_diagnostica3['grade'], y = juncao_auxiliar_diagnostica3[coluna], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(juncao_auxiliar_diagnostica3))
                        fig2.add_scatter(x = juncao_auxiliar_diagnostica3['grade'], y = 100*juncao_auxiliar_diagnostica3[coluna+'_x'], name = 'Média Eduqo', line=dict(color="red"))
                        fig2.add_scatter(x = juncao_auxiliar_diagnostica3['grade'], y = 100*juncao_auxiliar_diagnostica3[coluna+'_y'], name = 'Média '+avaliacao_diagnostica_anoescolar_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_diagnostica_anoescolar_select_juncao['licenças'][0], line=dict(color="black"))
                        fig2.update_layout(title = "Pontuação média em Avaliação Diagnóstica por ano escolar")
                        fig2.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
                        st.plotly_chart(fig2)
                st.write('----')


    ############## Avaliação Somativa ##############

    st.markdown('**Avaliação Somativa**')

    ###### Namespaces destaques ######
    avaliacao_somativa_namespace5 = avaliacao_somativa_namespace4.copy()
    avaliacao_somativa_namespace5['Média'] = round(100*avaliacao_somativa_namespace5['Média'],2)
    avaliacao_somativa_namespace5.rename(columns = {'Média':'Média (0 a 100)'}, inplace = True)
    avaliacao_somativa_namespace6 = pd.DataFrame()
    avaliacao_somativa_namespace6['namespace'] = avaliacao_somativa_namespace5['namespace']
    avaliacao_somativa_namespace6['Média (0 a 100)'] = avaliacao_somativa_namespace5['Média (0 a 100)']
    avaliacao_somativa_namespace6['Quartil'] = avaliacao_somativa_namespace5['Quartil']
    avaliacao_somativa_namespace7 = avaliacao_somativa_namespace6.groupby('namespace').mean()
    avaliacao_somativa_namespace8 = quartis(avaliacao_somativa_namespace7,'Média (0 a 100)').reset_index()
    avaliacao_somativa_namespace9 = avaliacao_somativa_namespace8.sort_values(by = 'Média (0 a 100)', ascending = False)
    with st.expander("Visualizar as escolas destaque em Avaliação Somativa -> (clique aqui 🖱️)"):
        avaliacao_somativa_namespace10 = destaques_rotina(avaliacao_somativa_namespace9)
        st.table(avaliacao_somativa_namespace10)

    ###### Visualizar um quartil ######
    ver_quartil_avaliacao_somativa = st.radio('Escolha o quartil que deseja ver os resultados de Avaliação Somativa 📈',('Nenhum','1º','2º','3º','4º'))
    if ver_quartil_avaliacao_somativa != 'Nenhum':
        avaliacao_somativa_namespace_quartil = visualizacao_resultado_quartil(ver_quartil_avaliacao_somativa,avaliacao_somativa_namespace9)
        st.table(avaliacao_somativa_namespace_quartil)

    ###### Visualização das métricas do namespace selecionado ######
    with st.expander("Visualizar os resultados de Avaliação Somativa do namespace selecionado por métrica -> (clique aqui 🖱️)"):
        for coluna in avaliacao_somativa_namespace_select.columns:
            if (coluna != 'namespace' and coluna != 'Média' and coluna != 'Quartil'):
                if avaliacao_somativa_namespace_select[coluna][0] >= avaliacao_somativa_namespace5[coluna].mean():
                    comparativo_media_avaliacao_somativa = ' 🟩'
                else:
                    comparativo_media_avaliacao_somativa = ' 🟨'
                st.markdown('**'+coluna+' (Pontuação: '+str(round(100*avaliacao_somativa_namespace_select[coluna][0], 2))+')**')
                st.progress(avaliacao_somativa_namespace_select[coluna][0])
                st.write('**Média Eduqo: '+str(round(100*avaliacao_somativa_namespace5[coluna].mean(), 2))+comparativo_media_avaliacao_somativa+'**')
                if avaliacao_somativa_namespace_select[coluna][0] >= juncao_hubspot_somativa_namespace3[coluna].mean():
                    comparativo_media_avaliacao_somativa_juncao = ' 🟩'
                else:
                    comparativo_media_avaliacao_somativa_juncao = ' 🟨'
                st.write('**Média '+avaliacao_somativa_namespace_select_juncao['Produto'][0]+' com faixa de licenças de '+avaliacao_somativa_namespace_select_juncao['licenças'][0]+': '+str(round(100*juncao_hubspot_somativa_namespace3[coluna].mean(), 2))+comparativo_media_avaliacao_somativa_juncao+'**')
                if coluna != 'Porcentagem de administrantes que visualizaram relatórios de AA':
                    beta = st.checkbox('Visualizar histórico semanal de '+coluna+' -> (clique aqui 🖱️)')
                    if beta == True:
                        avaliacao_somativa_temporal_select[coluna] = 100*avaliacao_somativa_temporal_select[coluna]
                        fig = px.bar(avaliacao_somativa_temporal_select, x = avaliacao_somativa_temporal_select['Semana'], y = coluna, range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(avaliacao_somativa_temporal_select))
                        avaliacao_somativa_temporal5 = avaliacao_somativa_temporal4.groupby('Semana').mean().reset_index()
                        fig.add_scatter(x = avaliacao_somativa_temporal5['Semana'], y = 100*avaliacao_somativa_temporal5[coluna],mode='lines', name = 'Média Eduqo', line=dict(color="red"))
                        juncao_hubspot_somativa_temporal4 = juncao_hubspot_somativa_temporal3.groupby('Semana').mean().reset_index()
                        fig.add_scatter(x = juncao_hubspot_somativa_temporal4['Semana'], y = 100*juncao_hubspot_somativa_temporal4[coluna],mode='lines', name = 'Média '+avaliacao_somativa_temporal_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_somativa_temporal_select_juncao['licenças'][0], line=dict(color="black"))
                        fig.update_layout(title = "Pontuação média por semana")
                        fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
                        st.plotly_chart(fig)
                if coluna in ('Porcentagem de engajamento em AAs','Número de AAs por turma','Média de exercícios de AA por turma','Porcentagem de visualização de relatórios de AA'):
                    beta = st.checkbox('Visualizar resultados por ano escolar de '+coluna+' -> (clique aqui 🖱️)')
                    if beta == True:
                        juncao_auxiliar2[coluna] = 100*juncao_auxiliar2[coluna]
                        fig2 = px.bar(juncao_auxiliar2, x = juncao_auxiliar2['grade'], y = juncao_auxiliar2[coluna], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(juncao_auxiliar2))
                        fig2.add_scatter(x = juncao_auxiliar2['grade'], y = 100*juncao_auxiliar2[coluna+'_x'], name = 'Média Eduqo', line=dict(color="red"))
                        fig2.add_scatter(x = juncao_auxiliar2['grade'], y = 100*juncao_auxiliar2[coluna+'_y'], name = 'Média '+avaliacao_somativa_anoescolar_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_somativa_anoescolar_select_juncao['licenças'][0], line=dict(color="black"))
                        fig2.update_layout(title = "Pontuação média em Avaliação Somativa por ano escolar")
                        fig2.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
                        st.plotly_chart(fig2)
                st.write('----')

else:
    st.warning('🙂 Escolha um namespace para visualizar seus resultados!')


