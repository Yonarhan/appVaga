Feature: Registro de Nova Empresa
  Como um visitante do site
  Eu quero me registrar como empresa
  Para que eu possa anunciar vagas

  Scenario: Registro de empresa com sucesso
    Dado que eu sou um visitante não logado
    
    Quando eu acesso a página de registro de empresa
    E eu preencho o campo "Nome da Empresa" com "Senior"
    E eu preencho o campo "Email" com "senior@solutions.com"
    E eu preencho o campo "Senha" com "senha1234"
    E eu clico no botão "Cadastrar"
    
    Então eu devo ser redirecionado para a página inicial (Home)
    E deve existir um usuário "senior@solutions.com" no sistema
    E deve existir um perfil de Empresa chamado "senior@solutions.com"