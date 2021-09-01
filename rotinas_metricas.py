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

# Importações de CSVs
avaliacao_somativa_namespace = pd.read_csv('./CSV/Avaliação Somativa/avaliacao_somativa.csv')
avaliacao_somativa_namespace2 = avaliacao_somativa_namespace[avaliacao_somativa_namespace['Média'] > 0]

## Título do relatório
st.image('[LOGO] Eduqo.png')

st.title('Relatório de Acompanhamento de Escolas/Redes')

image = Image.open('[LOGO] Eduqo.png')
st.sidebar.image(image,caption='Eduqo - Plataforma QMágico',use_column_width=True)

st.sidebar.markdown('Feito por : Alexandre Fernandes (Padre)')

## Introdução
st.subheader('Os dados analisados são do período entre 01/06/2021 e 29/08/2021')

## Resultados gerais

# Quartis Avaliação Somativa
quartil = (avaliacao_somativa_namespace2['Média'].max() - avaliacao_somativa_namespace2['Média'].min())/4
maximo = avaliacao_somativa_namespace2['Média'].max()
minimo = avaliacao_somativa_namespace2['Média'].min()
avaliacao_somativa_namespace4 = avaliacao_somativa_namespace2.copy()
avaliacao_somativa_namespace4['Quartil'] = '0º'
for i in range(len(avaliacao_somativa_namespace2['Média'])):
    if (avaliacao_somativa_namespace2['Média'][i] >= minimo and avaliacao_somativa_namespace2['Média'][i] < quartil + minimo):
        avaliacao_somativa_namespace4['Quartil'][i] = '4º'    
    if (avaliacao_somativa_namespace2['Média'][i] >= minimo + quartil and avaliacao_somativa_namespace2['Média'][i] < 2*quartil + minimo):
        avaliacao_somativa_namespace4['Quartil'][i] = '3º'  
    if (avaliacao_somativa_namespace2['Média'][i] >= minimo + 2*quartil and avaliacao_somativa_namespace2['Média'][i] < 3*quartil + minimo):
        avaliacao_somativa_namespace4['Quartil'][i] = '2º'  
    if (avaliacao_somativa_namespace2['Média'][i] >= minimo + 3*quartil and avaliacao_somativa_namespace2['Média'][i] <= 4*quartil + minimo):
        avaliacao_somativa_namespace4['Quartil'][i] = '1º'  


## Seleção do namespace a ser analisado
namespace_select = st.sidebar.selectbox('Selecione um namespace', avaliacao_somativa_namespace2['namespace'])

st.subheader('Namespace selecionado: **'+namespace_select+'**')

### Rotinas
st.header('Rotinas Pedagógicas Digitais')
st.image('Rotinas Pedagógicas Digitais.png', use_column_width=True, caption='Rotinas Pedagógicas Digitais')

## Rotina de Avaliação Somativa

## Leitura do csv com as métricas de Avaliação Somativa
#avaliacao_somativa_namespace = pd.read_csv('../CSV/Avaliação Somativa/avaliacao_somativa.csv')
avaliacao_somativa_namespace5 = avaliacao_somativa_namespace4.drop(columns = 'Unnamed: 0')
avaliacao_somativa_namespace5.rename(columns = {"('Criação de AA', '')":'Criação de AA'}, inplace = True)

