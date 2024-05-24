import pandas as pd
import os

df = pd.DataFrame(columns=['ID', 'Destino', 'Data Ida', 'Data Volta', 'Tipo1', 'Tipo2'])
df.to_excel('dados/dados.xlsx')


new_row = {'ID': 2000, 'Destino': 'patos', 'Data Ida': '10/06', 'Data Volta': '10/06', 'Tipo1': 'nacional', 'Tipo2': 'trabalho'}
new_df = pd.read_excel('dados/dados.xlsx')
df = pd.concat([new_row,new_df])

