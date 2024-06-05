from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = '1235687'


server_started = True
lista = []

def dataEmDecimal(data):
    partes = data.split('/')
    dia = int(partes[0])
    mes = int(partes[1])
    ano = int(partes[2])
    return dia + mes*30 + ano*365

def VerificaData(data1,data2):
    data1 = dataEmDecimal(data1)
    data2 = dataEmDecimal(data2)
    if data1 < data2:
        return False
    else:
        return True

def arrumaData(data):
    partes = data.split('-')
    return '/'.join(reversed(partes))

def adicionaLista(user):
    verificaArquivo(user)  # Ajuste para verificar o arquivo no diretório do usuário
    df = pd.read_excel(f'dados/{user}/dados.xlsx')  # Leitura do arquivo no diretório do usuário
    linhaId = list(df['Indice'])
    for id in linhaId:
        item = list(df[df['Indice'] == id].values.flatten())
        lista.append(item)

def limpaLista(lista):
    lista.clear()

def new_id(planilha):
    value = pd.read_excel(planilha)
    indice = len(value)
    if indice == 0:
        id = indice+1
    else:
        listaID = list(value['Indice'])
        id = listaID[indice-1]+1
    return id

def verificaArquivo(user):
    if not os.path.exists(f'dados/{user}/dados.xlsx'):
        df = pd.DataFrame(columns=['Indice', 'Destino', 'Data Ida', 'Data Volta', 'Tipo1', 'Tipo2'])
        df.to_excel(f'dados/{user}/dados.xlsx', index=False)

@app.route('/')
def index():
    global server_started
    if server_started:
        server_started = False
        return redirect(url_for('login'))
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    return render_template('index.html', lista=lista, login=True, usuario=session['username'])

@app.route('/adiciona', methods=['GET', 'POST'])
def adiciona_item():
    if request.method == 'POST':
        ID = new_id(f"dados/{session['username']}/dados.xlsx")
        destino = request.form.get('destino')
        data_ida = arrumaData(request.form.get('data_ida'))
        data_volta = arrumaData(request.form.get('data_volta'))
        interOuNaci = request.form.get('interOuNaci')
        tipo1 = ''
        if interOuNaci == 'nacional':
            tipo1 = 'nacional'
        if interOuNaci == 'internacional':
            tipo1 = 'internacional'
        trabOuLaz = request.form.get('trabOuLaz')
        tipo2 = ''
        if trabOuLaz == 'trabalho':
            tipo2 = 'trabalho'
        if trabOuLaz == 'lazer':
            tipo2 = 'lazer'
        if VerificaData(data_ida,data_volta):
            return render_template('adiciona.html',dataErrada=True)
        if destino:
            new_row = pd.DataFrame([[ID, destino, data_ida, data_volta, tipo1, tipo2]], columns=['Indice', 'Destino', 'Data Ida', 'Data Volta', 'Tipo1', 'Tipo2'])
            new_df = pd.read_excel(f"dados/{session['username']}/dados.xlsx")
            pd.concat([new_df, new_row], ignore_index=True).to_excel(f"dados/{session['username']}/dados.xlsx", index=False)
            lista.append([ID, destino, data_ida, data_volta, tipo1, tipo2])

        return redirect(url_for('index'))
    return render_template('adiciona.html')

@app.route('/copy', methods=['POST'])
def copy():
    id = request.form.get('id')
    if id is not None:
        id = int(id)
        arquivo = f"dados/{session['username']}/dados.xlsx"
        
        df = pd.read_excel(arquivo)
        linhaId = df[df['Indice'] == id].values.flatten()
        
        ID = new_id(arquivo)
        destino = linhaId[1]
        data_ida = linhaId[2]
        data_volta = linhaId[3]
        tipo1 = linhaId[4]
        tipo2 = linhaId[5]
        
        new_row = pd.DataFrame([[ID, destino, data_ida, data_volta, tipo1, tipo2]],columns=['Indice', 'Destino', 'Data Ida', 'Data Volta', 'Tipo1', 'Tipo2'])
        new_df = pd.concat([df, new_row], ignore_index=True).to_excel(arquivo, index=False)
        lista.append([ID, destino, data_ida, data_volta, tipo1, tipo2])

        
        return redirect(url_for('index'))
    
    return render_template('index.html')

