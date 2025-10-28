from behave import given, when, then
from django.urls import reverse
from django.contrib.auth.models import User
from sitevagas.models import Empresa, Vaga, Candidato, Candidatura


@given('que existe uma empresa com nome "{nome_empresa}"')
def step_given_cria_empresa(context, nome_empresa):
    user = User.objects.create_user(username=nome_empresa, password='temp')
    context.empresa = Empresa.objects.create(user=user, nome_empresa=nome_empresa)
    
@given('que existe uma vaga com titulo "{titulo_vaga}" criada pela empresa "{nome_empresa}"')
def step_given_cria_vaga(context, titulo_vaga, nome_empresa):
    empresa = Empresa.objects.get(nome_empresa=nome_empresa)
    
    context.vaga = Vaga.objects.create(
        empresa=empresa, 
        nome=titulo_vaga,
        faixa_salarial=3,
        requisitos='Conhecimento em Python',
        escolaridade_minima=4
    )

@given('que existe um candidato chamado "{nome}" com email "{email}" e senha "{senha}"')
def step_given_cria_candidato(context, nome, email, senha):
    user = User.objects.create_user(username=email, email=email, password=senha)
    context.candidato = Candidato.objects.create(
        user=user, 
        nome_candidato=nome,
        pretensao_salarial=3,
        experiencia='5 anos',
        ultima_escolaridade=4
    )
    context.candidato_login = {'username': email, 'password': senha} 


@when('o candidato com email "{email}" faz login com a senha "{senha}"')
def step_when_candidato_login(context, email, senha):
    context.client.login(username=email, password=senha)

@when('o candidato acessa a página de detalhes da vaga "{titulo_vaga}"')
def step_when_acessa_vaga(context, titulo_vaga):

    vaga = Vaga.objects.get(nome=titulo_vaga)
    context.vaga_url = reverse('info-vaga', kwargs={'pk': vaga.pk})
    context.response = context.client.get(context.vaga_url)

@when('o candidato aplica para a vaga')
def step_when_aplica_vaga(context):

    vaga_pk = context.vaga.pk
    aplicar_url = reverse('aplicar-vaga', kwargs={'pk': vaga_pk})
    context.response = context.client.post(aplicar_url, follow=True)

@then('o candidato deve ser redirecionado para a página de detalhes da vaga "{titulo_vaga}"')
def step_then_redirecionado_vaga(context, titulo_vaga):
    vaga = Vaga.objects.get(nome=titulo_vaga)
    expected_url = reverse('info-vaga', kwargs={'pk': vaga.pk})
    assert context.response.redirect_chain[-1][0] == expected_url
    assert context.response.redirect_chain[-1][1] == 200 

@then('o número de candidaturas para a vaga "{titulo_vaga}" deve ser {count:d}')
def step_then_verifica_candidaturas(context, titulo_vaga, count):
    vaga = Vaga.objects.get(nome=titulo_vaga)
    assert vaga.candidaturas_recebidas.count() == count