from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('vagas/', views.Vagas.as_view(), name='vagas-lista'),
    
    path('registro/', views.COUE.as_view(), name='registro-escolha'), 
    path('registro/empresa/', views.RegistroEmpresa.as_view(), name='registro-empresa'),
    path('registro/candidato/', views.RegistroCandidato.as_view(), name='registro-candidato'),
    
   
    path('vaga/nova/', views.CriarVaga.as_view(), name='vaga-criar'),
    path('vaga/<int:pk>/', views.InfoVaga.as_view(), name='info-vaga'),
    path('vaga/<int:pk>/editar/', views.EditarVaga.as_view(), name='vaga-editar'),
    path('vaga/<int:pk>/deletar/', views.DeletarVaga.as_view(), name='vaga-deletar'),
    path('vaga/<int:pk>/aplicar/', views.aplicar_vaga, name='vaga-aplicar'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/data/', views.get_dashboard_data, name='dashboard-data'),

]