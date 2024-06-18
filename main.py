from flask import Flask, render_template, request, redirect, url_for, session # importa o flask com algumas funções
import pandas as pd # importa o pandas como pd
import os # importa o os

# exigencia do flask
app = Flask(__name__)
app.secret_key = '1235687'

# iniciando principais variaveis
server_started = False
lista = []

def dataEmDecimal(data): # Comverte a data de dd/mm/yyyy para um numero decimal
    partes = data.split('/')
    dia = int(partes[0])
    mes = int(partes[1])
    ano = int(partes[2])
    return dia + mes*30 + ano*365

def VerificaData(data1,data2): # Faz a verificação se data1 é maior que data2
    data1 = dataEmDecimal(data1)
    data2 = dataEmDecimal(data2)
    if data1 < data2:
        return False
    else:
        return True

def arrumaData(data):# Ajusta o modelo de datas do html (yyyy-mm-dd) para dd/mm/yyyy
    partes = data.split('-')
    return '/'.join(reversed(partes))

def verificaArquivo(user):# Cria o arquivo dados no diretorio do usuario, caso não exista
    if not os.path.exists(f'dados/{user}/dados.xlsx'):
        df = pd.DataFrame(columns=['Indice', 'Destino', 'Data Ida', 'Data Volta', 'Tipo1', 'Tipo2', 'Roteiro'])
        df.to_excel(f'dados/{user}/dados.xlsx', index=False)

def adicionaLista(user):# Adicionar todos os dados do usuario na variavel lista
    verificaArquivo(user)
    df = pd.read_excel(f'dados/{user}/dados.xlsx')
    linhaId = list(df['Indice'])
    for id in linhaId:
        item = list(df[df['Indice'] == id].values.flatten())
        lista.append(item)

def limpaLista(lista):# Limpa a variavel lista
    lista.clear()

def new_id(planilha):# Gera um novo ID, pegando o ultimo da planilha e somando mais 1
    value = pd.read_excel(planilha)
    indice = len(value)
    if indice == 0:
        id = indice+1
    else:
        listaID = list(value['Indice'])
        id = listaID[indice-1]+1
    return id

def listaDestinos():# Faz uma lista com todos os destinos adicionados anteriormente
    df = pd.read_excel(f'dados/{session['username']}/dados.xlsx')

    destinos = list(df['Destino'])
    d=[]
    for destino in destinos:
        destino = destino.lower()
        if destino not in d:
            d.append(destino)

    for i in range(len(d)):
        d[i] = d[i].capitalize()
    return d

def CriaDicionario(id):# Cria um dicionario necessario para as funções de edit
    arquivo = f'dados/{session["username"]}/dados.xlsx'
    df = pd.read_excel(arquivo)
    linhaId = df[df['Indice'] == id].values.flatten()
    
    
    destino = linhaId[1]
    data_ida = linhaId[2]
    data_volta = linhaId[3]
    tipo1 = linhaId[4]
    tipo2 = linhaId[5]
    roteiro = linhaId[6]
    
    item = {'id': id, 'destino': destino, 'data_ida': data_ida, 'data_volta': data_volta, 'tipo1': tipo1, 'tipo2': tipo2, 'roteiro':roteiro}
    return item

