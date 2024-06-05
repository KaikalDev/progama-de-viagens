import pandas as pd

def dataEmDecimal(data):
    partes = data.split('/')
    dia = int(partes[0])
    mes = int(partes[1])
    ano = int(partes[2])
    return dia + mes*30 + ano*365

dataInicio = dataEmDecimal('31/05/2024')
dataFinal = dataEmDecimal('16/06/2024')
lista_filtrada = []

db = pd.read_excel("dados/kaique/dados.xlsx")


db['Data Ida Decimal'] = db['Data Ida'].apply(dataEmDecimal)

filtered_df = db[(db['Data Ida Decimal'] >= dataInicio) & (db['Data Ida Decimal'] <= dataFinal)]

for index, row in filtered_df.iterrows():
    lista_filtrada.append(row.tolist())

print(lista_filtrada)
