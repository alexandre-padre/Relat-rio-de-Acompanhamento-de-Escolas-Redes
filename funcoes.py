import pandas as pd
from datetime import timedelta
from git import Repo

PATH_OF_GIT_REPO = 'https://github.com/alexandre-padre/Relat-rio-de-Acompanhamento-de-Escolas-Redes.git'  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'Testando Push'

def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')    

def quartis(dataframe, coluna):
    """Separar em quartis.
    Args:
        dataframe (pd.DataFrame): dataframe to use
        coluna: A coluna a qual o quartil é calculado
    Returns:
        pd.DataFrame: re-assigned dataframe
    """
    quartil = (dataframe[coluna].max() - dataframe[coluna].min())/4
    maximo = dataframe[coluna].max()
    minimo = dataframe[coluna].min()
    dataframe_aux = dataframe.copy()
    dataframe_aux['Quartil'] = '0º'
    for i in range(len(dataframe[coluna])):
        if (dataframe[coluna][i] >= minimo and dataframe[coluna][i] < quartil + minimo):
            dataframe_aux['Quartil'][i] = '4º'    
        if (dataframe[coluna][i] >= minimo + quartil and dataframe[coluna][i] < 2*quartil + minimo):
            dataframe_aux['Quartil'][i] = '3º'  
        if (dataframe[coluna][i] >= minimo + 2*quartil and dataframe[coluna][i] < 3*quartil + minimo):
            dataframe_aux['Quartil'][i] = '2º'  
        if (dataframe[coluna][i] >= minimo + 3*quartil and dataframe[coluna][i] <= 4*quartil + minimo):
            dataframe_aux['Quartil'][i] = '1º' 
    return dataframe_aux

def destaques_rotina(dataframe):
    """Seleciona os 20 namespaces destaques da rotina.
    Args:
        dataframe (pd.DataFrame): dataframe to use
    Returns:
        pd.DataFrame: re-assigned dataframe
    """
    dataframe_aux = dataframe.drop(columns = ['Quartil']).reset_index(drop = True)
    dataframe_aux2 = dataframe_aux.loc[0:19]
    dataframe_aux2['Medalha'] = ''
    for i in range(20):
        if i == 0:
            dataframe_aux2['Medalha'][i] = '🥇'
        if i == 1:
            dataframe_aux2['Medalha'][i] = '🥈'
        if i == 2:
            dataframe_aux2['Medalha'][i] = '🥉'
        if i > 2:
            dataframe_aux2['Medalha'][i] = '  '   
    dataframe_aux2.set_index('Medalha', drop = True, inplace=True)
    return dataframe_aux2

def visualizacao_resultado_quartil(texto,dataframe):
    """Analisa a escolha de quartil para visualização.
    Args:
        texto: quartil escolhido
        dataframe (pd.DataFrame): dataframe to use
    Returns:
        pd.DataFrame: re-assigned dataframe
    """
    dataframe_aux = dataframe[dataframe['Quartil'] == texto]
    dataframe_aux.set_index('Quartil', inplace=True)
    return dataframe_aux

def inserir_linha(df, linha):
    df = df.append(linha, ignore_index=False)
    df = df.sort_index().reset_index(drop=True)
    return df

def normalizacao_z(df,coluna):
    df[coluna] = (df[coluna] - df[coluna].mean())/df[coluna].std()
    return df

def normalizacao_maxmin(df,coluna):
    df[coluna] = (df[coluna] - df[coluna].min())/(df[coluna].max() - df[coluna].min())
    return df

def normalizacao(df,coluna,inf,sup):
    var_inf = df[coluna].quantile([inf])
    var_sup = df[coluna].quantile([sup])
    for i in range(len(df[coluna])):
        var_aux = df[coluna][i]
        if (var_aux > var_inf[inf] and var_aux < var_sup[sup]):
            df.loc[i,coluna] = (var_aux - var_inf[inf])/(var_sup[sup] - var_inf[inf]) 
        if (var_aux >= var_sup[sup]):
            df.loc[i,coluna] = 1
        if (var_aux <= var_inf[inf]):
            df.loc[i,coluna] = 0
        
    return df

def normalizacao_datetime(df,coluna,inf,sup):
    df[coluna] = pd.to_timedelta(df[coluna])
    var_inf = df[coluna].quantile([inf])
    var_sup = df[coluna].quantile([sup])
    for i in range(len(df[coluna])):
        var_aux = df[coluna][i]
        if (var_aux > var_inf[inf] and var_aux < var_sup[sup]):
            df.loc[i,coluna] = (var_aux - var_inf[inf])/(var_sup[sup] - var_inf[inf]) 
        if (var_aux >= var_sup[sup]):
            df.loc[i,coluna] = 1
        if (var_aux <= var_inf[inf]):
            df.loc[i,coluna] = 0
        
    return df

def normalizacao_datetime_inversa(df,coluna,inf,sup):
    df[coluna] = pd.to_timedelta(df[coluna])
    df2 = df[df[coluna] != timedelta(days = 0)]
    var_inf = df2[coluna].quantile([inf])
    var_sup = df2[coluna].quantile([sup])
    for i in range(len(df[coluna])):
        var_aux = df[coluna][i]
        if var_aux == timedelta(days=0):
            df.loc[i,coluna] = 0
        if (var_aux > var_inf[inf] and var_aux < var_sup[sup]):
            df.loc[i,coluna] = (var_sup[sup] - var_aux)/(var_sup[sup] - var_inf[inf]) 
        if (var_aux >= var_sup[sup]):
            df.loc[i,coluna] = 0
        if (var_aux <= var_inf[inf] and var_aux != timedelta(days=0)):
            df.loc[i,coluna] = 1   
    return df