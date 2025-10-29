# Configuração do Projeto

Este é um projeto desenvolvido utilizando Django e Visual Studio Code (VSCode) como editor de código. Siga os passos abaixo para configurar o ambiente de desenvolvimento:

## Passo 1: Clonar o Repositório

Clone o repositório do projeto para o seu computador usando o comando:
~~~
git clone https://github.com/Yonarhan/appVaga
~~~

## Passo 2: Configurar o Ambiente Virtual

Dentro da pasta do projeto, abra um terminal e crie um ambiente virtual utilizando o comando:
~~~
python -m venv nome-da-venv
~~~

## Passo 3: Ativar o Ambiente Virtual

Ative o ambiente virtual utilizando o comando apropriado para o seu sistema operacional:

**Windows:**
~~~
nome-da-venv\Scripts\activate
~~~

**Linux / macOS:**
~~~
source nome-da-venv/bin/activate
~~~

## Passo 4: Instalar Dependências

Com o ambiente virtual ativado, instale as dependências do projeto, incluindo o Django, utilizando o comando:
~~~
pip install -r requirements.txt
~~~

## Passo 5: Entrar no diretório do projeto
~~~
cd nome-da-pasta-do-projeto
~~~

## Passo 6: Criar o banco local da aplicação
~~~
py manage.py makemigrations 
~~~
~~~
py manage.py migrate 
~~~

## Passo 7: Rodar o Servidor

Inicie o servidor de desenvolvimento do Django com o comando:
~~~
python manage.py runserver
~~~

## Passo 8: Acessar o Projeto

Abra o navegador web e acesse o seguinte endereço:
~~~
http://127.0.0.1:8000/
~~~

Agora você estará executando o projeto localmente no seu navegador.

**Observação:** 
Lembre-se de substituir `"nome-da-venv"` pelo nome desejado para a sua virtual environment (ambiente virtual) ao longo do tutorial.
