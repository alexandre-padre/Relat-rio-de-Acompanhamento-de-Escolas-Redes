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

# Importações de CSVs
avaliacao_somativa_namespace = pd.read_csv('./CSV/Avaliação Somativa/avaliacao_somativa.csv')
avaliacao_somativa_namespace2 = avaliacao_somativa_namespace[avaliacao_somativa_namespace['Média'] > 0]

## Título do relatório
st.image('[LOGO] Eduqo.png')
st.title('Relatório de Acompanhamento de Escolas/Redes')

## Barra lateral
image = Image.open('[LOGO] Eduqo.png')
st.sidebar.image(image,caption='Eduqo - Plataforma QMágico',use_column_width=True)
st.sidebar.markdown('Feito por : Alexandre Fernandes (Padre)')
st.sidebar.write("Repositório Github: [link] (https://github.com/alexandre-padre/Relat-rio-de-Acompanhamento-de-Escolas-Redes.git)")

## Introdução
st.subheader('Os dados analisados são do período entre 01/06/2021 e 29/08/2021')

## Seleção do namespace a ser analisado
namespace_select = st.sidebar.selectbox('Selecione um namespace', avaliacao_somativa_namespace2['namespace'])

st.subheader('Namespace selecionado: **'+namespace_select+'**')

### Rotinas
st.header('**Rotinas Pedagógicas Digitais**')

st.image('Rotinas Pedagógicas Digitais.png', use_column_width=True, caption='Rotinas Pedagógicas Digitais')

## Rotina de Avaliação Diagnóstica (Geral)

avaliacao_diagnostica_namespace = pd.read_csv('./CSV/Avaliação Diagnóstica/avaliacao_diagnostica.csv')

# Quartis Avaliação Diagnóstica
avaliacao_diagnostica_namespace_aux = quartis(avaliacao_diagnostica_namespace,'Média')

avaliacao_diagnostica_namespace2 = avaliacao_diagnostica_namespace_aux.drop(columns = 'Unnamed: 0')

avaliacao_diagnostica_namespace_select = avaliacao_diagnostica_namespace2[avaliacao_diagnostica_namespace2['namespace'] == namespace_select].reset_index(drop = True)

# Média do namespace
if avaliacao_diagnostica_namespace_select['Média'][0] >= avaliacao_diagnostica_namespace2['Média'].mean():
    comparativo_media_avaliacao_somativa = ' 🟩'
else:
    comparativo_media_avaliacao_somativa = ' 🟨'
st.subheader('**Avaliação Diagnóstica'+' (Pontuação: '+str(round(100*avaliacao_diagnostica_namespace_select['Média'][0], 2))+comparativo_media_avaliacao_somativa+')**')
st.markdown('***O namespace '+namespace_select+ ' está no '+avaliacao_diagnostica_namespace_select['Quartil'][0]+ ' quartil!***') 
st.progress(avaliacao_diagnostica_namespace_select['Média'][0])
st.write('Pontuação **Média Eduqo: '+str(round(100*avaliacao_diagnostica_namespace2['Média'].mean(), 2))+'**')

## Rotina de Avaliação Somativa (Geral)

# Quartis Avaliação Somativa
avaliacao_somativa_namespace4 = quartis(avaliacao_somativa_namespace2,'Média')

avaliacao_somativa_namespace5 = avaliacao_somativa_namespace4.drop(columns = 'Unnamed: 0')
avaliacao_somativa_namespace5.rename(columns = {"('Criação de AA', '')":'Criação de AA'}, inplace = True)

avaliacao_somativa_namespace_select = avaliacao_somativa_namespace5[avaliacao_somativa_namespace5['namespace'] == namespace_select].reset_index(drop = True)

# Média do namespace
if avaliacao_somativa_namespace_select['Média'][0] >= avaliacao_somativa_namespace5['Média'].mean():
    comparativo_media_avaliacao_somativa = ' 🟩'
else:
    comparativo_media_avaliacao_somativa = ' 🟨'
st.subheader('**Avaliação Somativa'+' (Pontuação: '+str(round(100*avaliacao_somativa_namespace_select['Média'][0], 2))+comparativo_media_avaliacao_somativa+')**')
st.markdown('***O namespace '+namespace_select+ ' está no '+avaliacao_somativa_namespace_select['Quartil'][0]+ ' quartil!***') 
st.progress(avaliacao_somativa_namespace_select['Média'][0])
st.write('Pontuação **Média Eduqo: '+str(round(100*avaliacao_somativa_namespace5['Média'].mean(), 2))+'**')
######################################################################################################

st.subheader('**Métricas detalhadas de cada rotina pedagógica**')

## Rotina de Avaliação Diagnóstica
st.markdown('**Avaliação Diagnóstica**')

# Ajustes na tabela de Avaliação Diagnóstica
avaliacao_diagnostica_namespace3 = avaliacao_diagnostica_namespace2.copy()
avaliacao_diagnostica_namespace3['Média'] = round(100*avaliacao_diagnostica_namespace3['Média'],2)
avaliacao_diagnostica_namespace3.rename(columns = {'Média':'Média (0 a 100)'}, inplace = True)

avaliacao_diagnostica_namespace4 = pd.DataFrame()
for coluna in avaliacao_diagnostica_namespace3.columns:
    if (coluna == 'namespace' or coluna == 'Média (0 a 100)' or coluna == 'Quartil'):
        avaliacao_diagnostica_namespace4[coluna] = avaliacao_diagnostica_namespace3[coluna]


# Visualização dos namespaces destaque
with st.expander("Visualizar as escolas destaque em Avaliação Diagnóstica -> (clique aqui 🖱️)"):
    avaliacao_diagnostica_namespace5 = destaques_rotina(avaliacao_diagnostica_namespace4)
    st.table(avaliacao_diagnostica_namespace5)

