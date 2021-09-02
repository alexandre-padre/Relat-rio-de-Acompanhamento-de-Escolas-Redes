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









## Rotina de Avaliação Diagnóstica

avaliacao_diagnostica_namespace = pd.read_csv('./CSV/Avaliação Diagnóstica/avaliacao_diagnostica.csv')

# Quartis Avaliação Diagnóstica
avaliacao_diagnostica_namespace_aux = quartis(avaliacao_diagnostica_namespace,'Média')

avaliacao_diagnostica_namespace2 = avaliacao_diagnostica_namespace_aux.drop(columns = 'Unnamed: 0')

avaliacao_diagnostica_namespace_select = avaliacao_diagnostica_namespace2[avaliacao_diagnostica_namespace2['namespace'] == namespace_select].reset_index(drop = True)

# Média do namespace
st.subheader('**Avaliação Diagnóstica'+' (Pontuação: '+str(round(100*avaliacao_diagnostica_namespace_select['Média'][0], 2))+')**')
st.markdown('***O namespace '+namespace_select+ ' está no '+avaliacao_diagnostica_namespace_select['Quartil'][0]+ ' quartil!***') 
st.progress(avaliacao_diagnostica_namespace_select['Média'][0])

ver_destaque_avaliacao_diagnostica = st.radio('Você deseja visualizar os namespaces destaque em Avaliação Diagnóstica? 📈',('Não','Sim'))

# Ajustes na tabela de Avaliação Diagnóstica
avaliacao_diagnostica_namespace3 = avaliacao_diagnostica_namespace2.copy()
avaliacao_diagnostica_namespace3['Média'] = round(100*avaliacao_diagnostica_namespace3['Média'],2)
avaliacao_diagnostica_namespace3.rename(columns = {'Média':'Média (0 a 100)'}, inplace = True)
#avaliacao_somativa_namespace7 = avaliacao_somativa_namespace6.drop(columns = ['Porcentagem de engajamento em AAs','Média de AAs por turma','Média de exercícios por turma','Correção de exercícios discursivos','Criação de AA','Publicação da AA','Acesso à relatórios de AA por aluno','Porcentagem de visualização de relatórios de AA por professor','Porcentagem de administradores que visualizaram relatórios de AA'])

# Visualização dos namespaces destaque
if ver_destaque_avaliacao_diagnostica == 'Sim':
    avaliacao_diagnostica_namespace4 = destaques_rotina(avaliacao_diagnostica_namespace3)
    st.table(avaliacao_diagnostica_namespace4)

# Visualização dos quartis
ver_quartil_avaliacao_diagnostica = st.radio('Escolha o quartil que deseja ver os resultados de Avaliação Diagnóstica 📈',('Nenhum','1º','2º','3º','4º'))
if ver_quartil_avaliacao_diagnostica != 'Nenhum':
    avaliacao_diagnostica_namespace_quartil = visualizacao_resultado_quartil(ver_quartil_avaliacao_diagnostica,avaliacao_diagnostica_namespace3)
    st.table(avaliacao_diagnostica_namespace_quartil)

# Visualização das métricas do namespace selecionado
check_box_avaliacao_diagnostica = st.checkbox('Selecione para visualizar os resultados de Avaliação Diagnóstica do namespace por métrica.')
var = []
if check_box_avaliacao_diagnostica == True:
    for coluna in avaliacao_diagnostica_namespace_select.loc[:,'Nº de AAs copiadas da estante mágica e aplicada':'Média de exercícios em relatórios de AD por turma']:
        st.markdown('**'+coluna+' (Pontuação: '+str(round(100*avaliacao_diagnostica_namespace_select[coluna][0], 2))+')**') 
        st.progress(avaliacao_diagnostica_namespace_select[coluna][0])

########################################################################################################

## Rotina de Avaliação Somativa

# Quartis Avaliação Somativa
avaliacao_somativa_namespace4 = quartis(avaliacao_somativa_namespace2,'Média')

avaliacao_somativa_namespace5 = avaliacao_somativa_namespace4.drop(columns = 'Unnamed: 0')
avaliacao_somativa_namespace5.rename(columns = {"('Criação de AA', '')":'Criação de AA'}, inplace = True)

avaliacao_somativa_namespace_select = avaliacao_somativa_namespace5[avaliacao_somativa_namespace5['namespace'] == namespace_select].reset_index(drop = True)

st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: #4A8AE8;
        }
        </style>""",
        unsafe_allow_html=True,
    )

# Média do namespace
st.subheader('**Avaliação Somativa'+' (Pontuação: '+str(round(100*avaliacao_somativa_namespace_select['Média'][0], 2))+')**')
st.markdown('***O namespace '+namespace_select+ ' está no '+avaliacao_somativa_namespace_select['Quartil'][0]+ ' quartil!***') 
st.progress(avaliacao_somativa_namespace_select['Média'][0])

ver_destaque_avaliacao_somativa = st.radio('Você deseja visualizar os namespaces destaque em Avaliação Somativa? 📈',('Não','Sim'))

# Ajustes na tabela de Avaliação Somativa
avaliacao_somativa_namespace6 = avaliacao_somativa_namespace5.copy()
avaliacao_somativa_namespace6['Média'] = round(100*avaliacao_somativa_namespace6['Média'],2)
avaliacao_somativa_namespace6.rename(columns = {'Média':'Média (0 a 100)'}, inplace = True)
avaliacao_somativa_namespace7 = avaliacao_somativa_namespace6.drop(columns = ['Porcentagem de engajamento em AAs','Média de AAs por turma','Média de exercícios por turma','Correção de exercícios discursivos','Criação de AA','Publicação da AA','Acesso à relatórios de AA por aluno','Porcentagem de visualização de relatórios de AA por professor','Porcentagem de administradores que visualizaram relatórios de AA'])


# Visualização dos namespaces destaque
if ver_destaque_avaliacao_somativa == 'Sim':
    avaliacao_somativa_namespace9 = destaques_rotina(avaliacao_somativa_namespace7)
    st.table(avaliacao_somativa_namespace9)

# Visualização dos quartis
ver_quartil_avaliacao_somativa = st.radio('Escolha o quartil que deseja ver os resultados de Avaliação Somativa 📈',('Nenhum','1º','2º','3º','4º'))
if ver_quartil_avaliacao_somativa != 'Nenhum':
    avaliacao_somativa_namespace_quartil = visualizacao_resultado_quartil(ver_quartil_avaliacao_somativa,avaliacao_somativa_namespace7)
    st.table(avaliacao_somativa_namespace_quartil)

# Visualização das métricas do namespace selecionado
check_box_avaliacao_somativa = st.checkbox('Selecione para visualizar os resultados de Avaliação Somativa do namespace por métrica.')
var = []
if check_box_avaliacao_somativa == True:
    for coluna in avaliacao_somativa_namespace_select.loc[:,'Porcentagem de engajamento em AAs':'Porcentagem de administradores que visualizaram relatórios de AA']:
        st.markdown('**'+coluna+' (Pontuação: '+str(round(100*avaliacao_somativa_namespace_select[coluna][0], 2))+')**') 
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

