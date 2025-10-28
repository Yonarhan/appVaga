Feature: Candidatura em Vagas
  Como um Candidato
  Eu quero me candidatar a uma vaga
  Para que meu perfil seja considerado pela empresa

  Scenario: Candidato aplica com sucesso a uma vaga
    Dado que existe uma empresa com nome "Senior"
    E que existe uma vaga com titulo "Desenvolvedor Django/Python" criada pela empresa "Senior"
    E que existe um candidato chamado "Yonarhan" com email "Yonarhan@gmail.com" e senha "senha456"
    
    Quando o candidato com email "Yonarhan@gmail.com" faz login com a senha "senha456"
    E o candidato acessa a página de detalhes da vaga "Desenvolvedor Django/Python"
    E o candidato aplica para a vaga
    
    Então o candidato deve ser redirecionado para a página de detalhes da vaga "Desenvolvedor Django/Python"
    E o número de candidaturas para a vaga "Desenvolvedor Django/Python" deve ser 1

    """candidato aplica para a vaga apenas uma vez (e é contratado)"""