avaliacao_somativa_namespace_select = avaliacao_somativa_namespace5[avaliacao_somativa_namespace5['namespace'] == namespace_select].reset_index(drop = True)
# Média do namespace
st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: #4A8AE8;
        }
        </style>""",
        unsafe_allow_html=True,
    )

st.subheader('**Avaliação Somativa'+' (Pontuação: '+str(round(100*avaliacao_somativa_namespace_select['Média'][0], 2))+')**')
st.markdown('***O namespace '+namespace_select+ ' está no '+avaliacao_somativa_namespace_select['Quartil'][0]+ ' quartil!***') 
st.progress(avaliacao_somativa_namespace_select['Média'][0])

ver_destaque_avaliacao_somativa = st.radio('Você deseja visualizar os namespaces destaque em Avaliação Somativa? 📈',('Não','Sim'))

avaliacao_somativa_namespace6 = avaliacao_somativa_namespace5.copy()
avaliacao_somativa_namespace6['Média'] = round(100*avaliacao_somativa_namespace6['Média'],2)
avaliacao_somativa_namespace6.rename(columns = {'Média':'Média (0 a 100)'}, inplace = True)
avaliacao_somativa_namespace7 = avaliacao_somativa_namespace6.drop(columns = ['Porcentagem de engajamento em AAs','Média de AAs por turma','Média de exercícios por turma','Correção de exercícios discursivos','Criação de AA','Publicação da AA','Acesso à relatórios de AA por aluno','Porcentagem de visualização de relatórios de AA por professor','Porcentagem de administradores que visualizaram relatórios de AA'])
    
if ver_destaque_avaliacao_somativa == 'Sim':
    avaliacao_somativa_namespace8 = avaliacao_somativa_namespace7.drop(columns = ['Quartil'])
    avaliacao_somativa_namespace9 = avaliacao_somativa_namespace8.loc[0:19]
    avaliacao_somativa_namespace9['Medalha'] = ''
    for i in range(20):
        if i == 0:
            avaliacao_somativa_namespace9['Medalha'][i] = '🥇'
        if i == 1:
            avaliacao_somativa_namespace9['Medalha'][i] = '🥈'
        if i == 2:
            avaliacao_somativa_namespace9['Medalha'][i] = '🥉'
        if i > 2:
            avaliacao_somativa_namespace9['Medalha'][i] = '  '   
    avaliacao_somativa_namespace9.set_index('Medalha', inplace=True)
    avaliacao_somativa_namespace10 = avaliacao_somativa_namespace9.style.format({"Média (0 a 100)":"{:,.2f}"})
    st.table(avaliacao_somativa_namespace10)


ver_quartil_avaliacao_somativa = st.radio('Escolha o quartil que deseja ver os resultados 📈',('Nenhum','1º','2º','3º','4º'))
if ver_quartil_avaliacao_somativa == '1º':
    avaliacao_somativa_namespace_quartil1 = avaliacao_somativa_namespace7[avaliacao_somativa_namespace7['Quartil'] == '1º']
    avaliacao_somativa_namespace_quartil1.set_index('Quartil', inplace=True)
    st.table(avaliacao_somativa_namespace_quartil1)
if ver_quartil_avaliacao_somativa == '2º':
    avaliacao_somativa_namespace_quartil2 = avaliacao_somativa_namespace7[avaliacao_somativa_namespace7['Quartil'] == '2º']
    avaliacao_somativa_namespace_quartil2.set_index('Quartil', inplace=True)
    st.table(avaliacao_somativa_namespace_quartil2)
if ver_quartil_avaliacao_somativa == '3º':
    avaliacao_somativa_namespace_quartil3 = avaliacao_somativa_namespace7[avaliacao_somativa_namespace7['Quartil'] == '3º']
    avaliacao_somativa_namespace_quartil3.set_index('Quartil', inplace=True)
    st.table(avaliacao_somativa_namespace_quartil3)
if ver_quartil_avaliacao_somativa == '4º':
    avaliacao_somativa_namespace_quartil4 = avaliacao_somativa_namespace7[avaliacao_somativa_namespace7['Quartil'] == '4º']    
    avaliacao_somativa_namespace_quartil4.set_index('Quartil', inplace=True)
    st.table(avaliacao_somativa_namespace_quartil4)
    

check_box_avaliacao_somativa = st.checkbox('Selecione para visualizar os resultados de Avaliação Somativa do namespace por métrica.')
var = []
if check_box_avaliacao_somativa == True:
    for coluna in avaliacao_somativa_namespace_select.loc[:,'Porcentagem de engajamento em AAs':'Porcentagem de administradores que visualizaram relatórios de AA']:
        st.markdown('**'+coluna+' (Pontuação: '+str(round(100*avaliacao_somativa_namespace_select[coluna][0], 2))+')**') 
        if coluna == 'Porcentagem de engajamento em AAs':
            #engajamento_aluno_aa = pd.read_csv('../CSV/Avaliação Somativa/engajamento_aluno_aa.csv')
            #engajamento_aluno_aa2 = engajamento_aluno_aa[engajamento_aluno_aa['namespace'] == namespace_select].reset_index()
            #st.write('Engajamento: '+ str(round(100*avaliacao_somativa_namespace_select[coluna][0], 2))+ '%')
            st.write('Essa métrica consiste na razão entre o número de exercícios realizados em relação aos disponibilizados (média entre os alunos)')
        #if coluna == 'Média de AAs por turma':
            #media_ex_aa_turma = pd.read_csv('../CSV/Avaliação Somativa/media_ex_aa_turma.csv')
            #media_ex_aa_turma['Média de AAs por turma'] = (media_ex_aa_turma['Média de AAs por turma'] - media_ex_aa_turma['Média de AAs por turma'].min())/(media_ex_aa_turma['Média de AAs por turma'].max() - media_ex_aa_turma['Média de AAs por turma'].min())
            #media_ex_aa_turma['Média de exercícios por turma'] = (media_ex_aa_turma['Média de exercícios por turma'] - media_ex_aa_turma['Média de exercícios por turma'].min())/(media_ex_aa_turma['Média de exercícios por turma'].max() - media_ex_aa_turma['Média de exercícios por turma'].min())
            #media_ex_aa_turma2 = media_ex_aa_turma[media_ex_aa_turma['namespace'] == namespace_select].reset_index()
            #media_ex_aa_turma3 = media_ex_aa_turma2.groupby('namespace').mean().reset_index()
            #st.dataframe(media_ex_aa_turma3)
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

########################################################################################################

## Rotina de Avaliação Diagnóstica