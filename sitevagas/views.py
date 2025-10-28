from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView)
from .models import Vaga, Candidatura
from .forms import EmpresaForm, CandidatoForm, VagaForm
from django.db.models import Count
from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from django.utils import timezone


class is_empresa(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'empresa')
    
class is_candidato(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'candidato')
    
class empresa_dona_da_vaga(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        vaga = self.get_object()
        return vaga.empresa.user == self.request.user
    

class Home(TemplateView):
    template_name = 'sitevagas/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and hasattr(self.request.user, 'empresa'):
            context['is_empresa'] = True
        else:
            context['is_empresa'] = False
        return context
    

class RegistroEmpresa(CreateView):
    form_class = EmpresaForm
    template_name = 'sitevagas/registro_empresa.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'Empresa'
        return context
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
class RegistroCandidato(CreateView):
    form_class = CandidatoForm
    template_name = 'sitevagas/registro_candidato.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'Candidato'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
class COUE(TemplateView):
    template_name = 'sitevagas/COUE.html'

class Vagas(ListView):
    model = Vaga
    template_name = 'sitevagas/vagas_lista.html'
    context_object_name = 'vagas'

    def get_queryset(self):
        
        return Vaga.objects.annotate(num_candidatos=Count('candidatos'))
    
class CriarVaga(is_empresa, CreateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'sitevagas/vagas_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        empresa = self.request.user.empresa
        form.instance.empresa = empresa
        return super().form_valid(form) 
    
class EditarVaga(empresa_dona_da_vaga, UpdateView):
    model = Vaga
    form_class = VagaForm
    template_name = 'sitevagas/vagas_form.html'

    def get_success_url(self):  
        return reverse('info-vaga', kwargs={'pk': self.object.pk})
    

class DeletarVaga(empresa_dona_da_vaga, DeleteView):
    model = Vaga
    template_name = 'sitevagas/deletar.html'
    success_url = reverse_lazy('home')

class InfoVaga(LoginRequiredMixin, DetailView):
    model = Vaga
    template_name = 'sitevagas/info_vaga.html'
    context_object_name = 'vaga'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vaga = self.get_object()
        user = self.request.user

        is_empresa_dona = hasattr(user, 'empresa') and vaga.empresa == user.empresa
        is_candidato_perfil = hasattr(user, 'candidato')
        context['is_empresa_dona'] = is_empresa_dona
        context['is_candidato_perfil'] = is_candidato_perfil

        if is_empresa_dona:
            candidatos = vaga.candidatos.all() 
            candidatos_com_score = []
            
            for candidato in candidatos:
                score = candidato.pontuacao_candidato(vaga) 
                candidato.score_perfil = score 
                candidatos_com_score.append(candidato)
                
            context['candidatos_na_vaga'] = candidatos_com_score
        if is_candidato_perfil:
            context['ja_aplicou'] = vaga.candidatos.filter(pk=user.candidato.pk).exists()
            
        return context
    
@login_required
def aplicar_vaga(request, pk):
    if request.method == 'POST':
        if not hasattr(request.user, 'candidato'):
            return redirect('home') 
        
        vaga = get_object_or_404(Vaga, pk=pk)
        candidato_perfil = request.user.candidato
        vaga.candidatos.add(candidato_perfil)
        
        return redirect('info-vaga', pk=vaga.pk)
    
    return redirect('home')

class DashboardView(is_empresa, TemplateView):
    template_name = 'sitevagas/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Dashboard da empresa:'
        return context

@login_required
def get_dashboard_data(request):
    empresa = request.user.empresa
    ano_agora = timezone.now().year
    
    vagas_mes = Vaga.objects.filter(empresa=empresa, data_criacao__year=ano_agora).annotate( mes=TruncMonth('data_criacao')).values('mes').annotate(total=Count('id') ).order_by('mes')
    candidaturas_mes = Candidatura.objects.filter(vaga__empresa=empresa,data_aplicacao__year=ano_agora).annotate(mes=TruncMonth('data_aplicacao')).values('mes').annotate(total=Count('id')).order_by('mes')
    
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    vagas_data = [0] * 12
    candidaturas_data = [0] * 12
    
    for item in vagas_mes:
        vagas_data[item['mes'].month - 1] = item['total']
        
    for item in candidaturas_mes:
        candidaturas_data[item['mes'].month - 1] = item['total']

    data = {'vagas': {'labels': meses,'data': vagas_data,},'candidaturas': {'labels': meses,'data': candidaturas_data,}}
    return JsonResponse(data)