@app.route('/')
def index(): # Inicia o codigo
    global server_started
    if server_started:
        pass
    else:
        server_started = True
        return redirect(url_for('login'))# se é a primeira vez que o codigo é ligado, obriga o login
    if 'logged_in' not in session or not session['logged_in']: 
        return redirect(url_for('login'))# se não tem registro de login, obriga o login

    destinos = listaDestinos()# Define a lista com todos os destinos 
    return render_template('index.html', lista=lista,destinos=destinos, login=True, usuario=session['username'])
    # Inicia o Index.html com algumas variaveis definidas

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # recolhe os dados imformados no html
        user = request.form.get('usuario').capitalize()
        email = request.form.get('email')
        senha = request.form.get('senha')
        c_senha = request.form.get('c_senha')


        # verifica se as senhas são iguais
        if senha != c_senha:
            return render_template('cadastro.html', comfirmacao = True, usuarioExiste = False)
        
        # Verifica de existe planilha usuarios existe
        if not os.path.exists('dados/usuarios.xlsx'):
            planilha_usuarios = pd.DataFrame(columns=['Indice', 'Usuario', 'Senha', 'Email'])
            planilha_usuarios.to_excel('dados/usuarios.xlsx', index=False)

        df = pd.read_excel('dados/usuarios.xlsx')

        # verifica de usuario ja existe
        lista_usuarios = list(df['Usuario'])
        for usuario in lista_usuarios:
            if usuario.lower() == user.lower():
                return render_template('cadastro.html', usuarioExiste = True, comfirmacao = False)
        
        # adiciona novo usuario a planilha usuarios
        ID = new_id('dados/usuarios.xlsx')
        novaLinha = pd.DataFrame([[ID, user, senha, email]], columns=['Indice', 'Usuario', 'Senha', 'Email'])
        pd.concat([df, novaLinha], ignore_index=True).to_excel('dados/usuarios.xlsx', index=False)
        os.makedirs(f'dados/{user}')
        
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # recolhe os dados imformados no html
        user = request.form.get('usuario')
        senha = request.form.get('senha')

        # fazer uma lista de usuarios e senhas (onde o index do usuario seja igual ao da senha)
        df = pd.read_excel('dados/usuarios.xlsx')
        Usuarios = list(df['Usuario'])
        listaSenha = list(df['Senha'])
        listaUsuarios = []

        for usuario in Usuarios:
            listaUsuarios.append(usuario.lower())
            

        if user.lower() in listaUsuarios: # Verifica se o usuario existe
            # pega o index do usuarios é recolhe a senha correspondente
            posicaoSenha = listaUsuarios.index(user)
            senhaDoUsuario = str(listaSenha[posicaoSenha])
            if senha == senhaDoUsuario: # Verifica se a senha e compativel
                # altera as variaveis de login
                session['logged_in'] = True
                session['username'] = user
                # limpa a lista é preenche com os novos dados 
                limpaLista(lista)
                adicionaLista(user)
                return redirect(url_for('index'))
            else:
                return render_template('login.html', usuarioIncorreto=False, senhaIncorreta=True)
        else:
            return render_template('login.html', senhaIncorreta=False, usuarioIncorreto=True)
        
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():# redefine as variaveis de login, e redireciona para login.html
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/adiciona', methods=['GET', 'POST'])
def adiciona_item():
    if request.method == 'POST':
        # cria um novo id
        ID = new_id(f"dados/{session['username']}/dados.xlsx")
        # recolhe os dados imformados no html
        destino = request.form.get('destino')
        data_ida = arrumaData(request.form.get('data_ida'))
        data_volta = arrumaData(request.form.get('data_volta'))
        roteiro = request.form.get('roteiro')
        tipo1 = request.form.get('interOuNaci')
        tipo2 = request.form.get('trabOuLaz')

        # verifica se as datas estão corretas
        if VerificaData(data_ida,data_volta):
            return render_template('adiciona.html',dataErrada=True)
        
        # adiciona o novo item na planilha de dados
        new_row = pd.DataFrame([[ID, destino, data_ida, data_volta, tipo1, tipo2,roteiro]], columns=['Indice', 'Destino', 'Data Ida', 'Data Volta', 'Tipo1', 'Tipo2','Roteiro'])
        new_df = pd.read_excel(f"dados/{session['username']}/dados.xlsx")
        pd.concat([new_df, new_row], ignore_index=True).to_excel(f"dados/{session['username']}/dados.xlsx", index=False)

        # adiciona o novo item na lista
        lista.append([ID, destino, data_ida, data_volta, tipo1, tipo2, roteiro])

        return redirect(url_for('index'))
    return render_template('adiciona.html')

@app.route('/copy', methods=['POST'])
def copy():
    # Recolhe o id do item selecionado 
    id = request.form.get('id')
    if id is not None:
        # pegar apenas a linha que corresponde ao ID
        id = int(id)
        arquivo = f"dados/{session['username']}/dados.xlsx"
        df = pd.read_excel(arquivo)
        linhaId = df[df['Indice'] == id].values.flatten()
        
        # define o valor das variaveis
        ID = new_id(arquivo)
        destino = linhaId[1]
        data_ida = linhaId[2]
        data_volta = linhaId[3]
        tipo1 = linhaId[4]
        tipo2 = linhaId[5]
        roteiro = linhaId[6]
        
        # Adicionado uma copida na planilha(com id diferente)
        new_row = pd.DataFrame([[ID, destino, data_ida, data_volta, tipo1, tipo2,roteiro]],columns=['Indice', 'Destino', 'Data Ida', 'Data Volta', 'Tipo1', 'Tipo2','Rroteiro'])
        pd.concat([df, new_row], ignore_index=True).to_excel(arquivo, index=False)

        # Adicionado uma copida na lista(com id diferente)
        lista.append([ID, destino, data_ida, data_volta, tipo1, tipo2,roteiro])

        
        return redirect(url_for('index'))
    
    return render_template('index.html')

