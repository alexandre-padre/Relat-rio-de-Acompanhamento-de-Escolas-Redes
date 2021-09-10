import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Banco de Dados').sheet1

banco_de_dados = sheet.get_all_records()

row = ['Mateus','acessoboqueirao']
index = 2
sheet.update_cell(1,2,"Namespace")
sheet.insert_row(row, index)
sheet = client.open('Banco de Dados').sheet1

banco_de_dados = sheet.get_all_records()
st.dataframe(banco_de_dados)

