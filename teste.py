from flask import Flask, render_template, request, redirect, url_for
import random


app = Flask(__name__)

# Dicionário para armazenar os itens
key = {}
chave_id = random.randint(1000, 9999)




@app.route('/add', methods=['POST'])
def add_item():
    destino = request.form.get('destino')
    data_ida = request.form.get('data_ida')
    data_volta = request.form.get('data_volta')
    nacional = request.form.get('nacional')
    internacional = request.form.get('internacional')
    if nacional:
        tipo1 = '<i><img src="/icon/geo-alt-fill.svg" alt="Nacional" title="Nacional"></i>'
    if internacional:
        tipo1 = '<i><img src="/icon/globe-americas.svg" alt="Internacional" title="Internacional"></i>'
    trabalho = request.form.get('trabalho')
    lazer = request.form.get('lazer')
    if trabalho:
        tipo2 = '<i><img src="/icon/briefcase-fill.svg" alt="Trabalho" title="Trabalho"></i>'
    if lazer:
        tipo2 = '<i><img src="/icon/sunglasses.svg" alt="Lazer" title="Lazer"></i>'
    if destino:
        
        add_detiny(chave_id, destino)
    
        # key.update({destino, data_ida, data_volta, tipo1, tipo2})
    return redirect(url_for('index'))

# Lista para armazenar objetos Usuario
usuarios = {}

def add_detiny(id, destiny):
    usuarios.append(Usuario(id, destiny))
    for usuario in usuarios:
        usuario.exibir_informacoes()
        print()


@app.route('/')
def index():
    lista = key
    return render_template('index.html', chaves=lista)

if __name__ == '__main__':
    app.run(debug=True)
