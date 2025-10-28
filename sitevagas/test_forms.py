from django.test import TestCase
from django.contrib.auth.models import User
from sitevagas.forms import EmpresaForm, CandidatoForm

#testando a duplicidade de email nos formulários de registro

class UnicidadeEmailFormTest(TestCase):

    def setUp(self):
        self.email_duplicado = 'teste@existente.com'
        self.senha_padrao = 'senha123'
        
        User.objects.create_user(
            username=self.email_duplicado, 
            email=self.email_duplicado, 
            password=self.senha_padrao
        )
        
        self.dados_duplicados = {'email': self.email_duplicado,'password': self.senha_padrao,'nome_candidato': 'Nome de Teste', 'pretensao_salarial': 1, 'experiencia': 'Nada', 'ultima_escolaridade': 1}
    
    def test_candidato_form_email_duplicado_falha(self):
        form = CandidatoForm(data=self.dados_duplicados)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('Este email já está sendo utilizado por outro usuário.', form.errors['email'])


    def test_empresa_form_email_duplicado_falha(self):
        dados_empresa_duplicada = {'email': self.email_duplicado,'password': self.senha_padrao, 'nome_empresa': 'Nova Empresa'}
        form = EmpresaForm(data=dados_empresa_duplicada)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)