from behave import given, when, then
from django.urls import reverse
from django.contrib.auth.models import User
from sitevagas.models import Empresa 


@given('que eu sou um visitante não logado')
def step_given_visitante_nao_logado(context):
    context.client.logout()

@when('eu acesso a página de registro de empresa')
def step_when_acesso_registro_empresa(context):
    context.url = reverse('registro-empresa')
    context.client.get(context.url) 

@when('eu preencho o campo "{campo}" com "{valor}"')
def step_when_preencho_campo_registro_empresa(context, campo, valor):
    if campo == "Nome da Empresa":
        context.form_data['nome_empresa'] = valor
    elif campo == "Email":
        context.form_data['email'] = valor
    elif campo == "Senha":
        context.form_data['password'] = valor

    
@when('eu clico no botão "Cadastrar"')
def step_when_clico_cadastrar_empresa(context):
    context.response = context.client.post(context.url, context.form_data, follow=True)


@then('eu devo ser redirecionado para a página inicial (Home)')
def step_then_redirecionado_home_empresa(context):
    home_url = reverse('home') 
    assert context.response.redirect_chain[-1][0] == home_url
    assert context.response.redirect_chain[-1][1] == 200

@then('deve existir um usuário "{email}" no sistema')
def step_then_existe_usuario_empresa(context, email):
    assert User.objects.filter(username=email).exists()

@then('E deve existir um perfil de Empresa chamado "{nome_empresa}"')
def step_then_existe_perfil_empresa(context, nome_empresa):
    assert Empresa.objects.filter(nome_empresa=nome_empresa).exists()