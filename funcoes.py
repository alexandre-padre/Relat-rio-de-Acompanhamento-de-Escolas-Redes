import pandas as pd

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