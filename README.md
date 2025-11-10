# 🎓 Assistente Educacional IA

Sistema completo de assistente educacional com FastAPI, Docker e Claude AI.

## 🚀 Características

- **Backend FastAPI**: API REST moderna e performática
- **Frontend Responsivo**: Interface intuitiva e elegante
- **Docker Multi-stage**: Build otimizado e seguro
- **Claude AI**: Assistente inteligente com modelos avançados
- **Múltiplas Disciplinas**: Suporte para 10+ matérias
- **Histórico de Conversação**: Contexto mantido durante a sessão

## 📋 Pré-requisitos

- Docker e Docker Compose
- Chave API da Anthropic (Claude)
- Git

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd assistente-educacional
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave API:

```env
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 3. Estrutura de arquivos

```
assistente-educacional/
├── main.py                 # Backend FastAPI
├── requirements.txt        # Dependências Python
├── Dockerfile             # Build multi-stage
├── docker-compose.yml     # Orquestração
├── nginx.conf             # Configuração Nginx
├── .env                   # Variáveis de ambiente
├── .env.example          # Exemplo de configuração
└── frontend/
    └── index.html        # Interface web
```

### 4. Construir e executar

```bash
# Construir imagens
docker-compose build

# Iniciar serviços
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### 5. Acessar a aplicação

- **Frontend**: http://localhost
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📡 API Endpoints

### GET /health
Verifica saúde da API

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-10T10:30:00"
}
```

### GET /api/subjects
Lista disciplinas disponíveis

**Response:**
```json
{
  "subjects": [
    {
      "id": "Cloud Comp",
      "name": "Fundamentos de Computação em Nuvem",
      "icon": "☁️"
    }
  ]
}
```

### POST /api/chat
Envia pergunta ao assistente

**Request:**
```json
{
  "subject": "Fundamentos de Computação em Nuvem",
  "question": "Explique o conceito de virtualização e sua importância para a computação em nuvem.",
  "context": "Estou estudando infraestrutura de cloud",
  "history": []
}
```

**Response:**
```json
{
  "answer": "A virtualização é a tecnologia que permite criar múltiplos ambientes virtuais independentes em um único hardware físico. Ela é fundamental para a computação em nuvem, pois possibilita o uso eficiente dos recursos, a escalabilidade e o isolamento entre aplicações.",
  "subject": "Fundamentos de Computação em Nuvem",
  "timestamp": "2025-11-10T10:30:00"
}
```

## 🐳 Comandos Docker

```bash
# Parar serviços
docker-compose down

# Reconstruir após mudanças
docker-compose up -d --build

# Ver logs de um serviço específico
docker-compose logs -f api

# Remover tudo (incluindo volumes)
docker-compose down -v

# Verificar status
docker-compose ps
```

## 🔒 Segurança

- ✅ Multi-stage build reduz tamanho da imagem
- ✅ Usuário não-root no container
- ✅ Health checks configurados
- ✅ CORS configurado adequadamente
- ✅ Variáveis de ambiente para secrets
- ✅ Nginx como reverse proxy

## 🎯 Disciplinas Suportadas

## 📊 Monitoramento

### Health Check
```bash
curl http://localhost:8000/health
```

### Logs
```bash
# Todos os serviços
docker-compose logs -f

# Apenas API
docker-compose logs -f api

# Apenas Frontend
docker-compose logs -f frontend
```

## 🛠️ Desenvolvimento

### Executar localmente (sem Docker)

```bash
# Instalar dependências
pip install -r requirements.txt
pip install -r requirements-test.txt

# Configurar variável de ambiente
export ANTHROPIC_API_KEY=your_key

# Executar API
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Abrir frontend/index.html no navegador
```

## 🧪 Testes

O projeto possui cobertura completa de testes unitários e de integração.

### Executar Testes

```bash
# Todos os testes
make test

# Testes com cobertura
make test-cov

# Apenas testes unitários
make test-unit

# Apenas testes de integração
make test-integration

# Ver relatório de cobertura
make coverage-report
```

### Testes Manuais da API

```bash
# Testar endpoint de health
curl http://localhost:8000/health

# Testar disciplinas
curl http://localhost:8000/api/subjects

# Testar chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type" application/json" \
  -d '{
    "subject": "Matemática Computacional",
    "question": "O que é um número primo?"
  }'
```

### Estrutura de Testes

```
tests/
├── conftest.py           # Fixtures compartilhadas
└── test_main.py         # Testes principais
    ├── TestHealthEndpoints
    ├── TestSubjectsEndpoint
    ├── TestChatEndpoint
    ├── TestModels
    ├── TestCORS
    ├── TestIntegration
    ├── TestPerformance
    └── TestErrorHandling
```

### Cobertura de Testes

- ✅ Endpoints de health check
- ✅ Listagem de disciplinas
- ✅ Chat com IA (com mocks)
- ✅ Validação de modelos Pydantic
- ✅ Tratamento de erros
- ✅ CORS
- ✅ Performance básica
- ✅ Integração completa

Meta de cobertura: **80%+**

## 🔄 CI/CD

Pipeline completo de integração e entrega contínua implementado.

### GitHub Actions

O projeto inclui pipeline automatizado com:

1. **Testes**: Executados em Python 3.9, 3.10 e 3.11
2. **Linting**: Flake8, Black e MyPy
3. **Docker Build**: Validação de imagens
4. **Security**: Varredura de vulnerabilidades
5. **Coverage**: Upload para Codecov

### Comandos Make

```bash
# Ver todos os comandos
make help

# Verificações completas (CI local)
make check

# Build e deploy
make docker-build
make docker-up

# Ver logs
make docker-logs

# Limpeza
make clean
```

### Pipeline Local

```bash
# Simular pipeline CI completo
make ci

# Apenas testes
make test

# Qualidade de código
make lint

# Build Docker
make docker-build
```

## 📝 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `ANTHROPIC_API_KEY` | Chave API Claude | **Obrigatório** |
| `ENVIRONMENT` | Ambiente (dev/prod) | `production` |
| `API_HOST` | Host da API | `0.0.0.0` |
| `API_PORT` | Porta da API | `8000` |
| `API_WORKERS` | Workers Uvicorn | `2` |

## 🐛 Troubleshooting

### API não responde
```bash
# Verificar logs
docker-compose logs api

# Reiniciar serviço
docker-compose restart api
```

### Frontend não carrega
```bash
# Verificar Nginx
docker-compose logs frontend

# Testar API diretamente
curl http://localhost:8000/health
```

### Erro de API Key
```bash
# Verificar variável de ambiente
docker-compose exec api printenv | grep ANTHROPIC
```

## 📚 Recursos

- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 📄 Licença

MIT License
