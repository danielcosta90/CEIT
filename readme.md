# C.E.I.T. - Controle de Estoque de Informática e Tecnologia

## Sobre o Projeto

O C.E.I.T. é um sistema de controle de estoque desenvolvido para gerenciar produtos, fornecedores e movimentações de entrada e saída. O projeto foi criado com fins acadêmicos, aplicando conceitos de desenvolvimento web, banco de dados e engenharia de software.

## Objetivo

Disponibilizar uma solução simples e eficiente para o gerenciamento de estoque, permitindo o acompanhamento de produtos, movimentações e níveis de estoque em tempo real.

## Funcionalidades

### Categorias
- Cadastro de categorias;
- Consulta de categorias;
- Atualização de categorias;
- Exclusão de categorias.

### Fornecedores
- Cadastro de fornecedores;
- Consulta de fornecedores;
- Atualização de dados;
- Exclusão de registros.

### Produtos
- Cadastro de produtos;
- Consulta de produtos;
- Atualização de informações;
- Exclusão de produtos;
- Controle de quantidade em estoque.

### Movimentações
- Registro de entradas;
- Registro de saídas;
- Registro de reposições;
- Atualização automática do estoque.

### Consultas e Relatórios
- Busca de produtos por nome;
- Consulta de estoque disponível;
- Identificação de produtos com baixo estoque;
- Histórico de movimentações.

## Requisitos para rodar sistema

- Python 3.10 ou superior
- PostgreSQL 14 ou superior
- pip
- Git
- Navegador web

## Tecnologias Utilizadas

### Backend
- Python
- Flask
- SQLAlchemy

### Banco de Dados
- PostgreSQL

### Frontend
- HTML5
- CSS3
- JavaScript

### Ferramentas
- Visual Studio Code
- Git
- GitHub
- Postman

## Ambiente utilizado no desenvolvimento

O projeto foi desenvolvido utilizando:
- Visual Studio Code
- Python
- PostgreSQL

Embora tenha sido desenvolvido no VS Code, o sistema pode ser executado em qualquer ambiente compatível com Python e PostgreSQL.

## Estrutura do Projeto

```text
CEIT/
│
├── app.py
├── models/
├── routes/
├── static/
├── templates/
├── sql/
│   └── ceit.sql
├── README.md
└── requirements.txt
```

## Modelo de Dados

### Categoria
- id
- nome
- descricao

### Fornecedor
- id
- nome
- telefone
- email
- endereco

### Produto
- id
- nome
- categoria
- preco
- quantidade_estoque
- fornecedor_id

### Movimentacao
- id
- tipo_movimento
- quantidade
- data_movimento
- produto_id

## Regras de Negócio

- Todo produto deve estar vinculado a um fornecedor.
- Entradas aumentam automaticamente o estoque.
- Saídas reduzem automaticamente o estoque.
- Reposições aumentam automaticamente o estoque.
- O sistema não permite estoque negativo.
- Produtos com quantidade abaixo do limite definido são considerados com estoque baixo.

## Instalação

### Clone o repositório
```bash
git clone https://github.com/danielcosta90/CEIT.git
```

### Acesse a pasta do projeto
```bash
cd ceit
```

### Instale as dependências
```bash
pip install -r requirements.txt
```

## Configuração do Banco de Dados

O projeto utiliza PostgreSQL como sistema gerenciador de banco de dados.

### Criar o banco de dados
Execute o comando abaixo no PostgreSQL:

```sql
CREATE DATABASE ceit;
```

### Restaurar a estrutura do banco
Após criar o banco, execute o script disponibilizado na pasta `sql` para criar as tabelas, relacionamentos, funções e demais objetos necessários ao funcionamento da aplicação.

!!!! O arquivo `sql/ceit.sql` contém a estrutura completa do banco de dados, incluindo tabelas, relacionamentos, funções, triggers e dados iniciais. !!!!

Exemplo:

```bash
psql -U postgres -d ceit -f sql/ceit.sql
```

### Configurar a conexão
Verifique as configurações de conexão com o PostgreSQL no arquivo da aplicação e ajuste os parâmetros conforme o seu ambiente:

```python
DATABASE_URL = "postgresql://usuario:senha@localhost:5432/ceit"
```
### Execute o projeto
```bash
python app.py
```

ou

```bash
flask run
```

## Endpoints Principais

