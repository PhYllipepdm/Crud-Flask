from flask import Flask, url_for , render_template, request
import sqlite3

# inicialização
app = Flask(__name__)

#Conexão com o banco de Dados
conexao = sqlite3.connect('gestao_clientes.db')
cursor = conexao.cursor()

#Criação da tabela 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL,
               cpf TEXT UNIQUE,
               plano TEXT,
               data_vencimento DATE,
               status TEXT
    )

""")

conexao.commit()#Salvar
conexao.close()#Fechar

@app.route('/')
def index():
    conexao = sqlite3.connect('gestao_clientes.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conexao.close()
    return render_template('index.html', clientes=clientes)


@app.route('/adicionar_cliente', methods=['POST'])
def adicionar_cliente():
    print(request.form)
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        plano = request.form['plano']
        data_vencimento = request.form['data_vencimento']
        status = request.form['status']

        cursor.execute("INSERT INTO clientes (nome, cpf, plano, data_vencimento, status) VALUES(?,?,?,?,?)",
                      (nome, cpf, plano, data_vencimento, status) )
        conexao.commit()
        return 'Cliente adicionado com sucesso!'

# execução
if __name__ == '__main__':
    app.run(debug=True)