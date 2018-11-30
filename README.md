
### Instruções / dependências

| Lista de Dependências |
| ------ |
| [Django](https://www.djangoproject.com/) |
| [mock](https://github.com/testing-cabal/mock) |
| [python 3.5](https://www.python.org/) |

Procedimentos para execução do projeto
* Iniciar o ambiente virtual
```sh
$. pipenv shell
```
* Instalar as dependencias:
```sh
$. pipenv install
```

* Aplicar as migracoes
```sh
$. python manage.py migrate
```

* Criar o superuser para acesso ao painel do /admin
```sh
$. python manage.py createsuperuser
```

* Executar o projeto no ambiente local
```sh
$. python manage.py runserver
```

#### O painel administrativo poderá ser acessado no seguinte link
[Django admin](http://localhost:8000)

#### Submissão do arquivo de vendas

Para submeter o arquivo de vendas, é necessário acessar o painel do django admin (como superuser), clicar no modelo *Sales files* e clicar no botão Add (levando a [essa pagina](http://localhost:8000/admin/sales/salesfile/add/)). A página seguinte constitui um formulário para submissão do arquivo de vendas. Quando concluída a submissão, os modelos pertinentes serão devidamente populados.

O valor de *receita total* será apresentada na change_list de Transaction ([essa página](http://localhost:8000/admin/sales/transaction/)).

