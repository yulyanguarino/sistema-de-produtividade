# Sistema de Produtividade Operacional

## Descrição

Um sistema web para substituir o controle realizado por planilhas, permitindo registrar as operações de separação e conferência de pedidos, calcular indicadores de produtividade e apresentar os resultados em um dashboard interativo.

O sistema foi desenvolvido para automatizar o rastreamento de operações em ambientes de warehouse/logística, facilitando o acompanhamento de produtividade por colaborador.

## Status

- **Backend**: Funcional ✅
- **Banco de Dados**: PostgreSQL com schema automático ✅
- **Frontend**: A definir (placeholder folder)

## Stack Tecnológico

- **Backend**: Python + FastAPI
- **Banco de Dados**: PostgreSQL
- **ORM**: SQLAlchemy 2.0+
- **Validação**: Pydantic v2
- **Servidor**: Uvicorn

## Estrutura do Projeto

```
Sistema de produtividade/
├── .gitignore
├── README.md
├── backend/
│   ├── main.py                    (FastAPI app)
│   ├── database.py                (SQLAlchemy engine/session + config)
│   ├── models.py                  (ORM models: Colaborador, Operacao)
│   ├── schemas.py                 (Pydantic schemas para validação)
│   ├── services.py                (lógica de negócio)
│   ├── requirements.txt
│   ├── .env.example               (template de variáveis de ambiente)
│   ├── .env                       (local only, não committed)
│   └── routes/
│       ├── colaboradores.py
│       ├── operacoes.py
│       └── dashboard.py
├── frontend/                      (placeholder — stack a definir)
└── database/
    └── schema.sql                 (DDL de referência)
```

## Banco de Dados

### Tabela: `colaboradores`

| Campo | Tipo | Descrição |
|---|---|---|
| id | SERIAL | Identificador único |
| nome | VARCHAR(100) | Nome do colaborador |
| ativo | BOOLEAN | Indica se o colaborador está ativo (default: TRUE) |

### Tabela: `operacoes`

| Campo | Tipo | Descrição |
|---|---|---|
| id | SERIAL | Identificador único |
| data | DATE | Data da operação |
| pedido | VARCHAR(50) | Número do pedido |
| separador_id | INTEGER FK | Colaborador responsável pela separação |
| qtd_itens_separados | INTEGER | Quantidade de itens separados (CHECK >= 0) |
| conferente_id | INTEGER FK | Colaborador responsável pela conferência |
| qtd_itens_conferidos | INTEGER | Quantidade de itens conferidos (CHECK >= 0) |

A tabela `operacoes` é criada automaticamente na inicialização do backend via `SQLAlchemy` (não é necessário rodar scripts SQL manualmente).

## Setup Local

### Pré-requisitos

- Python 3.11+
- PostgreSQL rodando localmente
- pgAdmin (opcional, para visualização/debugging)
- Database `Dash_Estoque` já criado no PostgreSQL (vazio)

### Instalação

1. **Abra o PowerShell e navegue até o diretório do projeto**:
   ```powershell
   cd "c:\Users\YulyanG\Desktop\Sistema de produtividade"
   ```

2. **Crie e ative um virtual environment**:
   ```powershell
   cd backend
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**:
   - Copie `.env.example` para `.env`:
     ```powershell
     copy .env.example .env
     ```
   - Edite `.env` com as credenciais reais do seu PostgreSQL:
     ```env
     DB_HOST=localhost
     DB_PORT=5432
     DB_NAME=Dash_Estoque
     DB_USER=postgres
     DB_PASSWORD=sua_senha_aqui
     ```

5. **Execute o servidor**:
   ```powershell
   uvicorn main:app --reload
   ```

   O servidor estará disponível em `http://127.0.0.1:8000`

6. **Teste a API**:
   - Documentação interativa (Swagger): `http://127.0.0.1:8000/docs`
   - Documentação alternativa (ReDoc): `http://127.0.0.1:8000/redoc`

## API Endpoints

### Colaboradores

- `POST /colaboradores` — Cadastrar novo colaborador
- `GET /colaboradores?ativo=true` — Listar colaboradores (filtro opcional por status)
- `GET /colaboradores/{id}` — Obter um colaborador
- `PUT /colaboradores/{id}` — Editar nome/status de um colaborador
- `PATCH /colaboradores/{id}/status` — Ativar/Inativar colaborador

### Operações

- `POST /operacoes` — Registrar uma operação completa
- `GET /operacoes?dia=2026-07-20&...` — Listar operações com filtros (dia, mês, período, separador, conferente)
- `GET /operacoes/{id}` — Obter uma operação

### Dashboard

- `GET /dashboard?dia=2026-07-20&...` — Obter indicadores + rankings filtrados

Filtros disponíveis (mutuamente exclusivos para data):
- `dia`: data exata (YYYY-MM-DD)
- `mes`: mês (YYYY-MM)
- `periodo_inicio` + `periodo_fim`: range de datas
- `separador_id`: apenas operações de um separador específico
- `conferente_id`: apenas operações de um conferente específico

> **Nota**: `colaboradores_ativos` é um contador global de colaboradores com `ativo=True`, não afetado pelos filtros de data/operações.

## Exemplos de Uso

### 1. Cadastrar um colaborador

```bash
curl -X POST "http://127.0.0.1:8000/colaboradores" \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Silva", "ativo": true}'
```

### 2. Registrar uma operação

```bash
curl -X POST "http://127.0.0.1:8000/operacoes" \
  -H "Content-Type: application/json" \
  -d '{
    "data": "2026-07-20",
    "pedido": "PED-001",
    "separador_id": 1,
    "qtd_itens_separados": 50,
    "conferente_id": 2,
    "qtd_itens_conferidos": 50
  }'
```

### 3. Consultar dashboard

```bash
curl "http://127.0.0.1:8000/dashboard"
```

Com filtro de data:

```bash
curl "http://127.0.0.1:8000/dashboard?mes=2026-07"
```

## Limitações Conhecidas

- **Sem migrations**: A schema é criada automaticamente na primeira inicialização do backend. Alterações futuras à schema requerem intervenção manual ou adoção do Alembic.
- **CORS aberto**: Configuração temporária (`allow_origins=["*"]`) até que o frontend seja definido. Deverá ser restringido à origem do frontend após escolha da stack.
- **Sem autenticação**: Nenhuma camada de segurança/autenticação implementada ainda.
- **Sem rate limiting**: Não há proteção contra abuso de API.

## Convenção de Branches

- `main`: branch de produção — sempre estável, pronto para deploy
- `dev`: branch de desenvolvimento — integrações de features, testes
- `feature/*`: features individuais, abrem PR contra `dev`

## Roadmap

- [ ] Frontend (React, Vue, ou outro — a definir)
- [ ] Autenticação e autorização
- [ ] Migrations com Alembic
- [ ] Testes automatizados
- [ ] Documentação de deploy/produção
- [ ] CI/CD pipeline

## Suporte

Para dúvidas ou issues, consulte a documentação Swagger em `/docs` ou abra um issue no repositório.
