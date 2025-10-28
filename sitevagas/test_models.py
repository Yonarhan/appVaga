from django.test import TestCase
from django.contrib.auth.models import User
from sitevagas.models import Candidato, Vaga, Empresa, Candidatura

#teste da pontuação do candidato para uma vaga específica

class CandidatoPontuacaoTest(TestCase):
    def setUp(self):

        empresa_user = User.objects.create_user(username='empresa_teste', password='123')
        candidato_user = User.objects.create_user(username='candidato_teste', password='123')
        
        self.empresa = Empresa.objects.create(user=empresa_user, nome_empresa='Tech Corp')
        self.candidato_alice = Candidato.objects.create(user=candidato_user, nome_candidato='Alice Silva', pretensao_salarial=2, experiencia='Dev', ultima_escolaridade=4)

    def test_pontuacao_maxima(self):
        vaga_facil = Vaga.objects.create(empresa=self.empresa,nome='Vaga Fácil',faixa_salarial=3,requisitos='Nenhum',escolaridade_minima=2)
        
        pontuacao = self.candidato_alice.pontuacao_candidato(vaga_facil)
        self.assertEqual(pontuacao, 2)


    def test_pontuacao_minima(self):
        vaga_dificil = Vaga.objects.create(empresa=self.empresa,nome='Vaga Difícil',faixa_salarial=1,requisitos='Mestrado',escolaridade_minima=5)
        pontuacao = self.candidato_alice.pontuacao_candidato(vaga_dificil)
        self.assertEqual(pontuacao, 0)
        

    def test_pontuacao_parcial_salario(self):
        vaga_salario_ok = Vaga.objects.create(empresa=self.empresa,nome='Vaga Salário OK',faixa_salarial=3,requisitos='Fundamental',escolaridade_minima=5)
        pontuacao = self.candidato_alice.pontuacao_candidato(vaga_salario_ok)
        self.assertEqual(pontuacao, 1)

    def test_pontuacao_parcial_escolaridade(self):
        vaga_escolaridade_ok = Vaga.objects.create(empresa=self.empresa,nome='Vaga Escolaridade OK',faixa_salarial=1,requisitos='Superior',escolaridade_minima=3)
        pontuacao = self.candidato_alice.pontuacao_candidato(vaga_escolaridade_ok)
        self.assertEqual(pontuacao, 1)