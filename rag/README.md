# App RAG - Sistema de Documentos com IA

## 📁 Estrutura do App

```
rag/
├── models.py          # Modelo de dados (Document)
├── services.py        # Lógica do RAG (upload S3, embedding, Qdrant)
├── views.py           # Views/Controllers (upload, busca)
├── urls.py            # Rotas do app
├── admin.py           # Configuração do Django Admin
└── templates/rag/
    └── index.html     # Interface web
```

## 🎯 Como Funciona

### 1. **models.py** - Banco de Dados
Armazena informações dos documentos processados:
- source (nome do arquivo)
- s3_url (link do S3)
- category, author, date, etc.

### 2. **services.py** - Lógica Principal
Classe `RAGService` que gerencia:
- **upload_pdf_to_s3()**: Envia PDF para AWS S3
- **process_document()**: Faz embedding e indexa no Qdrant
- **search()**: Busca documentos similares usando IA

### 3. **views.py** - Endpoints
- **index()**: Página principal com lista de documentos
- **upload_document()**: Recebe PDF, processa e salva
- **search_documents()**: Busca semântica nos documentos

### 4. **urls.py** - Rotas
- `/rag/` - Página inicial
- `/rag/upload/` - Upload de documentos
- `/rag/search/` - Busca de documentos

## 🚀 Como Usar

### 1. Configurar Variáveis de Ambiente
Copie `.env.example` para `.env` e preencha:
```bash
cp .env.example .env
```

### 2. Instalar Dependências
```bash
pip install django python-dotenv boto3 agno-ai
```

### 3. Rodar Migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Criar Superusuário (opcional)
```bash
python manage.py createsuperuser
```

### 5. Iniciar Servidor
```bash
python manage.py runserver
```

### 6. Acessar
- Interface: http://localhost:8000/rag/
- Admin: http://localhost:8000/admin/

## 📝 Exemplo de Uso

### Upload de Documento (via interface web)
1. Acesse http://localhost:8000/rag/
2. Selecione um PDF
3. Preencha autor, categoria, tipo
4. Clique em "Enviar e Processar"

### Upload via Python/API
```python
import requests

files = {'pdf_file': open('documento.pdf', 'rb')}
data = {
    'author': 'João Silva',
    'category': 'IA',
    'type': 'technical_document'
}

response = requests.post('http://localhost:8000/rag/upload/', files=files, data=data)
print(response.json())
```

### Busca de Documentos
```python
import requests

data = {'query': 'O que é inteligência artificial?', 'limit': 5}
response = requests.post('http://localhost:8000/rag/search/', data=data)
print(response.json())
```

## 🔧 Personalização

### Alterar Configurações do Qdrant
Edite `services.py`:
```python
self.vector_db = Qdrant(
    collection="seu_nome",
    url="sua_url",
    embedder=OpenAIEmbedder(id="text-embedding-3-small", dimensions=1536)
)
```

### Alterar Chunking do PDF
Edite `services.py`:
```python
self.pdf_reader = PDFReader(
    chunk_size=2000,  # tamanho do chunk
    chunk_overlap=400  # sobreposição
)
```

## 🎓 Conceitos Django para Iniciantes

### Models (models.py)
- Define a estrutura da tabela no banco de dados
- Cada classe = uma tabela
- Cada atributo = uma coluna

### Views (views.py)
- Controladores que processam requisições
- Recebem dados do usuário
- Retornam respostas (HTML, JSON)

### URLs (urls.py)
- Mapeiam URLs para views
- Ex: `/rag/upload/` chama a view `upload_document`

### Services (services.py)
- Lógica de negócio separada das views
- Facilita reutilização e testes
- Mantém código organizado

### Templates (templates/)
- Arquivos HTML que o Django renderiza
- Podem usar variáveis do Python
- Ex: `{{ doc.source }}` mostra o nome do documento

## 📚 Próximos Passos

1. Adicionar autenticação de usuários
2. Implementar paginação na lista de documentos
3. Adicionar filtros de busca avançada
4. Criar API REST com Django REST Framework
5. Adicionar testes unitários
