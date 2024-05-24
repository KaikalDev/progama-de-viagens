from flask import Flask, render_template, request, redirect, url_for
import random
import pandas as pd

df = pd.DataFrame(columns=['ID', 'Destino', 'Data Ida', 'Data Volta', 'Tipo1', 'Tipo2'])
df.to_excel('dados/dados.xlsx')

app = Flask(__name__)

# Dictionary to store items
chaves = {}
chave_id = random.randint(1000, 9999)

@app.route('/add', methods=['POST'])
def add_item():
    global chave_id  # to modify the global chave_id
    destino = request.form.get('destino')
    data_ida = request.form.get('data_ida')
    data_volta = request.form.get('data_volta')
    nacional = request.form.get('nacional')
    internacional = request.form.get('internacional')
    tipo1 = ''
    if nacional:
        tipo1 = '<i><img src="/static/icon/geo-alt-fill.svg" alt="Nacional" title="Nacional"></i>'
    if internacional:
        tipo1 = '<i><img src="/static/icon/globe-americas.svg" alt="Internacional" title="Internacional"></i>'
    trabalho = request.form.get('trabalho')
    lazer = request.form.get('lazer')
    tipo2 = ''
    if trabalho:
        tipo2 = '<i><img src="/static/icon/briefcase-fill.svg" alt="Trabalho" title="Trabalho"></i>'
    if lazer:
        tipo2 = '<i><img src="/static/icon/sunglasses.svg" alt="Lazer" title="Lazer"></i>'
    if destino:
        new_row = {'ID': chave_id, 'Destino': destino, 'Data Ida': data_ida, 'Data Volta': data_volta, 'Tipo1': tipo1, 'Tipo2': tipo2}
        new_df = pd.read_excel('dados/dados.xlsx')
        df = df.apply(new_row)
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', chaves=chaves)

if __name__ == '__main__':
    app.run(debug=True)