@app.route('/delet', methods=['POST'])
def delet():
    # Recolhe o id do item selecionado
    id = request.form.get('id')
    if id is not None:
        # pegar apenas a linha que corresponde ao ID
        id = int(id)
        arquivo = f'dados/{session["username"]}/dados.xlsx'
        df = pd.read_excel(arquivo)
        linhaId = df[df['Indice'] == id].values.flatten()
        
        # define o valor das variaveis
        destino = linhaId[1]
        data_ida = linhaId[2]
        data_volta = linhaId[3]
        tipo1 = linhaId[4]
        tipo2 = linhaId[5]
        roteiro = linhaId[6]

        # recolhe o indice do item e deleta a linha
        df = pd.read_excel(arquivo)
        indiceLinha = df[df['Indice'] == id].index
        df = df.drop(indiceLinha)
        df.to_excel(arquivo, index=False)
        
        # deleta da lista
        lista.remove([id, destino, data_ida, data_volta, tipo1, tipo2, roteiro])
        
        return redirect(url_for('index'))
    
    return render_template('index.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    # Recolhe o id do item selecionado
    id = request.form.get('id')
    if id is not None:
        # pegar apenas a linha que corresponde ao ID 
        id = int(id)

        # cria o dicionario
        item = CriaDicionario(id)

        # abrir a tela de edição com as variveis setadas
        return render_template('edit.html',dataErrada=False, item=item)
    
    
    return render_template('index.html')

@app.route('/add_edit', methods=['POST'])
def add_edit():
    if request.method == 'POST':
        # Recolhe o id do item selecionado
        id = request.form.get('id')
        id = int(id)

        # recolhe os dados imformados no html
        destino = request.form.get('destino')
        data_ida = arrumaData(request.form.get('data_ida'))
        data_volta = arrumaData(request.form.get('data_volta'))
        roteiro = request.form.get('roteiro')
        tipo1 = request.form.get('interOuNaci')
        tipo2 = request.form.get('trabOuLaz')
        
        if VerificaData(data_ida,data_volta):
            # cria o dicionario
            item = CriaDicionario(id)
            return render_template('edit.html',dataErrada=True,item=item)

        # Reescrever a linha na planilha
        arquivo = f'dados/{session["username"]}/dados.xlsx'
        df = pd.read_excel(arquivo)
        df.loc[df['Indice'] == id, ['Destino', 'Data Ida', 'Data Volta', 'Tipo1', 'Tipo2', 'Roteiro']] = [destino, data_ida, data_volta, tipo1, tipo2,roteiro]
        df.to_excel(arquivo, index=False)

        # Reescrever a linha na Lista
        for item in lista:
            if item[0] == id:
                item[1] = destino
                item[2] = data_ida
                item[3] = data_volta
                item[4] = tipo1
                item[5] = tipo2
                item[6] = roteiro
        
        return redirect('/')
    return render_template('index.html')

@app.route('/roteiro', methods=['GET','POST'])
def roteiro():
    # Recolhe o id do item selecionado
    id = request.form.get('id')
    if id is not None:
        # Cria o dicionario 
        id = int(id)
        item = CriaDicionario(id)

        # abrir a tela de roteiro com as variveis setadas
        return render_template('roteiro.html', item=item)
    return render_template('index.html')

@app.route('/ordenarFiltrar', methods=['POST'])
def ordenarFiltrar():
    # recolhe os filtros selecionados
    valida_trabOUlaz = request.form.get('trabalhoOuLazer')
    valida_naciOUinternaci = request.form.get('NacionalOuInternacional')
    valida_periodo = request.form.get('Periodo')
    valida_destino = request.form.get('destino')

    if valida_trabOUlaz or valida_naciOUinternaci or valida_periodo or valida_destino:
        # recolhe os dados do html
        trabOUlaz = request.form.get('tipo1')
        naciOUinternaci = request.form.get('tipo2')
        destino = request.form.get('filtro_destino')
        dataInicio = arrumaData(request.form.get('dataInicio'))
        dataFinal = arrumaData(request.form.get('dataFinal'))

        lista_filtrada = []
        # recolhe os dados da planilha, alterando as datas para decimais
        db = pd.read_excel(f"dados/{session['username']}/dados.xlsx")
        db['Data Ida Decimal'] = db['Data Ida'].apply(dataEmDecimal)
        filtered_df = db

        # aplica o filtro por lazer ou trabalho
        if valida_trabOUlaz:
            if trabOUlaz == '1':
                filtered_df = filtered_df[filtered_df['Tipo2'] == 'lazer']
            elif trabOUlaz == '2':
                filtered_df = filtered_df[filtered_df['Tipo2'] == 'trabalho']

        # aplica o filtro por nacional ou internacional
        if valida_naciOUinternaci:
            if naciOUinternaci == '1':
                filtered_df = filtered_df[filtered_df['Tipo1'] == 'nacional']
            elif naciOUinternaci == '2':
                filtered_df = filtered_df[filtered_df['Tipo1'] == 'internacional']

        # aplica o filtro por destino
        if valida_destino:
            filtered_df = filtered_df[filtered_df['Destino'] == destino]

        # aplica o filtro por periodo
        if valida_periodo:
            filtered_df = filtered_df[(filtered_df['Data Ida Decimal'] >= dataEmDecimal(dataInicio)) & (filtered_df['Data Ida Decimal'] <= dataEmDecimal(dataFinal))]

        # aplica o filtro da planilha na lista
        for index, row in filtered_df.iterrows():
            lista_filtrada.append(row.tolist())

        # retorna o index com a lista filtrada
        destinos = listaDestinos()
        return render_template('index.html',destinos=destinos, lista=lista_filtrada, login=True, usuario=session['username'])
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
