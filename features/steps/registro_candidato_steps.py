from behave import given, when, then
from django.urls import reverse
from django.contrib.auth.models import User
from sitevagas.models import Candidato
from django.test.client import Client



@given('que eu sou um visitante não logado')
def step_given_visitante_nao_logado(context):
    context.client.logout()

@when('eu acesso a página de registro de candidato')
def step_when_acesso_registro(context):
    context.url = reverse('registro-candidato')
    context.response = context.client.get(context.url)

@when('eu preencho o campo "{campo}" com "{valor}"')
def step_when_preencho_campo(context, campo, valor):
    
    if campo == "Nome Completo":
        context.form_data['nome_candidato'] = valor
    elif campo == "Email":
        context.form_data['email'] = valor
    elif campo == "Senha":
        context.form_data['password'] = valor
    elif campo == "Pretensão Salarial":
        context.form_data['pretensao_salarial'] = valor
    elif campo == "Experiência":
        context.form_data['experiencia'] = valor
    elif campo == "Escolaridade":
        context.form_data['ultima_escolaridade'] = valor

@when('eu clico no botão "Cadastrar"')
def step_when_clico_cadastrar(context):
    context.response = context.client.post(context.url, context.form_data, follow=True)

@then('eu devo ser redirecionado para a página inicial (Home)')
def step_then_redirecionado_home(context):
    home_url = reverse('home') 
    
    assert context.response.redirect_chain[-1][0] == home_url
    assert context.response.redirect_chain[-1][1] == 200

@then('deve existir um usuário "{email}" no sistema')
def step_then_existe_usuario(context, email):
    assert User.objects.filter(email=email).exists()

@then('deve existir um perfil de Candidato associado ao usuário "{email}"')
def step_then_existe_perfil_candidato(context, email):
    user = User.objects.get(email=email)
    assert hasattr(user, 'candidato')
    assert Candidato.objects.filter(user=user).exists()