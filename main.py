from flask import Flask, render_template, url_for
from forms import FormPais, FormMarca, FormCat, FormCriacaoConta, FazerLogin
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'carros',
    'raise_on_warnings': True
}

app = Flask(__name__)

app.config['SECRET_KEY'] = '29cecf8afd6176f06bb3f55472d490d1'


@app.route('/', methods=['GET','POST'])
def home():
    form_pais = FormPais()
    form_marca = FormMarca()
    form_cat = FormCat()
    return render_template('home.html',form_pais=form_pais, form_marca=form_marca, form_cat=form_cat)

@app.route('/disponiveis')
def disponiveis():
    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()

    consulta_sql = f"SELECT nome, modelo, ano_prod, preco FROM carro JOIN marca ON id_marca = fk_id_marca LEFT JOIN compra ON id = fk_carro_id WHERE data_oferta IS NULL;"

    cursor.execute(consulta_sql)
    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()
    return render_template('disponiveis.html', resultados=resultados)


@app.route('/quilometragem')
def quilometragem():
    grafico_ = url_for('static', filename='./images/km_por_marca.png')
    return render_template('quilometragem.html', grafico=grafico_)

@app.route('/preco-marca')
def preco():
    grafico = url_for('static', filename='./images/media_por_marca.png')
    return render_template('preco.html', grafico=grafico)

@app.route('/consulta-marca', methods=['GET','POST'])
def consulta1():
    form = FormMarca()
    # Processar os dados do formulário aqui
    brand = form.marca.data


    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()

    consulta_sql = "SELECT modelo, ano_prod, preco FROM carro JOIN (SELECT id_marca FROM marca WHERE nome = %s) AS name ON id_marca = fk_id_marca;"

    cursor.execute(consulta_sql, (brand,))
    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()
    return render_template('consulta-marca.html', resultados=resultados, marca=brand)


@app.route('/consulta-pais',  methods=['GET','POST'])
def consulta2():
    form = FormPais()
    # Processar os dados do formulário aqui
    pais = form.pais.data

    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()

    consulta_sql = "SELECT nome, modelo, ano_prod, preco FROM carro JOIN (SELECT id_marca, nome FROM marca WHERE pais_sede = %s)  AS pais ON id_marca = fk_id_marca;"

    cursor.execute(consulta_sql, (pais,))
    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()
    return render_template('consulta-pais.html', resultados=resultados, pais = pais)

@app.route('/quantidade-pais',  methods=['GET','POST'])
def qtd_pais():
    form = FormCat()
    # Processar os dados do formulário aqui
    cat= form.cat.data

    conexao = mysql.connector.connect(**db_config)
    cursor = conexao.cursor()

    consulta_sql = "SELECT pais_sede, count(id) FROM carro JOIN marca ON id_marca = fk_id_marca  JOIN categoria ON id_cat = fk_id_cat WHERE categoria.nome = %s GROUP BY pais_sede;"

    cursor.execute(consulta_sql, (cat,))
    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template('quantidade-pais.html', resultados=resultados, cat=cat)


@app.route('/venda-pais')
def vendas_pais():
    grafico = url_for('static', filename='./images/vendas x pais.png')
    return render_template('venda-pais.html', grafico=grafico)


@app.route('/login',methods=['GET','POST'])
def login():
    form_login = FazerLogin()
    form_criar_conta = FormCriacaoConta()
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)

if __name__ == '__main__':
    app.run(debug=True)

