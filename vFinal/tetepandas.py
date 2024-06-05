import pandas as pd

id = int('1')
df = pd.read_excel(f'dados/kaique/dados.xlsx')
linhaId = list(df[df['Indice'] == id].values.flatten())
destino = linhaId[1]
data_ida = linhaId[2]
data_volta = linhaId[3]
tipo1 = linhaId[4]
tipo2 = linhaId[5]

print(destino)