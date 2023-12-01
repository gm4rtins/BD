from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class FormPais(FlaskForm):
    pais = StringField("País")
    submit_pais = SubmitField('Buscar')


class FormMarca(FlaskForm):
    marca = StringField('Marca')
    submit_marca = SubmitField('Buscar')


class FormCat(FlaskForm):
    cat = StringField('Categoria')
    submit_cat = SubmitField('Buscar')


class FormCriacaoConta(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('e-mail', validators=[DataRequired(), Email()])
    data_nasc = DateField('Data de Nascimento', validators=[DataRequired()])
    cpf = StringField('CPF', validators = [DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit_criar_conta = SubmitField('Criar Conta')

class FazerLogin(FlaskForm):
    email = StringField('e-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit_login = SubmitField('Login')