# Visualização dos quartis
ver_quartil_avaliacao_diagnostica = st.radio('Escolha o quartil que deseja ver os resultados de Avaliação Diagnóstica 📈',('Nenhum','1º','2º','3º','4º'))
if ver_quartil_avaliacao_diagnostica != 'Nenhum':
    avaliacao_diagnostica_namespace_quartil = visualizacao_resultado_quartil(ver_quartil_avaliacao_diagnostica,avaliacao_diagnostica_namespace4)
    st.table(avaliacao_diagnostica_namespace_quartil)

# Visualização das métricas do namespace selecionado
with st.expander("Visualizar os resultados de Avaliação Diagnóstica do namespace selecionado por métrica -> (clique aqui 🖱️)"):
    for coluna in avaliacao_diagnostica_namespace_select.loc[:,'Nº de AAs copiadas da estante mágica e aplicada':'Média de exercícios em relatórios de AD por turma']:
        if avaliacao_diagnostica_namespace_select[coluna][0] >= avaliacao_diagnostica_namespace2[coluna].mean():
            comparativo_media_avaliacao_diagnostica = ' 🟩'
        else:
            comparativo_media_avaliacao_diagnostica = ' 🟨'
        st.markdown('**'+coluna+' (Pontuação: '+str(round(100*avaliacao_diagnostica_namespace_select[coluna][0], 2))+comparativo_media_avaliacao_diagnostica+')**') 
        st.progress(avaliacao_diagnostica_namespace_select[coluna][0])
        st.write('Pontuação **Média Eduqo: '+str(round(100*avaliacao_diagnostica_namespace2[coluna].mean(), 2))+'**')

########################################################################################################

## Rotina de Avaliação Somativa
st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: #4A8AE8;
        }
        </style>""",
        unsafe_allow_html=True,
    )

# Ajustes na tabela de Avaliação Somativa
avaliacao_somativa_namespace6 = avaliacao_somativa_namespace5.copy()
avaliacao_somativa_namespace6['Média'] = round(100*avaliacao_somativa_namespace6['Média'],2)
avaliacao_somativa_namespace6.rename(columns = {'Média':'Média (0 a 100)'}, inplace = True)
avaliacao_somativa_namespace7 = avaliacao_somativa_namespace6.drop(columns = ['Porcentagem de engajamento em AAs','Média de AAs por turma','Média de exercícios por turma','Correção de exercícios discursivos','Criação de AA','Publicação da AA','Acesso à relatórios de AA por aluno','Porcentagem de visualização de relatórios de AA por professor','Porcentagem de administradores que visualizaram relatórios de AA'])

st.markdown('**Avaliação Somativa**')

# Visualização dos namespaces destaque
with st.expander("Visualizar as escolas destaque em Avaliação Somativa -> (clique aqui 🖱️)"):
    avaliacao_somativa_namespace8 = destaques_rotina(avaliacao_somativa_namespace7)
    st.table(avaliacao_somativa_namespace8)

# Visualização dos quartis
ver_quartil_avaliacao_somativa = st.radio('Escolha o quartil que deseja ver os resultados de Avaliação Somativa 📈',('Nenhum','1º','2º','3º','4º'))
if ver_quartil_avaliacao_somativa != 'Nenhum':
    avaliacao_somativa_namespace_quartil = visualizacao_resultado_quartil(ver_quartil_avaliacao_somativa,avaliacao_somativa_namespace7)
    st.table(avaliacao_somativa_namespace_quartil)

# Visualização das métricas do namespace selecionado
with st.expander("Visualizar os resultados de Avaliação Somativa do namespace selecionado por métrica -> (clique aqui 🖱️)"):
    for coluna in avaliacao_somativa_namespace_select.loc[:,'Porcentagem de engajamento em AAs':'Porcentagem de administradores que visualizaram relatórios de AA']:
        if avaliacao_somativa_namespace_select[coluna][0] >= avaliacao_somativa_namespace5[coluna].mean():
            comparativo_media_avaliacao_somativa = ' 🟩'
        else:
            comparativo_media_avaliacao_somativa = ' 🟨'
        st.markdown('**'+coluna+' (Pontuação: '+str(round(100*avaliacao_somativa_namespace_select[coluna][0], 2))+comparativo_media_avaliacao_somativa+')**') 
        if coluna == 'Porcentagem de engajamento em AAs':
            st.write('Essa métrica consiste na razão entre o número de exercícios realizados em relação aos disponibilizados (média entre os alunos)')
        if coluna == 'Correção de exercícios discursivos':
            st.write('Essa métrica consiste no tempo médio de correção de exercícios discursivos por questão por aluno')
        if coluna == 'Criação de AA':
            st.write('Essa métrica consiste no tempo médio entre a criação da AA e sua publicação')
        if coluna == 'Publicação da AA':
            st.write('Essa métrica consiste no tempo médio entre a publicação da AA e seu início')
        if coluna == 'Acesso à relatórios de AA por aluno':
            st.write('Essa métrica consiste na razão entre o número de AAs diferentes que o aluno visualizou o relatório e o número de AAs que esteve disponibilizado para ele.')
        if coluna == 'Porcentagem de visualização de relatórios de AA por professor':
            st.write('Essa métrica consiste na razão entre o número de AAs diferentes que o professor viu o relatório dentre as que ele é corretor/dono número.')
        st.progress(avaliacao_somativa_namespace_select[coluna][0])
        st.write('Pontuação **Média Eduqo: '+str(round(100*avaliacao_somativa_namespace5[coluna].mean(), 2))+'**')

