# imports e definições
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime
import streamlit as st
import math
from PIL import Image
import plotly.express as px
from funcoes import *
from git import Repo
import datetime as dt
import random

######################## Configuração da página ########################

st.set_page_config(
    page_title="Relatório de Acompanhamento de Escolas/Redes", layout="centered", page_icon="[LOGO] Eduqo 4.png"
)

######################### Banco de Dados ########################
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Banco de Dados').sheet1          # Enquanto estiver rodando na nuvem
#sheet = client.open('Banco de Dados - Teste').sheet1   # Enquanto estiver rodando no local

#### Colunas (id, Data e Hora, Nome, Rede, Grupo, Gestor, Produto, Faixa de licenças, Namespace, NPS, Feedback)
row0 = ['Data e Hora', 'Nome', 'Rede', 'Grupo', 'Gestor', 'Produto', 'Faixa de licenças', 'Namespace', 'NPS', 'Feedback']

banco_de_dados = sheet.get_all_records()
banco_de_dados2 = pd.DataFrame(banco_de_dados)
#st.dataframe(banco_de_dados2)

######################### Namespaces a serem analisados ########################

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

######################## Senha ########################

senha = 'eduqo'
senha_preenchida = str(st.text_input("Digite a senha para conseguir acessar o relatório")).strip().lower()
"""
        #### Dica: Nome da Edtech mais cabulosa do Brasil!
        ##
"""
nomes_eduqo = pd.read_csv('./CSV/nomes_eduqo.csv')
nomes_eduqo = inserir_linha(pd.DataFrame(data = nomes_eduqo['Nomes'].unique()),pd.DataFrame({0: 'Nome'}, index=[-1]))
nome = str(st.selectbox('Digite o seu nome',nomes_eduqo[0]))
if senha_preenchida == 'eduqo' and nome != 'Nome':

    ######################## Preenchimento do histórico de acessos ao relatório ########################

    row = [str(datetime.today()),nome]
    index = 2
    sheet.insert_row(row, index)

    ######################## Junção namespaces e informações do Hubspot ########################

    namespaces_x_hubspot = pd.merge(namespaces, informacoes_hubspot, on = ['namespace','Produto'], how = 'left')
    namespaces_x_hubspot2 = namespaces_x_hubspot.drop(columns = ['Unnamed: 0_x','Unnamed: 0_y','Interações A.A','Interações Cadernos'])
    namespaces_x_hubspot3 = pd.merge(namespaces_x_hubspot2, namespace_rede, on = 'namespace', how = 'left')

    ######################## Menu do relatório ########################
    st.write('----')

    escolha_relatorio = st.radio('👉 Selecione o relatório que deseja acessar 📈',('Escolha abaixo:','Relatório QBR','Relatório QBR de Redes','Relatório de Rotinas pegagógicas (em construção)'))    

    if escolha_relatorio == 'Relatório QBR':
        
        ######################### Filtro de namespace ############################
        namespace_meio = namespaces_x_hubspot3.sort_values(by = 'namespace')
        namespace_meio2 = inserir_linha(pd.DataFrame(data = namespace_meio['namespace'].unique()),pd.DataFrame({0: 'Namespace'}, index=[-1]))
        namespace_meio_select = st.selectbox('👉 Selecione um namespace ', namespace_meio2)

        ######################### Acesso a plataforma por alunos ############################
        alunos_acessaram_namespace = pd.read_csv('./CSV/QBR/Resultados por namespace/alunos_acessaram_namespace.csv')
        alunos_acessaram_namespace_select = alunos_acessaram_namespace[alunos_acessaram_namespace['namespace'] == namespace_meio_select]
        alunos_acessaram_anoescolar = pd.read_csv('./CSV/QBR/Resultados por ano escolar/alunos_acessaram_anoescolar.csv')
        alunos_acessaram_anoescolar_select = alunos_acessaram_anoescolar[alunos_acessaram_anoescolar['namespace'] == namespace_meio_select]

        ######################### Data de análise ############################
        dias = []
        for i in range(len(alunos_acessaram_namespace['day'].unique())+1):
            dias.append(datetime.strptime(alunos_acessaram_namespace['day'][i], '%Y-%m-%d').date())
        periodo_data = st.slider('👉 Data de análise',min(dias),max(dias),[min(dias),max(dias)],timedelta(1))

        ######################### Filtro acesso da plataforma (namespace) - Data de análise ############################
        alunos_acessaram_namespace_select['day'] = pd.to_datetime(alunos_acessaram_namespace_select['day'])
        periodo_data = pd.to_datetime(periodo_data)
        alunos_acessaram_namespace_select_tempo = alunos_acessaram_namespace_select[alunos_acessaram_namespace_select['day'] >= periodo_data[0]]
        alunos_acessaram_namespace_select_tempo2 = alunos_acessaram_namespace_select_tempo[alunos_acessaram_namespace_select_tempo['day'] <= periodo_data[1]]

        ######################### Filtro acesso da plataforma (ano escolar) - Data de análise ############################
        alunos_acessaram_anoescolar_select['day'] = pd.to_datetime(alunos_acessaram_anoescolar_select['day'])
        alunos_acessaram_anoescolar_select_tempo = alunos_acessaram_anoescolar_select[alunos_acessaram_anoescolar_select['day'] >= periodo_data[0]]
        alunos_acessaram_anoescolar_select_tempo2 = alunos_acessaram_anoescolar_select_tempo[alunos_acessaram_anoescolar_select_tempo['day'] <= periodo_data[1]]

        ######################### Filtro de ano escolar ############################   
        ano_escolar = inserir_linha(pd.DataFrame(data = alunos_acessaram_anoescolar_select['grade'].unique()),pd.DataFrame({0: 'Ano Escolar'}, index=[-1]))
        anoescolar_select = st.multiselect('👉 Selecione um ano escolar', ano_escolar)

        ######################### Exercícios realizados em AAs ############################
        exercicios_realizados_namespace = pd.read_csv('./CSV/QBR/Resultados por namespace/exercicios_realizados_namespace.csv')
        exercicios_realizados_namespace_select = exercicios_realizados_namespace[exercicios_realizados_namespace['namespace'] == namespace_meio_select]
        exercicios_realizados_namespace_select['creation'] = pd.to_datetime(exercicios_realizados_namespace_select['creation'])
        exercicios_realizados_namespace_select_tempo = exercicios_realizados_namespace_select[exercicios_realizados_namespace_select['creation'] >= periodo_data[0]]
        exercicios_realizados_namespace_select_tempo2 = exercicios_realizados_namespace_select_tempo[exercicios_realizados_namespace_select_tempo['creation'] <= periodo_data[1]]

        exercicios_realizados_anoescolar = pd.read_csv('./CSV/QBR/Resultados por ano escolar/exercicios_realizados_anoescolar.csv')
        exercicios_realizados_anoescolar_select = exercicios_realizados_anoescolar[exercicios_realizados_anoescolar['namespace'] == namespace_meio_select]
        exercicios_realizados_anoescolar_select['creation'] = pd.to_datetime(exercicios_realizados_anoescolar_select['creation'])
        exercicios_realizados_anoescolar_select_tempo = exercicios_realizados_anoescolar_select[exercicios_realizados_anoescolar_select['creation'] >= periodo_data[0]]
        exercicios_realizados_anoescolar_select_tempo2 = exercicios_realizados_anoescolar_select_tempo[exercicios_realizados_anoescolar_select_tempo['creation'] <= periodo_data[1]]

        ######################### Exercícios realizados em SEs ############################
        exercicios_realizados_se_namespace = pd.read_csv('./CSV/QBR/Resultados por namespace/exercicios_realizados_se_namespace.csv')
        exercicios_realizados_se_namespace_select = exercicios_realizados_se_namespace[exercicios_realizados_se_namespace['namespace'] == namespace_meio_select]
        exercicios_realizados_se_namespace_select['day'] = pd.to_datetime(exercicios_realizados_se_namespace_select['day'])
        exercicios_realizados_se_namespace_select_tempo = exercicios_realizados_se_namespace_select[exercicios_realizados_se_namespace_select['day'] >= periodo_data[0]]
        exercicios_realizados_se_namespace_select_tempo2 = exercicios_realizados_se_namespace_select_tempo[exercicios_realizados_se_namespace_select_tempo['day'] <= periodo_data[1]]
        #st.dataframe(exercicios_realizados_se_namespace_select_tempo2)

        exercicios_realizados_se_anoescolar = pd.read_csv('./CSV/QBR/Resultados por ano escolar/exercicios_realizados_se_anoescolar.csv')
        exercicios_realizados_se_anoescolar_select = exercicios_realizados_se_anoescolar[exercicios_realizados_se_anoescolar['namespace'] == namespace_meio_select]
        exercicios_realizados_se_anoescolar_select['day'] = pd.to_datetime(exercicios_realizados_se_anoescolar_select['day'])
        exercicios_realizados_se_anoescolar_select_tempo = exercicios_realizados_se_anoescolar_select[exercicios_realizados_se_anoescolar_select['day'] >= periodo_data[0]]
        exercicios_realizados_se_anoescolar_select_tempo2 = exercicios_realizados_se_anoescolar_select_tempo[exercicios_realizados_se_anoescolar_select_tempo['day'] <= periodo_data[1]]

        ######################### Conteúdos estudados ############################
        conteudos_estudados_namespace = pd.read_csv('./CSV/QBR/Resultados por namespace/conteudos_estudados_namespace.csv')
        conteudos_estudados_namespace_select = conteudos_estudados_namespace[conteudos_estudados_namespace['namespace'] == namespace_meio_select]
        conteudos_estudados_namespace_select['day'] = pd.to_datetime(conteudos_estudados_namespace_select['day'])
        conteudos_estudados_namespace_select_tempo = conteudos_estudados_namespace_select[conteudos_estudados_namespace_select['day'] >= periodo_data[0]]
        conteudos_estudados_namespace_select_tempo2 = conteudos_estudados_namespace_select_tempo[conteudos_estudados_namespace_select_tempo['day'] <= periodo_data[1]]

        conteudos_estudados_anoescolar = pd.read_csv('./CSV/QBR/Resultados por ano escolar/conteudos_estudados_anoescolar.csv')
        conteudos_estudados_anoescolar_select = conteudos_estudados_anoescolar[conteudos_estudados_anoescolar['namespace'] == namespace_meio_select]
        conteudos_estudados_anoescolar_select['day'] = pd.to_datetime(conteudos_estudados_anoescolar_select['day'])
        conteudos_estudados_anoescolar_select_tempo = conteudos_estudados_anoescolar_select[conteudos_estudados_anoescolar_select['day'] >= periodo_data[0]]
        conteudos_estudados_anoescolar_select_tempo2 = conteudos_estudados_anoescolar_select_tempo[conteudos_estudados_anoescolar_select_tempo['day'] <= periodo_data[1]]

        ######################### Acesso a plataforma por professores ############################
        profs_acessaram = pd.read_csv('./CSV/QBR/Resultados por namespace/profs_acessaram.csv')
        profs_acessaram_select = profs_acessaram[profs_acessaram['namespace'] == namespace_meio_select]
        profs_acessaram_select['day'] = pd.to_datetime(profs_acessaram_select['day'])
        profs_acessaram_select_tempo = profs_acessaram_select[profs_acessaram_select['day'] >= periodo_data[0]]
        profs_acessaram_select_tempo2 = profs_acessaram_select_tempo[profs_acessaram_select_tempo['day'] <= periodo_data[1]]

        ######################### Professores materiais ############################
        profs_materiais = pd.read_csv('./CSV/QBR/Resultados por namespace/profs_materiais.csv')
        profs_materiais_select = profs_materiais[profs_materiais['namespace'] == namespace_meio_select]
        profs_materiais_select['created'] = pd.to_datetime(profs_materiais_select['created'])
        profs_materiais_select_tempo = profs_materiais_select[profs_materiais_select['created'] >= periodo_data[0]]
        profs_materiais_select_tempo2 = profs_materiais_select_tempo[profs_materiais_select_tempo['created'] <= periodo_data[1]]

        ######################### Professores exercícios ############################
        profs_exercicios = pd.read_csv('./CSV/QBR/Resultados por namespace/profs_exercicios.csv')
        profs_exercicios_select = profs_exercicios[profs_exercicios['namespace'] == namespace_meio_select]
        profs_exercicios_select['created'] = pd.to_datetime(profs_exercicios_select['created'])
        profs_exercicios_select_tempo = profs_exercicios_select[profs_exercicios_select['created'] >= periodo_data[0]]
        profs_exercicios_select_tempo2 = profs_exercicios_select_tempo[profs_exercicios_select_tempo['created'] <= periodo_data[1]]

        ######################### Professores visualização de relatórios ############################
        profs_relatorios = pd.read_csv('./CSV/QBR/Resultados por namespace/profs_relatorios.csv')
        profs_relatorios_select = profs_relatorios[profs_relatorios['namespace'] == namespace_meio_select]
        profs_relatorios_select['creation'] = pd.to_datetime(profs_relatorios_select['creation'])
        profs_relatorios_select_tempo = profs_relatorios_select[profs_relatorios_select['creation'] >= periodo_data[0]]
        profs_relatorios_select_tempo2 = profs_relatorios_select_tempo[profs_relatorios_select_tempo['creation'] <= periodo_data[1]]

        st.write('----')

        if namespace_meio_select != 'Namespace':
            """
                ### **Benefício 1**: Alunos engajados, no seu próprio ritmo e recebendo feedback em tempo real.
                ## 🚀 **Acesso à plataforma por alunos**
                Aqui analisamos a quantidade de acessos à plataforma, cada número representa a média semanal da quantidade de alunos que acessaram diariamente em relação ao número de alunos ativos.
            """
            alunos_acessaram_namespace_select_tempo2 = alunos_acessaram_namespace_select_tempo2.reset_index(drop = True)
            alunos_acessaram_namespace_select_tempo2['Semana'] = 0
            for i in range(len(alunos_acessaram_namespace_select_tempo2['day'])):
                aux2 = alunos_acessaram_namespace_select_tempo2['day'][i].strftime('%Y-%m-%d')
                aux = aux2.split('-')
                for j in range(len(aux)):
                    aux[j] = int(aux[j])
                alunos_acessaram_namespace_select_tempo2['Semana'][i] = dt.date(aux[0],aux[1],aux[2]).isocalendar()[1]
            alunos_acessaram_namespace_select_tempo3 = alunos_acessaram_namespace_select_tempo2.groupby(['namespace','Semana']).mean().reset_index()   
            
            fig = px.bar(alunos_acessaram_namespace_select_tempo3, x = alunos_acessaram_namespace_select_tempo3['Semana'], y = 100*alunos_acessaram_namespace_select_tempo3['Engajamento de alunos ativos'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(alunos_acessaram_namespace_select_tempo3))
            
            if len(anoescolar_select) != 0:
                alunos_acessaram_anoescolar_select_tempo2 = alunos_acessaram_anoescolar_select_tempo2.reset_index(drop = True)
                alunos_acessaram_anoescolar_select_tempo2['Semana'] = 0
                for i in range(len(alunos_acessaram_anoescolar_select_tempo2['day'])):
                    aux2 = alunos_acessaram_anoescolar_select_tempo2['day'][i].strftime('%Y-%m-%d')
                    aux = aux2.split('-')
                    for j in range(len(aux)):
                        aux[j] = int(aux[j])
                    alunos_acessaram_anoescolar_select_tempo2['Semana'][i] = dt.date(aux[0],aux[1],aux[2]).isocalendar()[1]
                alunos_acessaram_anoescolar_select_tempo3 = alunos_acessaram_anoescolar_select_tempo2.groupby(['namespace','Semana','grade']).mean().reset_index() 
                cor = []
                for i in range(len(anoescolar_select)):
                    alunos_acessaram_anoescolar_select_tempo4 = alunos_acessaram_anoescolar_select_tempo3.loc[alunos_acessaram_anoescolar_select_tempo3['grade'] == anoescolar_select[i]]
                    cor.append("#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
                    fig.add_scatter(x = alunos_acessaram_anoescolar_select_tempo4['Semana'], y = 100*alunos_acessaram_anoescolar_select_tempo4['Engajamento de alunos ativos'],mode='lines', name = anoescolar_select[i], line=dict(color=cor[i]))
            fig.update_layout(title = "Engajamento de alunos ativos")
            st.plotly_chart(fig)

            alunos_ativos = pd.read_csv('./CSV/QBR/Resultados Query/alunos_ativos.csv')
            alunos_ativos2 = alunos_ativos[alunos_ativos['namespace'] == namespace_meio_select]
            alunos_ativos3 = alunos_ativos2.groupby('namespace').sum()

            adm_doc_ativos = pd.read_csv('./CSV/QBR/Resultados Query/adm_doc_ativos.csv')
            adm_ativo = adm_doc_ativos[adm_doc_ativos['role'] == 'ADMIN']
            adm_ativo2 = adm_ativo[adm_ativo['namespace'] == namespace_meio_select].reset_index(drop = True)
            doc_ativo = adm_doc_ativos[adm_doc_ativos['role'] == 'TEACHER']
            doc_ativo2 = doc_ativo[doc_ativo['namespace'] == namespace_meio_select].reset_index(drop = True)
            porc_aluno_ativo = alunos_ativos3['count'][0]/(alunos_ativos3['count'][0]+adm_ativo2['count'][0]+doc_ativo2['count'][0])
            porc_doc_ativo = doc_ativo2['count'][0]/(alunos_ativos3['count'][0]+adm_ativo2['count'][0]+doc_ativo2['count'][0])
            porc_adm_ativo = adm_ativo2['count'][0]/(alunos_ativos3['count'][0]+adm_ativo2['count'][0]+doc_ativo2['count'][0])
            porc_adm_ativo2 = round(100*truncar(porc_adm_ativo,3),3)
            porc_aluno_ativo2 = round(100*truncar(porc_aluno_ativo,3),3) 
            porc_doc_ativo2 = round(100*truncar(porc_doc_ativo,3),3)    

            st.write('O total de administrantes é **'+str(adm_ativo2['count'][0])+' ('+str(porc_adm_ativo2)+'%)**, de professores é **'+str(doc_ativo2['count'][0])+' ('+str(porc_doc_ativo2)+'%)** e a quantidade de alunos é **'+str(alunos_ativos3['count'][0])+' ('+str(porc_aluno_ativo2)+'%)**.')    


            """
                ## 🚀 **Exercícios resolvidos (Atividades Avaliativas)**
                Aqui analisamos a quantidade de exercícios resolvidos pelos alunos em atividades avaliativas, por aluno ativo, ou seja, é a média de exercícios de AA resolvidos por aluno em cada semana.
            """
            ######################### Exercícios realizados em AAs ############################
            exercicios_realizados_namespace_select_tempo2 = exercicios_realizados_namespace_select_tempo2.reset_index(drop = True)
            exercicios_realizados_namespace_select_tempo2['Exercícios resolvidos por aluno'] = exercicios_realizados_namespace_select_tempo2['exercicios_realizados']/exercicios_realizados_namespace_select_tempo2['count']
            exercicios_realizados_namespace_select_tempo2 = exercicios_realizados_namespace_select_tempo2.drop(columns = ['exercicios_realizados','count','Unnamed: 0'])
            exercicios_realizados_namespace_select_tempo3 = exercicios_realizados_namespace_select_tempo2.groupby(['namespace','Semana']).sum().reset_index()   
            fig = px.bar(exercicios_realizados_namespace_select_tempo3, x = exercicios_realizados_namespace_select_tempo3['Semana'], y = exercicios_realizados_namespace_select_tempo3['Exercícios resolvidos por aluno'], color_discrete_sequence = ['#4a8ae8']*len(exercicios_realizados_namespace_select_tempo3))
            

            if len(anoescolar_select) != 0:
                exercicios_realizados_anoescolar_select_tempo2 = exercicios_realizados_anoescolar_select_tempo2.reset_index(drop = True)
                exercicios_realizados_anoescolar_select_tempo2['Exercícios resolvidos por aluno'] = exercicios_realizados_anoescolar_select_tempo2['exercicios_realizados']/exercicios_realizados_anoescolar_select_tempo2['count']
                exercicios_realizados_anoescolar_select_tempo2 = exercicios_realizados_anoescolar_select_tempo2.drop(columns = ['exercicios_realizados','count','Unnamed: 0'])
                exercicios_realizados_anoescolar_select_tempo3 = exercicios_realizados_anoescolar_select_tempo2.groupby(['namespace','Semana','grade']).sum().reset_index()
                for i in range(len(anoescolar_select)):
                    exercicios_realizados_anoescolar_select_tempo4 = exercicios_realizados_anoescolar_select_tempo3.loc[exercicios_realizados_anoescolar_select_tempo3['grade'] == anoescolar_select[i]]
                    fig.add_scatter(x = exercicios_realizados_anoescolar_select_tempo4['Semana'], y = exercicios_realizados_anoescolar_select_tempo4['Exercícios resolvidos por aluno'],mode='lines', name = anoescolar_select[i], line=dict(color=cor[i]))
            fig.update_layout(title = "Exercícios resolvidos de AA por aluno")
            st.plotly_chart(fig)
            
            st.write('A média de exercícios resolvidos em todas as semanas é **'+str(round(truncar(exercicios_realizados_namespace_select_tempo3['Exercícios resolvidos por aluno'].mean(),3),3))+'** exercícios por aluno.')

            """
                ## 🚀 **Exercícios resolvidos (Séries de exercícios)**
                Aqui analisamos a quantidade de exercícios resolvidos pelos alunos em séries de exercícios, por aluno ativo, ou seja, é a média de exercícios de SE resolvidos por aluno em cada semana.
            """
            ######################### Exercícios realizados em SEs ############################
            exercicios_realizados_se_namespace_select_tempo2 = exercicios_realizados_se_namespace_select_tempo2.reset_index(drop = True)
            exercicios_realizados_se_namespace_select_tempo2['Exercícios resolvidos de SE por aluno'] = exercicios_realizados_se_namespace_select_tempo2['num_ex']/exercicios_realizados_se_namespace_select_tempo2['count']
            exercicios_realizados_se_namespace_select_tempo2 = exercicios_realizados_se_namespace_select_tempo2.drop(columns = ['num_ex','count','Unnamed: 0'])
            exercicios_realizados_se_namespace_select_tempo3 = exercicios_realizados_se_namespace_select_tempo2.groupby(['namespace','Semana']).sum().reset_index()   
            fig = px.bar(exercicios_realizados_se_namespace_select_tempo3, x = exercicios_realizados_se_namespace_select_tempo3['Semana'], y = exercicios_realizados_se_namespace_select_tempo3['Exercícios resolvidos de SE por aluno'], color_discrete_sequence = ['#4a8ae8']*len(exercicios_realizados_se_namespace_select_tempo3))
            
            if len(anoescolar_select) != 0:
                exercicios_realizados_se_anoescolar_select_tempo2 = exercicios_realizados_se_anoescolar_select_tempo2.reset_index(drop = True)
                exercicios_realizados_se_anoescolar_select_tempo2['Exercícios resolvidos de SE por aluno'] = exercicios_realizados_se_anoescolar_select_tempo2['num_ex']/exercicios_realizados_se_anoescolar_select_tempo2['count']
                exercicios_realizados_se_anoescolar_select_tempo2 = exercicios_realizados_se_anoescolar_select_tempo2.drop(columns = ['num_ex','count','Unnamed: 0'])
                exercicios_realizados_se_anoescolar_select_tempo3 = exercicios_realizados_se_anoescolar_select_tempo2.groupby(['namespace','Semana','grade']).sum().reset_index()
                for i in range(len(anoescolar_select)):
                    exercicios_realizados_se_anoescolar_select_tempo4 = exercicios_realizados_se_anoescolar_select_tempo3.loc[exercicios_realizados_se_anoescolar_select_tempo3['grade'] == anoescolar_select[i]]
                    fig.add_scatter(x = exercicios_realizados_se_anoescolar_select_tempo4['Semana'], y = exercicios_realizados_se_anoescolar_select_tempo4['Exercícios resolvidos de SE por aluno'],mode='lines', name = anoescolar_select[i], line=dict(color=cor[i]))
            fig.update_layout(title = "Exercícios resolvidos de SE por aluno")
            st.plotly_chart(fig)

            st.write('A média de exercícios resolvidos em todas as semanas é **'+str(round(truncar(exercicios_realizados_se_namespace_select_tempo3['Exercícios resolvidos de SE por aluno'].mean(),3),3))+'** exercícios por aluno.')

            """
                ## 🚀 **Conteúdos estudados**
                Aqui analisamos a quantidade de conteúdos estudados, por aluno ativo, ou seja, é a média de conteúdos estudados por aluno em cada semana.
            """
            ######################### Conteúdos estudados ############################
            conteudos_estudados_namespace_select_tempo2 = conteudos_estudados_namespace_select_tempo2.reset_index(drop = True)
            conteudos_estudados_namespace_select_tempo2['Conteudos estudados por aluno'] = conteudos_estudados_namespace_select_tempo2['count_y']/conteudos_estudados_namespace_select_tempo2['count_x']
            conteudos_estudados_namespace_select_tempo2_aux = conteudos_estudados_namespace_select_tempo2.drop(columns = ['count_x','count_y'])
            conteudos_estudados_namespace_select_tempo3 = conteudos_estudados_namespace_select_tempo2_aux.groupby(['namespace','Semana']).sum().reset_index()   
            fig = px.bar(conteudos_estudados_namespace_select_tempo3, x = conteudos_estudados_namespace_select_tempo3['Semana'], y = conteudos_estudados_namespace_select_tempo3['Conteudos estudados por aluno'], color_discrete_sequence = ['#4a8ae8']*len(conteudos_estudados_namespace_select_tempo3))
            
            if len(anoescolar_select) != 0:
                conteudos_estudados_anoescolar_select_tempo2 = conteudos_estudados_anoescolar_select_tempo2.reset_index(drop = True)
                conteudos_estudados_anoescolar_select_tempo2['Conteudos estudados por aluno'] = conteudos_estudados_anoescolar_select_tempo2['count_y']/conteudos_estudados_anoescolar_select_tempo2['count_x']
                conteudos_estudados_anoescolar_select_tempo2_aux = conteudos_estudados_anoescolar_select_tempo2.drop(columns = ['count_x','count_y'])
                conteudos_estudados_anoescolar_select_tempo3 = conteudos_estudados_anoescolar_select_tempo2_aux.groupby(['namespace','Semana','grade']).sum().reset_index()
                for i in range(len(anoescolar_select)):
                    conteudos_estudados_anoescolar_select_tempo4 = conteudos_estudados_anoescolar_select_tempo3.loc[conteudos_estudados_anoescolar_select_tempo3['grade'] == anoescolar_select[i]]
                    fig.add_scatter(x = conteudos_estudados_anoescolar_select_tempo4['Semana'], y = conteudos_estudados_anoescolar_select_tempo4['Conteudos estudados por aluno'],mode='lines', name = anoescolar_select[i], line=dict(color=cor[i]))
            fig.update_layout(title = "Conteudos estudados por aluno")
            st.plotly_chart(fig)

            st.write('A média de conteúdos estudados em todas as semanas é **'+str(round(truncar(conteudos_estudados_namespace_select_tempo3['Conteudos estudados por aluno'].mean(),3),3))+'** conteúdos por aluno.')

            """
                ### **Benefício 2**: Professores que estão personalizando a aprendizagem.
                ## 🚀 **Acesso à plataforma por professores**
                Aqui analisamos a quantidade de acessos à plataforma, cada número representa a média semanal da quantidade de professores que acessaram diariamente em relação ao número de professores ativos.
            """
            ######################### Acesso de professores à plataforma ############################
            profs_acessaram_select_tempo2 = profs_acessaram_select_tempo2.reset_index(drop = True)
            profs_acessaram_select_tempo2['Engajamento de professores'] = profs_acessaram_select_tempo2['count_y']/profs_acessaram_select_tempo2['count_x']
            profs_acessaram_select_tempo2_aux = profs_acessaram_select_tempo2.drop(columns = ['count_x','count_y'])
            profs_acessaram_select_tempo3 = profs_acessaram_select_tempo2_aux.groupby(['namespace','Semana']).mean().reset_index()   
            fig = px.bar(profs_acessaram_select_tempo3, x = profs_acessaram_select_tempo3['Semana'], y = 100*profs_acessaram_select_tempo3['Engajamento de professores'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(profs_acessaram_select_tempo3))
            fig.update_layout(title = "Engajamento de professores")
            st.plotly_chart(fig)

            st.write('A média de acesso por professores por dia é **'+str(round(truncar(100*profs_acessaram_select_tempo3['Engajamento de professores'].mean(),3),3))+'%**.')

            """
                ## 🚀 **Materiais criados por professor**
                Aqui analisamos a quantidade de materiais criador por professor, cada número representa a média semanal da quantidade de materiais postados.
            """
            ######################### Materiais criados por professor ############################
            profs_materiais_select_tempo2 = profs_materiais_select_tempo2.reset_index(drop = True)
            profs_materiais_select_tempo2['Materiais por professor'] = profs_materiais_select_tempo2['count_y']/profs_materiais_select_tempo2['count_x']
            profs_materiais_select_tempo2_aux = profs_materiais_select_tempo2.drop(columns = ['count_x','count_y'])
            profs_materiais_select_tempo3 = profs_materiais_select_tempo2_aux.groupby(['namespace','Semana']).sum().reset_index()   
            fig = px.bar(profs_materiais_select_tempo3, x = profs_materiais_select_tempo3['Semana'], y = profs_materiais_select_tempo3['Materiais por professor'], color_discrete_sequence = ['#4a8ae8']*len(profs_materiais_select_tempo3))
            fig.update_layout(title = "Materiais criados por professor")
            st.plotly_chart(fig)

            st.write('A média de materiais postados por professor por semana é **'+str(round(truncar(profs_materiais_select_tempo3['Materiais por professor'].mean(),3),3))+'**.')

            """
                ## 🚀 **Exercícios criados por professor**
                Aqui analisamos a quantidade de exercícios criador por professor, cada número representa a média semanal da quantidade de exercícios postados.
            """
            ######################### Exercícios criador por professores ############################
            profs_exercicios_select_tempo2 = profs_exercicios_select_tempo2.reset_index(drop = True)
            profs_exercicios_select_tempo2['Exercícios por professor'] = profs_exercicios_select_tempo2['count_y']/profs_exercicios_select_tempo2['count_x']
            profs_exercicios_select_tempo2_aux = profs_exercicios_select_tempo2.drop(columns = ['count_x','count_y'])
            profs_exercicios_select_tempo3 = profs_exercicios_select_tempo2_aux.groupby(['namespace','Semana']).sum().reset_index()   
            fig = px.bar(profs_exercicios_select_tempo3, x = profs_exercicios_select_tempo3['Semana'], y = profs_exercicios_select_tempo3['Exercícios por professor'], color_discrete_sequence = ['#4a8ae8']*len(profs_exercicios_select_tempo3))
            fig.update_layout(title = "Exercícios criados por professor")
            st.plotly_chart(fig)

            st.write('A média de exercícios criados por professor por semana é **'+str(round(truncar(profs_exercicios_select_tempo3['Exercícios por professor'].mean(),3),3))+'**.')

            """
                ### **Benefício 3**: Escola que analisa dados para personalização da aprendizagem.
                ## 🚀 **Visualização de relatórios por professor**
                Aqui analisamos a visualização de relatórios por professor semanalmente, ou seja cada número representa a porcentagem de professores que visualizações relatórios em cada semana.
            """
            ######################### Visualização de relatórios por professores ############################
            profs_relatorios_select_tempo2 = profs_relatorios_select_tempo2.reset_index(drop = True)
            profs_relatorios_select_tempo3 = profs_relatorios_select_tempo2.groupby(['namespace','Semana']).nunique().reset_index()   
            profs_relatorios_select_tempo4 = profs_relatorios_select_tempo3.drop(columns = ['Unnamed: 0','creation','type'])
            profs_ativos2 = pd.read_csv('./CSV/QBR/Resultados Query/profs_ativos.csv', sep = ',')
            profs_ativos3 = profs_ativos2.drop(columns = ['Unnamed: 0'])
            profs_relatorios_select_tempo5 = pd.merge(profs_ativos3,profs_relatorios_select_tempo4, on = 'namespace', how = 'inner')
            profs_relatorios_select_tempo5['Engajamento na visualização de relatórios'] = profs_relatorios_select_tempo5['user_id']/profs_relatorios_select_tempo5['count']
            profs_relatorios_select_tempo6 = profs_relatorios_select_tempo5.drop(columns = ['user_id','count'])
            fig = px.bar(profs_relatorios_select_tempo6, x = profs_relatorios_select_tempo6['Semana'], y = 100*profs_relatorios_select_tempo6['Engajamento na visualização de relatórios'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(profs_relatorios_select_tempo6))
            fig.update_layout(title = "Porcentagem de professores que visualizam relatórios")
            st.plotly_chart(fig)

            st.write('A porcentagem de professores que visualizaram relatórios semanalmente é de **'+str(round(truncar(100*profs_relatorios_select_tempo6['Engajamento na visualização de relatórios'].mean(),3),3))+'%**.')

    if escolha_relatorio == 'Relatório QBR de Redes':

        namespace_rede = pd.read_csv('./CSV/QBR/Resultados Query/namespace_rede.csv', sep = ',')

        ######################### Filtro de rede ############################
        namespace_rede2 = namespace_rede.sort_values(by = 'name')
        namespace_rede3 = inserir_linha(pd.DataFrame(data = namespace_rede2['name'].unique()),pd.DataFrame({0: 'Rede'}, index=[-1]))
        namespace_rede_select = st.selectbox('👉 Selecione uma rede', namespace_rede3)

        ######################### Acesso a plataforma por alunos ############################
        alunos_acessaram_namespace_rede = pd.read_csv('./CSV/QBR/Resultados por namespace/alunos_acessaram_namespace.csv')
        
        ######################### Data de análise ############################
        dias = []
        for i in range(len(alunos_acessaram_namespace_rede['day'].unique())+1):
            dias.append(datetime.strptime(alunos_acessaram_namespace_rede['day'][i], '%Y-%m-%d').date())
        periodo_data = st.slider('👉 Data de análise',min(dias),max(dias),[min(dias),max(dias)],timedelta(1))
        
        ######################### Filtro de grupo ############################
        namespace_grupo2_aux = namespace_rede[namespace_rede['name'] == namespace_rede_select]
        namespace_grupo2 = namespace_grupo2_aux.sort_values(by = 'grupo')
        namespace_grupo3 = inserir_linha(pd.DataFrame(data = namespace_grupo2['grupo'].unique()),pd.DataFrame({0: 'Grupo'}, index=[-1]))
        namespace_grupo_select = st.multiselect('👉 Selecione um grupo', namespace_grupo3)

        if namespace_rede_select != 'Rede':
            """
                ### **Benefício 1**: Alunos engajados, no seu próprio ritmo e recebendo feedback em tempo real.
                ## 🚀 **Acesso à plataforma por alunos**
                Aqui analisamos a quantidade de acessos à plataforma, cada número representa a média semanal da quantidade de alunos que acessaram diariamente em relação ao número de alunos ativos.
            """
            alunos_acessaram_namespace_rede2 = filtro_uniao_rede(alunos_acessaram_namespace_rede,namespace_rede2,namespace_rede_select)
            alunos_acessaram_namespace_rede3 = obter_semana(alunos_acessaram_namespace_rede2,'day')
            alunos_acessaram_namespace_rede4 = filtro_data(alunos_acessaram_namespace_rede3,'day',periodo_data)
            alunos_acessaram_namespace_rede5 = alunos_acessaram_namespace_rede4.groupby(['name','grupo','Semana']).mean().reset_index()
            alunos_acessaram_namespace_rede6 = alunos_acessaram_namespace_rede4.groupby(['name','Semana']).mean().reset_index()       
            fig = px.bar(alunos_acessaram_namespace_rede6, x = alunos_acessaram_namespace_rede6['Semana'], y = 100*alunos_acessaram_namespace_rede6['Engajamento de alunos ativos'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(alunos_acessaram_namespace_rede6))

            if len(namespace_grupo_select) != 0:
                alunos_acessaram_namespace_rede5 = alunos_acessaram_namespace_rede5.reset_index(drop = True)
                cor = []
                for i in range(len(namespace_grupo_select)):
                    alunos_acessaram_namespace_rede7 = alunos_acessaram_namespace_rede5.loc[alunos_acessaram_namespace_rede5['grupo'] == namespace_grupo_select[i]]
                    cor.append("#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
                    fig.add_scatter(x = alunos_acessaram_namespace_rede7['Semana'], y = 100*alunos_acessaram_namespace_rede7['Engajamento de alunos ativos'],mode='lines', name = namespace_grupo_select[i], line=dict(color=cor[i]))
            fig.update_layout(title = "Engajamento de alunos ativos")
            st.plotly_chart(fig)  

            st.write('A média de acesso por alunos da rede por dia é **'+str(round(truncar(100*alunos_acessaram_namespace_rede6['Engajamento de alunos ativos'].mean(),3),3))+'%**.')

            """
                ## 🚀 **Exercícios resolvidos (Atividades Avaliativas)**
                Aqui analisamos a quantidade de exercícios resolvidos pelos alunos em atividades avaliativas, por aluno ativo, ou seja, é a média de exercícios de AA resolvidos por aluno em cada semana.
            """
            ######################### Exercícios realizados em AAs ############################
            exercicios_realizados_namespace_rede = pd.read_csv('./CSV/QBR/Resultados por namespace/exercicios_realizados_namespace.csv')
            exercicios_realizados_namespace_rede2 = filtro_uniao_rede(exercicios_realizados_namespace_rede,namespace_rede2,namespace_rede_select)
            exercicios_realizados_namespace_rede3 = obter_semana(exercicios_realizados_namespace_rede2,'creation')
            exercicios_realizados_namespace_rede4 = filtro_data(exercicios_realizados_namespace_rede3,'creation',periodo_data)
            exercicios_realizados_namespace_rede5 = exercicios_realizados_namespace_rede4.groupby(['name','grupo','namespace','Semana']).agg({'exercicios_realizados': 'sum', 'count': 'mean'}).reset_index() 
            exercicios_realizados_namespace_rede6 = exercicios_realizados_namespace_rede5.groupby(['name','Semana']).agg({'exercicios_realizados': 'sum', 'count': 'sum'}).reset_index() 
            exercicios_realizados_namespace_rede6['Exercícios resolvidos em AA por aluno'] = exercicios_realizados_namespace_rede6['exercicios_realizados']/exercicios_realizados_namespace_rede6['count']
            exercicios_realizados_namespace_rede7 = exercicios_realizados_namespace_rede6.drop(columns = ['exercicios_realizados','count'])
            
            fig = px.bar(exercicios_realizados_namespace_rede7, x = exercicios_realizados_namespace_rede7['Semana'], y = exercicios_realizados_namespace_rede7['Exercícios resolvidos em AA por aluno'], color_discrete_sequence = ['#4a8ae8']*len(exercicios_realizados_namespace_rede7))
            
            exercicios_realizados_namespace_rede8 = exercicios_realizados_namespace_rede5.groupby(['name','grupo','Semana']).agg({'exercicios_realizados': 'sum', 'count': 'sum'}).reset_index() 
            exercicios_realizados_namespace_rede8['Exercícios resolvidos em AA por aluno'] = exercicios_realizados_namespace_rede8['exercicios_realizados']/exercicios_realizados_namespace_rede8['count']
            exercicios_realizados_namespace_rede9 = exercicios_realizados_namespace_rede8.drop(columns = ['exercicios_realizados','count'])
            
            if len(namespace_grupo_select) != 0:
                exercicios_realizados_namespace_rede9 = exercicios_realizados_namespace_rede9.reset_index(drop = True)
                for i in range(len(namespace_grupo_select)):
                    exercicios_realizados_namespace_rede10 = exercicios_realizados_namespace_rede9.loc[exercicios_realizados_namespace_rede9['grupo'] == namespace_grupo_select[i]]
                    fig.add_scatter(x = exercicios_realizados_namespace_rede10['Semana'], y = exercicios_realizados_namespace_rede10['Exercícios resolvidos em AA por aluno'],mode='lines', name = namespace_grupo_select[i], line=dict(color=cor[i]))
            fig.update_layout(title = "Exercícios resolvidos em AA por aluno")
            st.plotly_chart(fig)   

            st.write('A média de exercícios resolvidos da rede em todas as semanas é **'+str(round(truncar(exercicios_realizados_namespace_rede8['Exercícios resolvidos em AA por aluno'].mean(),3),3))+'** exercícios por aluno.')

            """
                ## 🚀 **Exercícios resolvidos (Séries de exercícios)**
                Aqui analisamos a quantidade de exercícios resolvidos pelos alunos em séries de exercícios, por aluno ativo, ou seja, é a média de exercícios de SE resolvidos por aluno em cada semana.
            """
            ######################### Exercícios realizados em SEs ############################
            exercicios_realizados_se_namespace_rede = pd.read_csv('./CSV/QBR/Resultados por namespace/exercicios_realizados_se_namespace.csv')
            exercicios_realizados_se_namespace_rede2 = filtro_uniao_rede(exercicios_realizados_se_namespace_rede,namespace_rede2,namespace_rede_select)
            exercicios_realizados_se_namespace_rede3 = obter_semana(exercicios_realizados_se_namespace_rede2,'day')
            exercicios_realizados_se_namespace_rede4 = filtro_data(exercicios_realizados_se_namespace_rede3,'day',periodo_data)
            exercicios_realizados_se_namespace_rede5 = exercicios_realizados_se_namespace_rede4.groupby(['name','grupo','namespace','Semana']).agg({'num_ex': 'sum', 'count': 'mean'}).reset_index() 
            exercicios_realizados_se_namespace_rede6 = exercicios_realizados_se_namespace_rede5.groupby(['name','Semana']).agg({'num_ex': 'sum', 'count': 'sum'}).reset_index() 
            exercicios_realizados_se_namespace_rede6['Exercícios resolvidos em SE por aluno'] = exercicios_realizados_se_namespace_rede6['num_ex']/exercicios_realizados_se_namespace_rede6['count']
            exercicios_realizados_se_namespace_rede7 = exercicios_realizados_se_namespace_rede6.drop(columns = ['num_ex','count'])
            #st.dataframe(exercicios_realizados_se_namespace_rede7)

            fig = px.bar(exercicios_realizados_se_namespace_rede7, x = exercicios_realizados_se_namespace_rede7['Semana'], y = exercicios_realizados_se_namespace_rede7['Exercícios resolvidos em SE por aluno'], color_discrete_sequence = ['#4a8ae8']*len(exercicios_realizados_se_namespace_rede7))
            
            exercicios_realizados_se_namespace_rede8 = exercicios_realizados_se_namespace_rede5.groupby(['name','grupo','Semana']).agg({'num_ex': 'sum', 'count': 'sum'}).reset_index() 
            exercicios_realizados_se_namespace_rede8['Exercícios resolvidos em SE por aluno'] = exercicios_realizados_se_namespace_rede8['num_ex']/exercicios_realizados_se_namespace_rede8['count']
            exercicios_realizados_se_namespace_rede9 = exercicios_realizados_se_namespace_rede8.drop(columns = ['num_ex','count'])
            
            if len(namespace_grupo_select) != 0:
                exercicios_realizados_se_namespace_rede9 = exercicios_realizados_se_namespace_rede9.reset_index(drop = True)
                for i in range(len(namespace_grupo_select)):
                    exercicios_realizados_se_namespace_rede10 = exercicios_realizados_se_namespace_rede9.loc[exercicios_realizados_se_namespace_rede9['grupo'] == namespace_grupo_select[i]]
                    fig.add_scatter(x = exercicios_realizados_se_namespace_rede10['Semana'], y = exercicios_realizados_se_namespace_rede10['Exercícios resolvidos em SE por aluno'],mode='lines', name = namespace_grupo_select[i], line=dict(color=cor[i]))
            fig.update_layout(title = "Exercícios resolvidos em SE por aluno")
            st.plotly_chart(fig) 

            st.write('A média de exercícios resolvidos da rede em todas as semanas é **'+str(round(truncar(exercicios_realizados_se_namespace_rede8['Exercícios resolvidos em SE por aluno'].mean(),3),3))+'** exercícios por aluno.')

            """
                ## 🚀 **Conteúdos estudados**
                Aqui analisamos a quantidade de conteúdos estudados, por aluno ativo, ou seja, é a média de conteúdos estudados por aluno em cada semana.
            """
            ######################### Conteúdos estudados ############################
            conteudos_estudados_namespace_rede = pd.read_csv('./CSV/QBR/Resultados por namespace/conteudos_estudados_namespace.csv')
            conteudos_estudados_namespace_rede2 = filtro_uniao_rede(conteudos_estudados_namespace_rede,namespace_rede2,namespace_rede_select)
            conteudos_estudados_namespace_rede3 = obter_semana(conteudos_estudados_namespace_rede2,'day')
            conteudos_estudados_namespace_rede4 = filtro_data(conteudos_estudados_namespace_rede3,'day',periodo_data)
            conteudos_estudados_namespace_rede5 = conteudos_estudados_namespace_rede4.groupby(['name','grupo','namespace','Semana']).agg({'count_y': 'sum', 'count_x': 'mean'}).reset_index() 
            conteudos_estudados_namespace_rede6 = conteudos_estudados_namespace_rede5.groupby(['name','Semana']).agg({'count_y': 'sum', 'count_x': 'sum'}).reset_index() 
            conteudos_estudados_namespace_rede6['Conteúdos estudados por aluno'] = conteudos_estudados_namespace_rede6['count_y']/conteudos_estudados_namespace_rede6['count_x']
            conteudos_estudados_namespace_rede7 = conteudos_estudados_namespace_rede6.drop(columns = ['count_y','count_x'])
            #st.dataframe(conteudos_estudados_namespace_rede7)

            fig = px.bar(conteudos_estudados_namespace_rede7, x = conteudos_estudados_namespace_rede7['Semana'], y = conteudos_estudados_namespace_rede7['Conteúdos estudados por aluno'], color_discrete_sequence = ['#4a8ae8']*len(conteudos_estudados_namespace_rede7))
            
            conteudos_estudados_namespace_rede8 = conteudos_estudados_namespace_rede5.groupby(['name','grupo','Semana']).agg({'count_y': 'sum', 'count_x': 'sum'}).reset_index() 
            conteudos_estudados_namespace_rede8['Conteúdos estudados por aluno'] = conteudos_estudados_namespace_rede8['count_y']/conteudos_estudados_namespace_rede8['count_x']
            conteudos_estudados_namespace_rede9 = conteudos_estudados_namespace_rede8.drop(columns = ['count_y','count_x'])
            
            if len(namespace_grupo_select) != 0:
                conteudos_estudados_namespace_rede9 = conteudos_estudados_namespace_rede9.reset_index(drop = True)
                for i in range(len(namespace_grupo_select)):
                    conteudos_estudados_namespace_rede10 = conteudos_estudados_namespace_rede9.loc[conteudos_estudados_namespace_rede9['grupo'] == namespace_grupo_select[i]]
                    fig.add_scatter(x = conteudos_estudados_namespace_rede10['Semana'], y = conteudos_estudados_namespace_rede10['Conteúdos estudados por aluno'],mode='lines', name = namespace_grupo_select[i], line=dict(color=cor[i]))
            fig.update_layout(title = "Conteúdos estudados por aluno")
            st.plotly_chart(fig) 

            st.write('A média de conteúdos estudados da rede em todas as semanas é **'+str(round(truncar(conteudos_estudados_namespace_rede8['Conteúdos estudados por aluno'].mean(),3),3))+'** conteúdos por aluno.')

            """
                ### **Benefício 2**: Professores que estão personalizando a aprendizagem.
                ## 🚀 **Acesso à plataforma por professores**
                Aqui analisamos a quantidade de acessos à plataforma, cada número representa a média semanal da quantidade de professores que acessaram diariamente em relação ao número de professores ativos.
            """
            ######################### Acesso a plataforma por professores ############################
            profs_acessaram_rede = pd.read_csv('./CSV/QBR/Resultados por namespace/profs_acessaram.csv')
            profs_acessaram_rede2 = filtro_uniao_rede(profs_acessaram_rede,namespace_rede2,namespace_rede_select)
            profs_acessaram_rede3 = obter_semana(profs_acessaram_rede2,'day')
            profs_acessaram_rede4 = filtro_data(profs_acessaram_rede3,'day',periodo_data)
            profs_acessaram_rede5 = profs_acessaram_rede4.groupby(['name','grupo','namespace','Semana']).agg({'count_y': 'mean', 'count_x': 'mean'}).reset_index() 
            profs_acessaram_rede6 = profs_acessaram_rede5.groupby(['name','Semana']).agg({'count_y': 'sum', 'count_x': 'sum'}).reset_index() 
            profs_acessaram_rede6['Engajamento de professores'] = profs_acessaram_rede6['count_y']/profs_acessaram_rede6['count_x']
            profs_acessaram_rede7 = profs_acessaram_rede6.drop(columns = ['count_y','count_x'])
            #st.dataframe(profs_acessaram_rede7)

            fig = px.bar(profs_acessaram_rede7, x = profs_acessaram_rede7['Semana'], y = 100*profs_acessaram_rede7['Engajamento de professores'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(profs_acessaram_rede7))
            
            profs_acessaram_rede8 = profs_acessaram_rede5.groupby(['name','grupo','Semana']).agg({'count_y': 'sum', 'count_x': 'sum'}).reset_index() 
            profs_acessaram_rede8['Engajamento de professores'] = profs_acessaram_rede8['count_y']/profs_acessaram_rede8['count_x']
            profs_acessaram_rede9 = profs_acessaram_rede8.drop(columns = ['count_y','count_x'])
            
            if len(namespace_grupo_select) != 0:
                profs_acessaram_rede9 = profs_acessaram_rede9.reset_index(drop = True)
                for i in range(len(namespace_grupo_select)):
                    profs_acessaram_rede10 = profs_acessaram_rede9.loc[profs_acessaram_rede9['grupo'] == namespace_grupo_select[i]]
                    fig.add_scatter(x = profs_acessaram_rede10['Semana'], y = 100*profs_acessaram_rede10['Engajamento de professores'],mode='lines', name = namespace_grupo_select[i], line=dict(color=cor[i]))
            fig.update_layout(title = "Engajamento de professores")
            st.plotly_chart(fig) 

            st.write('A média de acesso por professores da rede por dia é **'+str(round(truncar(100*profs_acessaram_rede8['Engajamento de professores'].mean(),3),3))+'%**.')

            """
                ## 🚀 **Materiais criados por professor**
                Aqui analisamos a quantidade de materiais criador por professor, cada número representa a média semanal da quantidade de materiais postados.
            """
            ######################### Professores materiais ############################
            profs_materiais_rede = pd.read_csv('./CSV/QBR/Resultados por namespace/profs_materiais.csv')
            profs_materiais_rede2 = filtro_uniao_rede(profs_materiais_rede,namespace_rede2,namespace_rede_select)
            profs_materiais_rede3 = obter_semana(profs_materiais_rede2,'created')
            profs_materiais_rede4 = filtro_data(profs_materiais_rede3,'created',periodo_data)
            profs_materiais_rede5 = profs_materiais_rede4.groupby(['name','grupo','namespace','Semana']).agg({'count_y': 'sum', 'count_x': 'mean'}).reset_index() 
            profs_materiais_rede6 = profs_materiais_rede5.groupby(['name','Semana']).agg({'count_y': 'sum', 'count_x': 'sum'}).reset_index() 
            profs_materiais_rede6['Materiais criados por professor'] = profs_materiais_rede6['count_y']/profs_materiais_rede6['count_x']
            profs_materiais_rede7 = profs_materiais_rede6.drop(columns = ['count_y','count_x'])
            #st.dataframe(profs_materiais_rede7)

            fig = px.bar(profs_materiais_rede7, x = profs_materiais_rede7['Semana'], y = profs_materiais_rede7['Materiais criados por professor'], color_discrete_sequence = ['#4a8ae8']*len(profs_materiais_rede7))
            
            profs_materiais_rede8 = profs_materiais_rede5.groupby(['name','grupo','Semana']).agg({'count_y': 'sum', 'count_x': 'sum'}).reset_index() 
            profs_materiais_rede8['Materiais criados por professor'] = profs_materiais_rede8['count_y']/profs_materiais_rede8['count_x']
            profs_materiais_rede9 = profs_materiais_rede8.drop(columns = ['count_y','count_x'])
            
            if len(namespace_grupo_select) != 0:
                profs_materiais_rede9 = profs_materiais_rede9.reset_index(drop = True)
                for i in range(len(namespace_grupo_select)):
                    profs_materiais_rede10 = profs_materiais_rede9.loc[profs_materiais_rede9['grupo'] == namespace_grupo_select[i]]
                    fig.add_scatter(x = profs_materiais_rede10['Semana'], y = profs_materiais_rede10['Materiais criados por professor'],mode='lines', name = namespace_grupo_select[i], line=dict(color=cor[i]))
            fig.update_layout(title = "Materiais criados por professor")
            st.plotly_chart(fig) 

            st.write('A média de materiais postados por professor da rede por semana é **'+str(round(truncar(profs_materiais_rede8['Materiais criados por professor'].mean(),3),3))+'**.')

            """
                ## 🚀 **Exercícios criados por professor**
                Aqui analisamos a quantidade de exercícios criador por professor, cada número representa a média semanal da quantidade de exercícios postados.
            """
            ######################### Professores exercícios ############################
            profs_exercicios_rede = pd.read_csv('./CSV/QBR/Resultados por namespace/profs_exercicios.csv')
            profs_exercicios_rede2 = filtro_uniao_rede(profs_exercicios_rede,namespace_rede2,namespace_rede_select)
            profs_exercicios_rede3 = obter_semana(profs_exercicios_rede2,'created')
            profs_exercicios_rede4 = filtro_data(profs_exercicios_rede3,'created',periodo_data)
            profs_exercicios_rede5 = profs_exercicios_rede4.groupby(['name','grupo','namespace','Semana']).agg({'count_y': 'sum', 'count_x': 'mean'}).reset_index() 
            profs_exercicios_rede6 = profs_exercicios_rede5.groupby(['name','Semana']).agg({'count_y': 'sum', 'count_x': 'sum'}).reset_index() 
            profs_exercicios_rede6['Exercícios criados por professor'] = profs_exercicios_rede6['count_y']/profs_exercicios_rede6['count_x']
            profs_exercicios_rede7 = profs_exercicios_rede6.drop(columns = ['count_y','count_x'])
            #st.dataframe(profs_exercicios_rede7)

            fig = px.bar(profs_exercicios_rede7, x = profs_exercicios_rede7['Semana'], y = profs_exercicios_rede7['Exercícios criados por professor'], color_discrete_sequence = ['#4a8ae8']*len(profs_exercicios_rede7))
            
            profs_exercicios_rede8 = profs_exercicios_rede5.groupby(['name','grupo','Semana']).agg({'count_y': 'sum', 'count_x': 'sum'}).reset_index() 
            profs_exercicios_rede8['Exercícios criados por professor'] = profs_exercicios_rede8['count_y']/profs_exercicios_rede8['count_x']
            profs_exercicios_rede9 = profs_exercicios_rede8.drop(columns = ['count_y','count_x'])
            
            if len(namespace_grupo_select) != 0:
                profs_exercicios_rede9 = profs_exercicios_rede9.reset_index(drop = True)
                for i in range(len(namespace_grupo_select)):
                    profs_exercicios_rede10 = profs_exercicios_rede9.loc[profs_exercicios_rede9['grupo'] == namespace_grupo_select[i]]
                    fig.add_scatter(x = profs_exercicios_rede10['Semana'], y = profs_exercicios_rede10['Exercícios criados por professor'],mode='lines', name = namespace_grupo_select[i], line=dict(color=cor[i]))
            fig.update_layout(title = "Exercícios criados por professor")
            st.plotly_chart(fig) 

            st.write('A média de exercícios criados por professor da rede por semana é **'+str(round(truncar(profs_exercicios_rede8['Exercícios criados por professor'].mean(),3),3))+'**.')

            """
                ### **Benefício 3**: Escola que analisa dados para personalização da aprendizagem.
                ## 🚀 **Visualização de relatórios por professor**
                Aqui analisamos a visualização de relatórios por professor semanalmente, ou seja cada número representa a porcentagem de professores que visualizações relatórios em cada semana.
            """
            ######################### Professores visualização de relatórios ############################
            profs_relatorios_rede = pd.read_csv('./CSV/QBR/Resultados por namespace/profs_relatorios.csv')
            profs_relatorios_rede2 = filtro_uniao_rede(profs_relatorios_rede,namespace_rede2,namespace_rede_select)
            profs_relatorios_rede3 = obter_semana(profs_relatorios_rede2,'creation')
            profs_relatorios_rede4 = filtro_data(profs_relatorios_rede3,'creation',periodo_data)
            profs_relatorios_rede5 = profs_relatorios_rede4.groupby(['name','grupo','namespace','Semana']).nunique().reset_index()
            profs_relatorios_rede6 = profs_relatorios_rede5.drop(columns = ['creation','type'])
            profs_ativos2 = pd.read_csv('./CSV/QBR/Resultados Query/profs_ativos.csv', sep = ',')
            profs_ativos3 = profs_ativos2.drop(columns = ['Unnamed: 0'])
            profs_relatorios_rede7 = pd.merge(profs_ativos3,profs_relatorios_rede6, on = 'namespace', how = 'inner')
            #st.dataframe(profs_relatorios_rede7)

            profs_relatorios_rede8 = profs_relatorios_rede7.groupby(['name','grupo','namespace','Semana']).agg({'user_id': 'sum', 'count': 'mean'}).reset_index() 
            profs_relatorios_rede9 = profs_relatorios_rede8.groupby(['name','Semana']).agg({'user_id': 'sum', 'count': 'sum'}).reset_index() 
            profs_relatorios_rede9['Engajamento de visualização de relatórios por professor'] = profs_relatorios_rede9['user_id']/profs_relatorios_rede9['count']
            profs_relatorios_rede10 = profs_relatorios_rede9.drop(columns = ['user_id','count'])
            #st.dataframe(profs_relatorios_rede10)

            fig = px.bar(profs_relatorios_rede10, x = profs_relatorios_rede10['Semana'], y = 100*profs_relatorios_rede10['Engajamento de visualização de relatórios por professor'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(profs_relatorios_rede10))
            
            profs_relatorios_rede11 = profs_relatorios_rede8.groupby(['name','grupo','Semana']).agg({'user_id': 'sum', 'count': 'sum'}).reset_index() 
            profs_relatorios_rede11['Engajamento de visualização de relatórios por professor'] = profs_relatorios_rede11['user_id']/profs_relatorios_rede11['count']
            profs_relatorios_rede12 = profs_relatorios_rede11.drop(columns = ['user_id','count'])
            
            if len(namespace_grupo_select) != 0:
                profs_relatorios_rede12 = profs_relatorios_rede12.reset_index(drop = True)
                for i in range(len(namespace_grupo_select)):
                    profs_relatorios_rede13 = profs_relatorios_rede12.loc[profs_relatorios_rede12['grupo'] == namespace_grupo_select[i]]
                    fig.add_scatter(x = profs_relatorios_rede13['Semana'], y = 100*profs_relatorios_rede13['Engajamento de visualização de relatórios por professor'],mode='lines', name = namespace_grupo_select[i], line=dict(color=cor[i]))
            fig.update_layout(title = "Engajamento de visualização de relatórios por professor")
            st.plotly_chart(fig) 

            st.write('A porcentagem de professores da rede que visualizaram relatórios semanalmente é de **'+str(round(truncar(100*profs_relatorios_rede11['Engajamento de visualização de relatórios por professor'].mean(),3),3))+'%**.')

            #st.warning('Em construção!')

    if escolha_relatorio == 'Relatório de Rotinas pegagógicas (em construção)':

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

            row = [str(datetime.today()),nome,rede_select,grupo_select,gestor_select,produto_select,licenças_select,namespace_select]
            index = 2
            sheet.insert_row(row, index)
            #st.dataframe(banco_de_dados2)

            st.subheader('**Resultados gerais por Rotina Pedagógica Digital**')

            ############## Avaliação Continuada ##############

            ###### Leitura dos dados de cada rotina por namespace ######
            avaliacao_continuada_namespace = pd.read_csv('./CSV/Avaliação Continuada/Resultados por namespace/avaliacao_continuada_namespace.csv')
            avaliacao_continuada_namespace2 = pd.merge(namespaces_x_hubspot3['namespace'],avaliacao_continuada_namespace, on = 'namespace', how = 'left')
            avaliacao_continuada_namespace3 = avaliacao_continuada_namespace2.groupby('namespace').mean().reset_index()
            avaliacao_continuada_namespace4 = avaliacao_continuada_namespace3.drop(columns = ['Unnamed: 0'])

            ###### Leitura dos dados de cada rotina temporal ######
            avaliacao_continuada_temporal = pd.read_csv('./CSV/Avaliação Continuada/Resultados temporais/avaliacao_continuada_temporal.csv')
            avaliacao_continuada_temporal2 = pd.merge(namespaces_x_hubspot3['namespace'],avaliacao_continuada_temporal, on = 'namespace', how = 'left')

            ###### Leitura dos dados de cada rotina por ano escolar ######
            avaliacao_continuada_anoescolar = pd.read_csv('./CSV/Avaliação Continuada/Resultados por ano escolar/avaliacao_continuada_anoescolar.csv')
            avaliacao_continuada_anoescolar2 = pd.merge(namespaces_x_hubspot3['namespace'],avaliacao_continuada_anoescolar, on = 'namespace', how = 'left')

            ###### Normalização dos dados ######
            for coluna in avaliacao_continuada_namespace4.columns:
                if coluna in ('Número de exercícios por turma','Média de séries de exercícios por turma','Número de AAs iniciadas por aluno'):
                    avaliacao_continuada_namespace4 = normalizacao(avaliacao_continuada_namespace4,coluna,0.1, 0.9)
                if coluna in ('Número de exercícios por turma','Média de séries de exercícios por turma','Número de AAs iniciadas por aluno'):
                    avaliacao_continuada_anoescolar2 = normalizacao(avaliacao_continuada_anoescolar2,coluna,0.1, 0.9)
                if coluna in ('Número de exercícios por turma','Média de séries de exercícios por turma','Número de AAs iniciadas por aluno'):
                    avaliacao_continuada_temporal2 = normalizacao(avaliacao_continuada_temporal2,coluna,0.1, 0.9)

            ###### Média Final ######
            col = avaliacao_continuada_namespace4.loc[: , "Porcentagem de engajamento em série de exercícios":"Número de AAs iniciadas por aluno"]
            avaliacao_continuada_namespace4['Média'] = col.mean(axis=1)
            col = avaliacao_continuada_anoescolar2.loc[: , "Porcentagem de engajamento em série de exercícios":"Número de AAs iniciadas por aluno"]
            avaliacao_continuada_anoescolar2['Média'] = col.mean(axis=1)
            avaliacao_continuada_anoescolar3 = avaliacao_continuada_anoescolar2.drop(columns = ['Unnamed: 0'])
            col = avaliacao_continuada_temporal2.loc[: , "Porcentagem de engajamento em série de exercícios":"Número de AAs iniciadas por aluno"]
            avaliacao_continuada_temporal2['Média'] = col.mean(axis=1)

            ###### Quartis ######
            avaliacao_continuada_namespace5 = quartis(avaliacao_continuada_namespace4,'Média')
            avaliacao_continuada_namespace_select = avaliacao_continuada_namespace5[avaliacao_continuada_namespace5['namespace'] == namespace_select].reset_index(drop = True)
            avaliacao_continuada_anoescolar4 = quartis(avaliacao_continuada_anoescolar3,'Média')
            avaliacao_continuada_anoescolar_select = avaliacao_continuada_anoescolar4[avaliacao_continuada_anoescolar4['namespace'] == namespace_select].reset_index(drop = True)
            avaliacao_continuada_temporal3 = quartis(avaliacao_continuada_temporal2,'Média')
            avaliacao_continuada_temporal_select = avaliacao_continuada_temporal3[avaliacao_continuada_temporal3['namespace'] == namespace_select].reset_index(drop = True)

            ###### Média do namespace x média Eduqo ######
            if avaliacao_continuada_namespace_select['Média'][0] >= avaliacao_continuada_namespace5['Média'].mean():
                comparativo_media_avaliacao_continuada = ' 🟩'
            else:
                comparativo_media_avaliacao_continuada = ' 🟨'
            st.subheader('**Avaliação Continuada'+' (Pontuação: '+str(round(100*avaliacao_continuada_namespace_select['Média'][0], 2))+')**')
            st.markdown('O namespace '+namespace_select+ ' está no **'+avaliacao_continuada_namespace_select['Quartil'][0]+ ' quartil**!') 
            st.progress(avaliacao_continuada_namespace_select['Média'][0])
            st.write('Pontuação **Média Eduqo: '+str(round(100*avaliacao_continuada_namespace5['Média'].mean(), 2))+comparativo_media_avaliacao_continuada+'**')

            ###### Junção Hubspot para pegar média das escolas que tem o mesmo produto e mesma faixa de licenças ######
            juncao_hubspot_continuada_namespace = pd.merge(namespaces_x_hubspot3,avaliacao_continuada_namespace4, on = 'namespace', how = 'left')
            avaliacao_continuada_namespace_select_juncao = juncao_hubspot_continuada_namespace[juncao_hubspot_continuada_namespace['namespace'] == namespace_select].reset_index(drop = True)
            juncao_hubspot_continuada_namespace2 = juncao_hubspot_continuada_namespace[juncao_hubspot_continuada_namespace['Produto'] == avaliacao_continuada_namespace_select_juncao['Produto'][0]]
            juncao_hubspot_continuada_namespace3 = juncao_hubspot_continuada_namespace2[juncao_hubspot_continuada_namespace2['licenças'] == avaliacao_continuada_namespace_select_juncao['licenças'][0]]
            if avaliacao_continuada_namespace_select['Média'][0] >= juncao_hubspot_continuada_namespace3['Média'].mean():
                comparativo_media_avaliacao_continuada_juncao = ' 🟩'
            else:
                comparativo_media_avaliacao_continuada_juncao = ' 🟨'
            st.write('Pontuação **Média '+avaliacao_continuada_namespace_select_juncao['Produto'][0]+' com faixa de licenças de '+avaliacao_continuada_namespace_select_juncao['licenças'][0]+': '+str(round(100*juncao_hubspot_continuada_namespace3['Média'].mean(), 2))+comparativo_media_avaliacao_continuada_juncao+'**')

            ###### Gráfico temporal ######
            juncao_hubspot_continuada_temporal = pd.merge(namespaces_x_hubspot3,avaliacao_continuada_temporal3, on = 'namespace', how = 'left')
            avaliacao_continuada_temporal_select_juncao = juncao_hubspot_continuada_temporal[juncao_hubspot_continuada_temporal['namespace'] == namespace_select].reset_index(drop = True)
            juncao_hubspot_continuada_temporal2 = juncao_hubspot_continuada_temporal[juncao_hubspot_continuada_temporal['Produto'] == avaliacao_continuada_temporal_select_juncao['Produto'][0]]
            juncao_hubspot_continuada_temporal3 = juncao_hubspot_continuada_temporal2[juncao_hubspot_continuada_temporal2['licenças'] == avaliacao_continuada_temporal_select_juncao['licenças'][0]]

            with st.expander("Visualizar o histórico semanal da média de Avaliação Continuada -> (clique aqui 🖱️)"):
                avaliacao_continuada_temporal_select['Média'] = 100*avaliacao_continuada_temporal_select['Média']
                avaliacao_continuada_temporal_select2 = avaliacao_continuada_temporal_select.groupby('Semana').mean().reset_index()
                fig = px.bar(avaliacao_continuada_temporal_select2, x = avaliacao_continuada_temporal_select2['Semana'], y = avaliacao_continuada_temporal_select2['Média'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(avaliacao_continuada_temporal_select2))
                avaliacao_continuada_temporal5 = avaliacao_continuada_temporal3.groupby('Semana').mean().reset_index()
                fig.add_scatter(x = avaliacao_continuada_temporal5['Semana'], y = 100*avaliacao_continuada_temporal5['Média'],mode='lines', name = 'Média Eduqo', line=dict(color="red"))
                juncao_hubspot_continuada_temporal4 = juncao_hubspot_continuada_temporal3.groupby('Semana').mean().reset_index()
                fig.add_scatter(x = juncao_hubspot_continuada_temporal4['Semana'], y = 100*juncao_hubspot_continuada_temporal4['Média'],mode='lines', name = 'Média '+avaliacao_continuada_temporal_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_continuada_temporal_select_juncao['licenças'][0], line=dict(color="black"))
                fig.update_layout(title = "Pontuação média em Avaliação Continuada por semana")
                fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
                st.plotly_chart(fig)


            ###### Gráfico por ano escolar ######
            juncao_hubspot_continuada_anoescolar = pd.merge(namespaces_x_hubspot3,avaliacao_continuada_anoescolar4, on = 'namespace', how = 'left')
            avaliacao_continuada_anoescolar_select_juncao = juncao_hubspot_continuada_anoescolar[juncao_hubspot_continuada_anoescolar['namespace'] == namespace_select].reset_index(drop = True)
            juncao_hubspot_continuada_anoescolar2 = juncao_hubspot_continuada_anoescolar[juncao_hubspot_continuada_anoescolar['Produto'] == avaliacao_continuada_anoescolar_select_juncao['Produto'][0]]
            juncao_hubspot_continuada_anoescolar3 = juncao_hubspot_continuada_anoescolar2[juncao_hubspot_continuada_anoescolar2['licenças'] == avaliacao_continuada_anoescolar_select_juncao['licenças'][0]]

            with st.expander("Visualizar a média de Avaliação Continuada por ano escolar -> (clique aqui 🖱️)"):
                avaliacao_continuada_anoescolar_select['Média'] = 100*avaliacao_continuada_anoescolar_select['Média']
                avaliacao_continuada_anoescolar_select_aux = avaliacao_continuada_anoescolar_select.groupby('grade').mean().reset_index()
                avaliacao_continuada_anoescolar_select2 = avaliacao_continuada_anoescolar_select_aux.sort_values(by = 'grade')
                avaliacao_continuada_anoescolar5 = avaliacao_continuada_anoescolar4.groupby('grade').mean().reset_index()
                avaliacao_continuada_anoescolar6 = avaliacao_continuada_anoescolar5.sort_values(by = 'grade')
                juncao_hubspot_continuada_anoescolar4 = juncao_hubspot_continuada_anoescolar3.groupby('grade').mean().reset_index()
                juncao_hubspot_continuada_anoescolar5 = juncao_hubspot_continuada_anoescolar4.sort_values(by = 'grade')
                juncao_auxiliar_continuada = pd.merge(avaliacao_continuada_anoescolar6,juncao_hubspot_continuada_anoescolar5, on = 'grade', how = 'left')
                juncao_auxiliar_continuada2 = pd.merge(juncao_auxiliar_continuada,avaliacao_continuada_anoescolar_select2, on = 'grade', how = 'left')
                fig2 = px.bar(juncao_auxiliar_continuada2, x = juncao_auxiliar_continuada2['grade'], y = juncao_auxiliar_continuada2['Média'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(juncao_auxiliar_continuada2))
                fig2.add_scatter(x = juncao_auxiliar_continuada2['grade'], y = 100*juncao_auxiliar_continuada2['Média_x'], name = 'Média Eduqo', line=dict(color="red"))
                fig2.add_scatter(x = juncao_auxiliar_continuada2['grade'], y = 100*juncao_auxiliar_continuada2['Média_y'], name = 'Média '+avaliacao_continuada_anoescolar_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_continuada_anoescolar_select_juncao['licenças'][0], line=dict(color="black"))
                fig2.update_layout(title = "Pontuação média em Avaliação Continuada por ano escolar")
                fig2.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
                st.plotly_chart(fig2)

            st.write('---')

            ############## Avaliação Diagnóstica ##############

            ###### Leitura dos dados de cada rotina por namespace ######
            avaliacao_diagnostica_namespace = pd.read_csv('./CSV/Avaliação Diagnóstica/Resultados por namespace/avaliacao_diagnostica_namespace.csv')
            avaliacao_diagnostica_namespace2 = pd.merge(namespaces_x_hubspot3['namespace'],avaliacao_diagnostica_namespace, on = 'namespace', how = 'left')
            avaliacao_diagnostica_namespace3 = avaliacao_diagnostica_namespace2.groupby('namespace').mean().reset_index()
            avaliacao_diagnostica_namespace4 = avaliacao_diagnostica_namespace3.drop(columns = ['Unnamed: 0'])

            ###### Leitura dos dados de cada rotina por ano escolar ######
            avaliacao_diagnostica_anoescolar = pd.read_csv('./CSV/Avaliação Diagnóstica/Resultados por ano escolar/avaliacao_diagnostica_anoescolar.csv')
            avaliacao_diagnostica_anoescolar2 = pd.merge(namespaces_x_hubspot3['namespace'],avaliacao_diagnostica_anoescolar, on = 'namespace', how = 'left')

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

            ###### Normalização dos dados por ano escolar ######
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
            avaliacao_somativa_temporal_select['Tempo de correção por aluno por questão'] = pd.to_numeric(avaliacao_somativa_temporal_select['Tempo de correção por aluno por questão'],errors = 'coerce')
            avaliacao_somativa_temporal_select['Tempo médio entre publicação e ínicio de AA'] = pd.to_numeric(avaliacao_somativa_temporal_select['Tempo médio entre publicação e ínicio de AA'],errors = 'coerce')
            avaliacao_somativa_temporal_select['Tempo médio entre criação e publicação de AA por questão'] = pd.to_numeric(avaliacao_somativa_temporal_select['Tempo médio entre criação e publicação de AA por questão'],errors = 'coerce')                
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
                avaliacao_somativa_temporal_select2 = avaliacao_somativa_temporal_select.groupby('Semana').mean().reset_index()
                fig = px.bar(avaliacao_somativa_temporal_select2, x = avaliacao_somativa_temporal_select2['Semana'], y = avaliacao_somativa_temporal_select2['Média'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(avaliacao_somativa_temporal_select2))
                avaliacao_somativa_temporal4['Tempo de correção por aluno por questão'] = pd.to_numeric(avaliacao_somativa_temporal4['Tempo de correção por aluno por questão'],errors = 'coerce')
                avaliacao_somativa_temporal4['Tempo médio entre publicação e ínicio de AA'] = pd.to_numeric(avaliacao_somativa_temporal4['Tempo médio entre publicação e ínicio de AA'],errors = 'coerce')
                avaliacao_somativa_temporal4['Tempo médio entre criação e publicação de AA por questão'] = pd.to_numeric(avaliacao_somativa_temporal4['Tempo médio entre criação e publicação de AA por questão'],errors = 'coerce')
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
                juncao_auxiliar_somativa = pd.merge(avaliacao_somativa_anoescolar6,juncao_hubspot_somativa_anoescolar5, on = 'grade', how = 'left')
                juncao_auxiliar_somativa2 = pd.merge(juncao_auxiliar_somativa,avaliacao_somativa_anoescolar_select2, on = 'grade', how = 'left')
                fig2 = px.bar(juncao_auxiliar_somativa2, x = juncao_auxiliar_somativa2['grade'], y = juncao_auxiliar_somativa2['Média'], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(juncao_auxiliar_somativa2))
                fig2.add_scatter(x = juncao_auxiliar_somativa2['grade'], y = 100*juncao_auxiliar_somativa2['Média_x'], name = 'Média Eduqo', line=dict(color="red"))
                fig2.add_scatter(x = juncao_auxiliar_somativa2['grade'], y = 100*juncao_auxiliar_somativa2['Média_y'], name = 'Média '+avaliacao_somativa_anoescolar_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_somativa_anoescolar_select_juncao['licenças'][0], line=dict(color="black"))
                fig2.update_layout(title = "Pontuação média em Avaliação Somativa por ano escolar")
                fig2.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
                st.plotly_chart(fig2)

            st.write('---')

            ######################## Resultados detalhados por rotina ########################

            st.subheader('**Resultados detalhados por Rotina Pedagógica Digital**')

            ############## Avaliação Continuada ##############

            st.markdown('**Avaliação Continuada**')

            ###### Namespaces destaques ######
            avaliacao_continuada_namespace6 = avaliacao_continuada_namespace5.copy()
            avaliacao_continuada_namespace6['Média'] = round(100*avaliacao_continuada_namespace6['Média'],2)
            avaliacao_continuada_namespace6.rename(columns = {'Média':'Média (0 a 100)'}, inplace = True)
            avaliacao_continuada_namespace7 = pd.DataFrame()
            avaliacao_continuada_namespace7['namespace'] = avaliacao_continuada_namespace6['namespace']
            avaliacao_continuada_namespace7['Média (0 a 100)'] = avaliacao_continuada_namespace6['Média (0 a 100)']
            avaliacao_continuada_namespace7['Quartil'] = avaliacao_continuada_namespace6['Quartil']
            avaliacao_continuada_namespace8 = avaliacao_continuada_namespace7.groupby('namespace').mean()
            avaliacao_continuada_namespace9 = quartis(avaliacao_continuada_namespace8,'Média (0 a 100)').reset_index()
            avaliacao_continuada_namespace10 = avaliacao_continuada_namespace9.sort_values(by = 'Média (0 a 100)', ascending = False)
            with st.expander("Visualizar as escolas destaque em Avaliação Continuada -> (clique aqui 🖱️)"):
                avaliacao_continuada_namespace11 = destaques_rotina(avaliacao_continuada_namespace10)
                st.table(avaliacao_continuada_namespace11)

            ###### Visualizar um quartil ######
            ver_quartil_avaliacao_continuada = st.radio('Escolha o quartil que deseja ver os resultados de Avaliação Continuada 📈',('Nenhum','1º','2º','3º','4º'))
            if ver_quartil_avaliacao_continuada != 'Nenhum':
                avaliacao_continuada_namespace_quartil = visualizacao_resultado_quartil(ver_quartil_avaliacao_continuada,avaliacao_continuada_namespace10)
                st.table(avaliacao_continuada_namespace_quartil)

            ###### Visualização das métricas do namespace selecionado ######
            with st.expander("Visualizar os resultados de Avaliação Continuada do namespace selecionado por métrica -> (clique aqui 🖱️)"):
                for coluna in avaliacao_continuada_namespace_select.columns:
                    if (coluna != 'namespace' and coluna != 'Média' and coluna != 'Quartil'):
                        if avaliacao_continuada_namespace_select[coluna][0] >= avaliacao_continuada_namespace6[coluna].mean():
                            comparativo_media_avaliacao_continuada = ' 🟩'
                        else:
                            comparativo_media_avaliacao_continuada = ' 🟨'
                        st.markdown('**'+coluna+' (Pontuação: '+str(round(100*avaliacao_continuada_namespace_select[coluna][0], 2))+')**')
                        st.progress(avaliacao_continuada_namespace_select[coluna][0])
                        st.write('**Média Eduqo: '+str(round(100*avaliacao_continuada_namespace6[coluna].mean(), 2))+comparativo_media_avaliacao_continuada+'**')
                        if avaliacao_continuada_namespace_select[coluna][0] >= juncao_hubspot_continuada_namespace3[coluna].mean():
                            comparativo_media_avaliacao_continuada_juncao = ' 🟩'
                        else:
                            comparativo_media_avaliacao_continuada_juncao = ' 🟨'
                        st.write('**Média '+avaliacao_continuada_namespace_select_juncao['Produto'][0]+' com faixa de licenças de '+avaliacao_continuada_namespace_select_juncao['licenças'][0]+': '+str(round(100*juncao_hubspot_continuada_namespace3[coluna].mean(), 2))+comparativo_media_avaliacao_continuada_juncao+'**')
                        beta = st.checkbox('Visualizar histórico semanal de '+coluna+' -> (clique aqui 🖱️)')
                        if beta == True:
                            avaliacao_continuada_temporal_select[coluna] = 100*avaliacao_continuada_temporal_select[coluna]
                            fig = px.bar(avaliacao_continuada_temporal_select, x = avaliacao_continuada_temporal_select['Semana'], y = coluna, range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(avaliacao_continuada_temporal_select))
                            avaliacao_continuada_temporal5 = avaliacao_continuada_temporal3.groupby('Semana').mean().reset_index()
                            fig.add_scatter(x = avaliacao_continuada_temporal5['Semana'], y = 100*avaliacao_continuada_temporal5[coluna],mode='lines', name = 'Média Eduqo', line=dict(color="red"))
                            juncao_hubspot_continuada_temporal4 = juncao_hubspot_continuada_temporal3.groupby('Semana').mean().reset_index()
                            fig.add_scatter(x = juncao_hubspot_continuada_temporal4['Semana'], y = 100*juncao_hubspot_continuada_temporal4[coluna],mode='lines', name = 'Média '+avaliacao_continuada_temporal_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_continuada_temporal_select_juncao['licenças'][0], line=dict(color="black"))
                            fig.update_layout(title = "Pontuação média por semana")
                            fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
                            st.plotly_chart(fig)
                        beta = st.checkbox('Visualizar resultados por ano escolar de '+coluna+' -> (clique aqui 🖱️)')
                        if beta == True:
                            juncao_auxiliar_continuada2[coluna] = 100*juncao_auxiliar_continuada2[coluna]
                            fig2 = px.bar(juncao_auxiliar_continuada2, x = juncao_auxiliar_continuada2['grade'], y = juncao_auxiliar_continuada2[coluna], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(juncao_auxiliar_continuada2))
                            fig2.add_scatter(x = juncao_auxiliar_continuada2['grade'], y = 100*juncao_auxiliar_continuada2[coluna+'_x'], name = 'Média Eduqo', line=dict(color="red"))
                            fig2.add_scatter(x = juncao_auxiliar_continuada2['grade'], y = 100*juncao_auxiliar_continuada2[coluna+'_y'], name = 'Média '+avaliacao_continuada_anoescolar_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_continuada_anoescolar_select_juncao['licenças'][0], line=dict(color="black"))
                            fig2.update_layout(title = "Pontuação média por ano escolar")
                            fig2.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
                            st.plotly_chart(fig2)
                        st.write('----')

            st.write('---')

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

            st.write('---')

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
                            beta = st.checkbox('Visualizar histórico semanal de '+coluna+' -> (clique aqui 🖱️) ')
                            if beta == True:
                                avaliacao_somativa_temporal_select[coluna] = 100*avaliacao_somativa_temporal_select[coluna]
                                fig = px.bar(avaliacao_somativa_temporal_select, x = avaliacao_somativa_temporal_select['Semana'], y = coluna, range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(avaliacao_somativa_temporal_select))
                                avaliacao_somativa_temporal5 = avaliacao_somativa_temporal4.groupby('Semana').mean().reset_index()
                                fig.add_scatter(x = avaliacao_somativa_temporal5['Semana'], y = 100*avaliacao_somativa_temporal5[coluna],mode='lines', name = 'Média Eduqo', line=dict(color="red"))
                                juncao_hubspot_somativa_temporal3['Tempo de correção por aluno por questão'] = pd.to_numeric(juncao_hubspot_somativa_temporal3['Tempo de correção por aluno por questão'],errors = 'coerce')
                                juncao_hubspot_somativa_temporal3['Tempo médio entre publicação e ínicio de AA'] = pd.to_numeric(juncao_hubspot_somativa_temporal3['Tempo médio entre publicação e ínicio de AA'],errors = 'coerce')
                                juncao_hubspot_somativa_temporal3['Tempo médio entre criação e publicação de AA por questão'] = pd.to_numeric(juncao_hubspot_somativa_temporal3['Tempo médio entre criação e publicação de AA por questão'],errors = 'coerce')
                                juncao_hubspot_somativa_temporal4 = juncao_hubspot_somativa_temporal3.groupby('Semana').mean().reset_index()
                                fig.add_scatter(x = juncao_hubspot_somativa_temporal4['Semana'], y = 100*juncao_hubspot_somativa_temporal4[coluna],mode='lines', name = 'Média '+avaliacao_somativa_temporal_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_somativa_temporal_select_juncao['licenças'][0], line=dict(color="black"))
                                fig.update_layout(title = "Pontuação média por semana")
                                fig.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
                                st.plotly_chart(fig)
                        if coluna in ('Porcentagem de engajamento em AAs','Número de AAs por turma','Média de exercícios de AA por turma','Porcentagem de visualização de relatórios de AA'):
                            beta = st.checkbox('Visualizar resultados por ano escolar de '+coluna+' -> (clique aqui 🖱️) ')
                            if beta == True:
                                juncao_auxiliar_somativa2[coluna] = 100*juncao_auxiliar_somativa2[coluna]
                                fig2 = px.bar(juncao_auxiliar_somativa2, x = juncao_auxiliar_somativa2['grade'], y = juncao_auxiliar_somativa2[coluna], range_y=[0,100], color_discrete_sequence = ['#4a8ae8']*len(juncao_auxiliar_somativa2))
                                fig2.add_scatter(x = juncao_auxiliar_somativa2['grade'], y = 100*juncao_auxiliar_somativa2[coluna+'_x'], name = 'Média Eduqo', line=dict(color="red"))
                                fig2.add_scatter(x = juncao_auxiliar_somativa2['grade'], y = 100*juncao_auxiliar_somativa2[coluna+'_y'], name = 'Média '+avaliacao_somativa_anoescolar_select_juncao['Produto'][0]+' com faixa de licenças '+avaliacao_somativa_anoescolar_select_juncao['licenças'][0], line=dict(color="black"))
                                fig2.update_layout(title = "Pontuação média por ano escolar")
                                fig2.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.30))
                                st.plotly_chart(fig2)
                            st.write('----')

            st.write('---')

            """
                ### 🥳 **Lançamento recente:**

                #### Avaliação Continuada

                #
            """
            """
                ### 📅 **Próximos lançamentos:**

                #### Tarefa de Casa
                #### Reforço/aprofundamento
                #### Ensino Híbrido

                    #
                """
            st.write('---')

            nps = st.selectbox('Em uma escala de 0 a 10, o quanto você acha que esse relatório te ajuda no dia a dia?', ['Nota','0','1','2','3','4','5','6','7','8','9','10'])
            text = st.empty()
            value = ""
            if st.button('Escrever outro feedback / ponto de melhoria'):
                value = " "
            feedback2 = text.text_input("Caso tenha algum feedback e/ou sugestão de melhoria, escreva aqui 😊", value)
            if nps == 'Nota':
                nps = '-1'
            row = [str(datetime.today()),nome,rede_select,grupo_select,gestor_select,produto_select,licenças_select,namespace_select,str(nps),feedback2]
            index = 2
            sheet.insert_row(row, index)
            #st.dataframe(banco_de_dados2)

        else:
            st.warning('🙂 Escolha um namespace para visualizar seus resultados!')

elif senha_preenchida == '':
            pass

elif nome == 'Nome':
        st.warning("Você esqueceu de preencher o seu nome 🙁")

elif senha_preenchida != 'eduqo':
    st.warning("Senha incorreta! Tente de novo, **preste atenção na dica**")


        

