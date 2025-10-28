Feature: Ciclo de Vida Completo da Vaga (CRUD)
  Como uma empresa proprietaria de vagas 
  Eu quero gerenciar minhas vagas
  Para que eu possa criar, atualizar e remover minhas vagas

  Scenario: Empresa cria, edita e exclui sua própria vaga com sucesso
    Dado que existe uma empresa chamada "Senior" com senha "testpass123"
    E a empresa "Senior" está logada com a senha "testpass123"
    
    Quando a empresa cria uma vaga com nome "Desenvolvedor Junior" e escolaridade minima 2
    Então deve existir uma vaga com nome "Desenvolvedor Junior" no banco de dados
    E eu devo ser redirecionado para a página inicial (Home)
    
    Quando a empresa edita a vaga "Desenvolvedor Junior" para "Desenvolvedor Pleno"
    Então deve existir uma vaga com nome "Desenvolvedor Pleno" no banco de dados
    E eu devo ser redirecionado para a página de detalhes da vaga "Desenvolvedor Pleno"
    
    Quando a empresa deleta a vaga "Desenvolvedor Pleno"
    Então não deve existir uma vaga com nome "Desenvolvedor Pleno" no banco de dados
    E eu devo ser redirecionado para a página inicial (Home)