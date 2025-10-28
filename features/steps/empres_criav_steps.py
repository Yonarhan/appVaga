from behave import given, when, then, step
from django.urls import reverse
from django.contrib.auth.models import User
from sitevagas.models import Empresa, Vaga
from django.shortcuts import get_object_or_404
from django.test.client import Client

def get_vaga_by_name(nome_vaga):
    return get_object_or_404(Vaga, nome=nome_vaga)


@given('que existe uma empresa chamada "{nome_empresa}" com senha "{senha}"')
def step_given_cria_empresa_com_senha(context, nome_empresa, senha):
    user = User.objects.create_user(username=nome_empresa, password=senha)
    Empresa.objects.create(user=user, nome_empresa=nome_empresa)
    context.login_credentials = {'username': nome_empresa, 'password': senha}
    
@given('E a empresa "{nome_empresa}" está logada com a senha "{senha}"')
def step_given_empresa_logada_com_senha(context, nome_empresa, senha):
    context.client.login(username=nome_empresa, password=senha)

@when('a empresa cria uma vaga com nome "{nome}" e escolaridade minima {escolaridade:d}')
def step_when_cria_vaga(context, nome, escolaridade):
    url = reverse('criar-vaga')
    vaga_data = {'nome': nome,'faixa_salarial': 3,'requisitos': 'Conhecimento em BDD','escolaridade_minima': escolaridade}
    context.response = context.client.post(url, data=vaga_data, follow=True)

@then('deve existir uma vaga com nome "{nome_vaga}" no banco de dados')
def step_then_existe_vaga(context, nome_vaga):
    assert Vaga.objects.filter(nome=nome_vaga).exists()

@when('a empresa edita a vaga "{nome_antigo}" para "{nome_novo}"')
def step_when_edita_vaga(context, nome_antigo, nome_novo):
    vaga = get_vaga_by_name(nome_antigo)
    url = reverse('editar-vaga', kwargs={'pk': vaga.pk})
    vaga_data = {'nome': nome_novo,'faixa_salarial': vaga.faixa_salarial, 'requisitos': vaga.requisitos,'escolaridade_minima': vaga.escolaridade_minima}
    context.response = context.client.post(url, data=vaga_data, follow=True)

@then('E eu devo ser redirecionado para a página de detalhes da vaga "{nome_vaga}"')
def step_then_redirecionado_info_vaga(context, nome_vaga):
    vaga = get_vaga_by_name(nome_vaga)
    expected_url = reverse('info-vaga', kwargs={'pk': vaga.pk})
    assert context.response.redirect_chain[-1][0] == expected_url

@when('a empresa deleta a vaga "{nome_vaga}"')
def step_when_deleta_vaga(context, nome_vaga):
    vaga = get_vaga_by_name(nome_vaga)
    url = reverse('deletar-vaga', kwargs={'pk': vaga.pk})
    
    context.response = context.client.post(url, follow=True)

@then('Então não deve existir uma vaga com nome "{nome_vaga}" no banco de dados')
def step_then_nao_existe_vaga(context, nome_vaga):
    assert not Vaga.objects.filter(nome=nome_vaga).exists()

@then('E eu devo ser redirecionado para a página inicial (Home)')
def step_then_redirecionado_home_lifecycle(context):
    home_url = reverse('home')
    assert context.response.redirect_chain[-1][0] == home_url
    assert context.response.redirect_chain[-1][1] == 200