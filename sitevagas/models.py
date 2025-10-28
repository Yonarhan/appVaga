from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

FAIXA_SALARIAL_CHOICES = [
    (1, "Até 1.000"),
    (2, "De 1.000 a 2.000"),
    (3, "De 2.000 a 3.000"),
    (4, "Acima de 3.000"),
]

ESCOLARIDADE_CHOICES = [
    (1, "Ensino Fundamental"),
    (2, "Ensino Médio"),
    (3, "Tecnólogo"),
    (4, "Ensino Superior"),
    (5, "Pós / MBA / Mestrado"),
    (6, "Doutorado"),
]


class Empresa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_empresa = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_empresa
    
class Candidato(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_candidato = models.CharField(max_length=100)
    pretensao_salarial = models.IntegerField(choices=FAIXA_SALARIAL_CHOICES)
    experiencia = models.TextField()
    ultima_escolaridade = models.IntegerField(choices=ESCOLARIDADE_CHOICES)
    

    def __str__(self):
        return self.nome_candidato
    
    def pontuacao_candidato(self, vaga):
        pontuacao = 0

        if self.pretensao_salarial <= vaga.faixa_salarial:
            pontuacao += 1
            
        if self.ultima_escolaridade >= vaga.escolaridade_minima:
            pontuacao += 1
        
        return pontuacao
        
class Vaga(models.Model):
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='vagas')
    nome = models.CharField(max_length=255)
    faixa_salarial = models.IntegerField(choices=FAIXA_SALARIAL_CHOICES)
    requisitos = models.TextField()
    escolaridade_minima = models.IntegerField(choices=ESCOLARIDADE_CHOICES)
    candidatos = models.ManyToManyField(Candidato,through='Candidatura',related_name='vagas_aplicadas',blank=True )
    data_criacao=models.DateTimeField( auto_now_add=True)
   

    def __str__(self):
        return self.nome
    def get_numero_candidatos(self):
        return self.candidaturas_recebidas.count()


class Candidatura(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, related_name='minhas_candidaturas')
    vaga = models.ForeignKey('Vaga', on_delete=models.CASCADE, related_name="candidaturas_recebidas") 
    data_aplicacao = models.DateTimeField(default=timezone.now)
    pontuacao = models.IntegerField(default=0) 

    class Meta:
        unique_together = ('vaga', 'candidato')
        ordering = ['data_aplicacao']
        verbose_name_plural = "Candidaturas"

    def __str__(self):
        return f"{self.candidato.nome_candidato} aplicado para {self.vaga.nome}"