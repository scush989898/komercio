<h1 align="center">
  API - Komercio
</h1>


## 💻 Projeto
Aplicação simulando um comércio que faz operações de CRUD entre compradores, vendedores e produtos de varejo.

## 🔨 Implementações

- [X] Cadastro, visualização, deleção e atualização de todas as entidades
- [X] Configurações dos testes e conexão com o banco de dados do teste e banco de produção.
- [X] Docker

## ✨ Tecnologias

- [X] Python
- [X] Django
- [X] Postgres
- [X] SQLite
- [X] Docker / Docker compose


# Instruções:
 

### Crie o ambiente virtual
```
python -m venv venv
```
### Ative o venv
```bash
# linux: 

source venv/bin/activate

# windows: 

.\venv\Scripts\activate

```

### Instale as dependências 
```
pip install -r requirements.txt
```
### Execute as migrações
```
./manage.py migrate
```

### Executando o servidor
```
python manage.py runserver
```

## Documentação da API

[Link da Documentação](https://komerciokenziem5.herokuapp.com/api/docs/) <br>