from django import forms
from django.contrib.auth.models import User
from .models import Empresa, Candidato, Vaga

class EmpresaForm(forms.ModelForm):
    email = forms.EmailField(required=True, label = 'Email')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label = 'Senha')
    
    class Meta:
        model = Empresa
        fields = ['nome_empresa']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Este email já está sendo utilizado por outra empresa.")
        return email    

    def save(self, commit=True):
        data = self.cleaned_data
        user = User.objects.create_user(username=data['email'],email=data['email'],password=data['password'])

        if commit:
            Empresa.objects.create(user=user,nome_empresa=data['nome_empresa'] )

        return user
        

class CandidatoForm(forms.ModelForm):
        email = forms.EmailField(required=True, label='Email')
        password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    
        class Meta:
            model = Candidato 
            fields = ['nome_candidato', 'pretensao_salarial', 'experiencia', 'ultima_escolaridade']
            
        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(username=email).exists():
                raise forms.ValidationError("Este email já está sendo utilizado por outro usuário.")
                
            return email
            
            
        def save(self, commit=True):
            data = self.cleaned_data
            user=User.objects.create_user(username=data['email'], email=data['email'], password=data['password'])
            
            if commit:
                Candidato.objects.create(user= user, nome_candidato=data['nome_candidato'], experiencia=data['experiencia'], pretensao_salarial=int(data['pretensao_salarial']), ultima_escolaridade=int(data['ultima_escolaridade']))
                
            return user            
       
class VagaForm(forms.ModelForm):
        class Meta:
            model = Vaga
            fields = ['nome', 'faixa_salarial', 'requisitos', 'escolaridade_minima']