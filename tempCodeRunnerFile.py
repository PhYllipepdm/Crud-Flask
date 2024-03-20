from flask import Flask, url_for, render_template, request, redirect
import sqlite3

# inicialização
app = Flask(__name__)

@app.route('/')
def index():
    # Conexão com o banco de dados e consulta dos clientes
    with sqlite3.connect('gestao_clientes.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM clientes')
        clientes = cursor.fetchall()
    
    clientes_ativos = obter_clientes_ativos()
    clientes_vencidos = obter_clientes_vencidos()
    
    return render_template('index.html', clientes=clientes, clientes_ativos=clientes_ativos, clientes_vencidos=clientes_vencidos)


@app.route('/adicionar_cliente', methods=['POST'])
def adicionar_cliente():
    # Coletar os dados do formulário
    nome = request.form['nome']
    cpf = request.form['cpf']
    plano = request.form['plano']
    data_vencimento = request.form['data_vencimento']
    status = request.form['status']
    
    # Inserir o novo cliente no banco de dados
    with sqlite3.connect('gestao_clientes.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO clientes (nome, cpf, plano, data_vencimento, status) VALUES (?, ?, ?, ?, ?)",
                       (nome, cpf, plano, data_vencimento, status))
        conexao.commit()

    return redirect('/')

@app.route('/editar_cliente/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        plano = request.form['plano']
        data_vencimento = request.form['data_vencimento']
        status = request.form['status']
        
        with sqlite3.connect('gestao_clientes.db') as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE clientes
                SET nome = ?, cpf = ?, plano = ?, data_vencimento = ?, status = ?
                WHERE id = ?
            """, (nome, cpf, plano, data_vencimento, status, cliente_id))
            conexao.commit()
        
        return redirect('/') 
    else:
        # Consultar o cliente a ser editado e exibir o formulário de edição
        with sqlite3.connect('gestao_clientes.db') as conexao:
            cursor = conexao.cursor()
            cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
            cliente = cursor.fetchone()
        return render_template('editar_cliente.html', cliente=cliente)


@app.route('/excluir_cliente/<int:cliente_id>')
def excluir_cliente(cliente_id):
    # Excluir o cliente do banco de dados
    with sqlite3.connect('gestao_clientes.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conexao.commit()
    
    return redirect('/')



def obter_clientes_ativos():
    with sqlite3.connect('gestao_clientes.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE status = 'ativo'") #Selecionando a quantidade de clientes onde status=ativo
        return cursor.fetchone()[0]


def obter_clientes_vencidos():
    with sqlite3.connect('gestao_clientes.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE status = 'vencido'")
        return cursor.fetchone()[0]
# execução
if __name__ == '__main__':
    app.run(debug=True)