### Categorias
| Método | Endpoint |
|---------|----------|
| POST | /categorias |
| GET | /categorias |
| GET | /categorias/{id} |
| PUT | /categorias/{id} |
| DELETE | /categorias/{id} |

### Fornecedores
| Método | Endpoint |
|---------|----------|
| POST | /fornecedores |
| GET | /fornecedores |
| GET | /fornecedores/{id} |
| PUT | /fornecedores/{id} |
| DELETE | /fornecedores/{id} |

### Produtos
| Método | Endpoint |
|---------|----------|
| POST | /produtos |
| GET | /produtos |
| GET | /produtos/{id} |
| PUT | /produtos/{id} |
| DELETE | /produtos/{id} |

### Movimentações
| Método | Endpoint |
|---------|----------|
| POST | /movimentacoes |
| GET | /movimentacoes |

## Exemplos de Teste das Requisições

Os testes podem ser realizados pelo Postman, Insomnia ou outra ferramenta de requisições HTTP.

### Categorias

#### Cadastrar categoria
**POST** `/categorias`
```json
{
  "nome": "Periféricos",
  "descricao": "Produtos como mouse, teclado e headset"
}
```

#### Atualizar categoria
**PUT** `/categorias/1`
```json
{
  "nome": "Periféricos e Acessórios",
  "descricao": "Itens utilizados como acessórios de informática"
}
```

---

### Fornecedores

#### Cadastrar fornecedor
**POST** `/fornecedores`
```json
{
  "nome": "Tech Distribuidora",
  "telefone": "(62) 99999-9999",
  "email": "contato@techdistribuidora.com",
  "endereco": "Goiânia - GO"
}
```

#### Atualizar fornecedor
**PUT** `/fornecedores/1`
```json
{
  "nome": "Tech Distribuidora LTDA",
  "telefone": "(62) 98888-8888",
  "email": "comercial@techdistribuidora.com",
  "endereco": "Aparecida de Goiânia - GO"
}
```

---

### Produtos

#### Cadastrar produto
**POST** `/produtos`
```json
{
  "nome": "Mouse Gamer",
  "categoria_id": 1,
  "fornecedor_id": 1,
  "preco": 89.90,
  "quantidade_estoque": 10
}
```

#### Atualizar produto
**PUT** `/produtos/1`
```json
{
  "nome": "Mouse Gamer RGB",
  "categoria_id": 1,
  "fornecedor_id": 1,
  "preco": 99.90,
  "quantidade_estoque": 15
}
```

---

### Movimentações

#### Registrar entrada de estoque
**POST** `/movimentacoes`
```json
{
  "produto_id": 1,
  "tipo_movimento": "entrada",
  "quantidade": 5
}
```

#### Registrar saída de estoque
**POST** `/movimentacoes`
```json
{
  "produto_id": 1,
  "tipo_movimento": "saida",
  "quantidade": 2
}
```

#### Registrar reposição de estoque
**POST** `/movimentacoes`
```json
{
  "produto_id": 1,
  "tipo_movimento": "reposicao",
  "quantidade": 10
}
```

---

### Consultas

#### Listar categorias
**GET** `/categorias`

#### Listar fornecedores
**GET** `/fornecedores`

#### Listar produtos
**GET** `/produtos`

#### Listar movimentações
**GET** `/movimentacoes`

#### Buscar produto por nome
**GET** `/produtos/buscar?nome=mouse`

#### Consultar produtos com estoque baixo
**GET** `/produtos/estoque-baixo`

## Funcionalidades Implementadas

- CRUD completo de fornecedores;
- CRUD completo de produtos;
- Controle de movimentações;
- Atualização automática do estoque;
- Busca de produtos;
- Consulta de estoque baixo;
- Integração entre frontend e backend;
- Banco de dados relacional com PostgreSQL.

## Melhorias Futuras

- Controle de usuários e permissões;
- Dashboard gerencial;
- Relatórios em PDF;
- Exportação para Excel;
- Indicadores e gráficos.

## Equipe

Projeto desenvolvido para fins acadêmicos.

- Daniel S. Costa
   qualquer duvida estou a diposição: 62982845320
- Felipe Carlos D. Machado
- João Gustavo M. de Aguiar
- Guilherme V. Teixeira
- Andre Junior Divino

## Status do Projeto

Projeto funcional e em constante evolução.

## Licença

Este projeto foi desenvolvido exclusivamente para fins acadêmicos e educacionais.