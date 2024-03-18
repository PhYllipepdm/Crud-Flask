from flask import Flask, url_for , render_template

# inicialização
app = Flask(__name__)


@app.route('/')
def ola_mundo():
    return render_template('index.html')


# execução
if __name__ == '__main__':
    app.run(debug=True)