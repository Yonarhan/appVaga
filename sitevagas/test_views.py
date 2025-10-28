from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from sitevagas.models import Empresa, Candidato, Vaga 

#teste para ver se o acesso à edição de vagas está restrito ao proprietário da vaga

class VagaOwnershipAccessTest(TestCase):
    
    def setUp(self):
        self.dona_user = User.objects.create_user(username='dono@teste.com', password='password123')
        self.dona_empresa = Empresa.objects.create(user=self.dona_user, nome_empresa='Empresa Proprietaria')

        self.non_dona_nome = User.objects.create_user(username='nao_dono@teste.com', password='password123')
        self.non_dona_empresa = Empresa.objects.create(user=self.non_dona_nome, nome_empresa='Empresa Invasora')
        
        self.candidato_user = User.objects.create_user(username='candidato@teste.com', password='password123')
        Candidato.objects.create(user=self.candidato_user, nome_candidato='Candidato', pretensao_salarial=1, experiencia='teste', ultima_escolaridade=1)

        self.vaga = Vaga.objects.create(empresa=self.dona_empresa, nome='Vaga Protegida', faixa_salarial=3, requisitos='Nenhum', escolaridade_minima=2)
        
        self.editar_url = reverse('vaga-editar', kwargs={'pk': self.vaga.pk})
        self.login_url = reverse('login') 


    def test_acesso_negado_anonimo(self):
        response = self.client.get(self.editar_url)
        self.assertEqual(response.status_code, 302)
        
        expected_redirect_url = f'{self.login_url}?next={self.editar_url}'
        self.assertRedirects(response, expected_redirect_url)


    def test_acesso_negado_nao_proprietario(self):
        
        self.client.login(username='nao_dono@teste.com', password='password123')
        
        response_empresa = self.client.get(self.editar_url)
        self.assertEqual(response_empresa.status_code, 403) 
        self.client.logout() 
        
        self.client.login(username='candidato@teste.com', password='password123')
        
        response_candidato = self.client.get(self.editar_url)
        self.assertEqual(response_candidato.status_code, 403) 

    def test_acesso_permitido_proprietario(self):
        self.client.login(username='dono@teste.com', password='password123')
        
        response = self.client.get(self.editar_url)
        self.assertEqual(response.status_code, 200)