from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, Email, Regexp

class CadastroForm(FlaskForm):
    nome = StringField("Nome", validators=[
        DataRequired(message="Nome é obrigatório"),
        Length(min=2, max=20)])
    
    sobrenome = StringField('Sobrenome', validators=[
        DataRequired(message="Sobrenome é obrigatório"),
        Length(min=2, max=20)])
    
    login = StringField('Login', validators=[
        DataRequired(message="Login é obrigatório"),
        Length(min=5, max=20)
    ])
    
    email = EmailField('E-mail', validators=[
        DataRequired('Digite um e-mail válido'), 
        Email(message='E-mail inválido')])
    
    senha = PasswordField('Senha', validators=[
        DataRequired('Senha é obrigatório'),
        Length(min=6, message=('Mínimo de 6 caracteres')),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&]).+$', message='Precisa ter letra maiúscula, minúscula, número e caractere especial')])
    
class LoginForm(FlaskForm):
    login = StringField('Login', validators=[
        DataRequired('Digite seu login')
    ])

    senha = PasswordField('Senha', validators=[
        DataRequired('Digite sua senha')
    ])