@app.route('/delet', methods=['POST'])
def delet():
    id = request.form.get('id')
    if id is not None:
        id = int(id)
        arquivo = f'dados/{session["username"]}/dados.xlsx'
        df = pd.read_excel(arquivo)
        linhaId = df[df['Indice'] == id].values.flatten()
        
        destino = linhaId[1]
        data_ida = linhaId[2]
        data_volta = linhaId[3]
        tipo1 = linhaId[4]
        tipo2 = linhaId[5]

        df = pd.read_excel(arquivo)
        indiceLinha = df[df['Indice'] == id].index
        
        df = df.drop(indiceLinha)
        df.to_excel(arquivo, index=False)
        
        try:
            lista.remove([id, destino, data_ida, data_volta, tipo1, tipo2])
        except ValueError:
            pass
        
        return redirect(url_for('index'))
    
    return render_template('index.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    id = request.form.get('id')
    if id is not None:
        id = int(id)
        arquivo = f'dados/{session["username"]}/dados.xlsx'
        
        df = pd.read_excel(arquivo)
        linhaId = df[df['Indice'] == id].values.flatten()
        
        if len(linhaId) == 0:
            return "ID not found", 404
        
        destino = linhaId[1]
        data_ida = linhaId[2]
        data_volta = linhaId[3]
        tipo1 = linhaId[4]
        tipo2 = linhaId[5]
        
        item = {'id': id, 'destino': destino, 'data_ida': data_ida, 'data_volta': data_volta, 'tipo1': tipo1, 'tipo2': tipo2}

        return render_template('edit.html',dataErrada=False, item=item)
    
    return render_template('index.html')

@app.route('/add_edit', methods=['POST'])
def add_edit():
    if request.method == 'POST':
        id = int(request.form.get('id'))
        destino = request.form.get('destino')
        data_ida = arrumaData(request.form.get('data_ida'))
        data_volta = arrumaData(request.form.get('data_volta'))
        interOuNaci = request.form.get('interOuNaci')
        tipo1 = 'nacional' if interOuNaci == 'nacional' else 'internacional'
        trabOuLaz = request.form.get('trabOuLaz')
        tipo2 = 'trabalho' if trabOuLaz == 'trabalho' else 'lazer'
        
        if VerificaData(data_ida,data_volta):
            return render_template('edit.html',dataErrada=True,item=item)

        arquivo = f'dados/{session["username"]}/dados.xlsx'
        df = pd.read_excel(arquivo)
        
        df.loc[df['Indice'] == id, ['Destino', 'Data Ida', 'Data Volta', 'Tipo1', 'Tipo2']] = [destino, data_ida, data_volta, tipo1, tipo2]
        
        df.to_excel(arquivo, index=False)

        for item in lista:
            if item[0] == id:
                item[1] = destino
                item[2] = data_ida
                item[3] = data_volta
                item[4] = tipo1
                item[5] = tipo2
        
        return redirect('/')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('usuario')
        senha = request.form.get('senha')
        df = pd.read_excel('dados/usuarios.xlsx')
        listaUsuarios = list(df['Usuario'])
        listaSenha = list(df['Senha'])
        if user in listaUsuarios:
            posicaoSenha = listaUsuarios.index(user)
            senhaDoUsuario = str(listaSenha[posicaoSenha])
            if senha == senhaDoUsuario:
                session['logged_in'] = True
                session['username'] = user
                # Limpa a lista atual e adiciona os dados do usuário logado
                limpaLista(lista)
                adicionaLista(user)
                return redirect(url_for('index'))
            else:
                return render_template('login.html', usuarioIncorreto=False, senhaIncorreta=True)
        else:
            return render_template('login.html', senhaIncorreta=False, usuarioIncorreto=True)
        
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        user = request.form.get('usuario')
        email = request.form.get('email')
        senha = request.form.get('senha')
        c_senha = request.form.get('c_senha')
        if senha != c_senha:
            return render_template('cadastro.html', comfirmacao = True, usuarioExiste = False)
        if not os.path.exists('dados/usuarios.xlsx'):
            df = pd.DataFrame(columns=['Indice', 'Usuario', 'Senha', 'Email'])
            df.to_excel('dados/usuarios.xlsx', index=False)
        ID = new_id('dados/usuarios.xlsx')
        df = pd.read_excel('dados/usuarios.xlsx')
        if user in list(df['Usuario']):
            return render_template('cadastro.html', usuarioExiste = True, comfirmacao = False)
        novaLinha = pd.DataFrame([[ID, user, senha, email]], columns=['Indice', 'Usuario', 'Senha', 'Email'])
        pd.concat([df, novaLinha], ignore_index=True).to_excel('dados/usuarios.xlsx', index=False)
        os.makedirs(f'dados/{user}')
        
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/ordenarFiltrar', methods=['POST'])
def ordenarFiltrar():
    valida_trabOUlaz = request.form.get('trabalhoOuLazer')
    valida_naciOUinternaci = request.form.get('NacionalOuInternacional')
    valida_periodo = request.form.get('Periodo')

    if valida_trabOUlaz or valida_naciOUinternaci or valida_periodo:
        trabOUlaz = request.form.get('tipo1')
        naciOUinternaci = request.form.get('tipo2')
        dataInicio = arrumaData(request.form.get('dataInicio'))
        dataFinal = arrumaData(request.form.get('dataFinal'))

        lista_filtrada = []
        db = pd.read_excel(f"dados/{session['username']}/dados.xlsx")

        db['Data Ida Decimal'] = db['Data Ida'].apply(dataEmDecimal)

        filtered_df = db

        if valida_trabOUlaz:
            if trabOUlaz == '1':
                filtered_df = filtered_df[filtered_df['Tipo2'] == 'lazer']
            elif trabOUlaz == '2':
                filtered_df = filtered_df[filtered_df['Tipo2'] == 'trabalho']

        if valida_naciOUinternaci:
            if naciOUinternaci == '1':
                filtered_df = filtered_df[filtered_df['Tipo1'] == 'nacional']
            elif naciOUinternaci == '2':
                filtered_df = filtered_df[filtered_df['Tipo1'] == 'internacional']

        if valida_periodo:
            filtered_df = filtered_df[(filtered_df['Data Ida Decimal'] >= dataEmDecimal(dataInicio)) & (filtered_df['Data Ida Decimal'] <= dataEmDecimal(dataFinal))]

        for index, row in filtered_df.iterrows():
            lista_filtrada.append(row.tolist())

        return render_template('index.html', lista=lista_filtrada, login=True, usuario=session['username'])

    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
