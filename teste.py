import pandas as pd

lista = []

df = pd.read_excel(f'dados/kaique/dados.xlsx')  # Leitura do arquivo no diretório do usuário
linhaId = list(df['Indice'])
for id in linhaId:
    item = list(df[df['Indice'] == id].values.flatten())
    lista.append(item)

print(lista)