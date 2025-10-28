Feature: Registro de Novo Candidato
  Como um visitante do site
  Eu quero me registrar como candidato
  Para que eu possa aplicar para as vagas

  Scenario: Registro de candidato com todos os dados válidos
    Dado que eu sou um visitante não logado
    
    Quando eu acesso a página de registro de candidato
    E eu preencho o campo "Nome Completo" com "Maria Souza"
    E eu preencho o campo "Email" com "maria@teste.com"
    E eu preencho o campo "Senha" com "senha123"
    E eu preencho o campo "Pretensão Salarial" com "3"
    E eu preencho o campo "Experiência" com "Desenvolvedor Backend 5 anos"
    E eu preencho o campo "Escolaridade" com "4"
    E eu clico no botão "Cadastrar"
    
    Então eu devo ser redirecionado para a página inicial (Home)
    E deve existir um usuário "maria@teste.com" no sistema
    E deve existir um perfil de Candidato associado ao usuário "maria@teste.com"