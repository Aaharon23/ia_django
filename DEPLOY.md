# Checklist de Deploy

## Antes do Deploy

### 1. Variáveis de Ambiente (.env)
```bash
SECRET_KEY=sua_chave_secreta_gerada
DEBUG=False
ALLOWED_HOSTS=seudominio.com
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
AWS_S3_BUCKET=...
OPENAI_API_KEY=...
```

### 2. Gerar SECRET_KEY
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Banco de Dados
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 4. Arquivos Estáticos
```bash
python manage.py collectstatic --noinput
```

### 5. Testar Localmente
```bash
DEBUG=False python manage.py runserver
```

## Deploy em Produção

### Opção 1: AWS EC2 + Gunicorn + Nginx

1. Instalar dependências:
```bash
pip install -r requirements.txt
```

2. Rodar com Gunicorn:
```bash
gunicorn ia.wsgi:application --bind 0.0.0.0:8000
```

3. Configurar Nginx como proxy reverso

### Opção 2: AWS Elastic Beanstalk

1. Criar arquivo `.ebextensions/django.config`
2. Deploy: `eb deploy`

### Opção 3: Docker

1. Criar Dockerfile
2. Build: `docker build -t lechi-rag .`
3. Run: `docker run -p 8000:8000 lechi-rag`

## Segurança

- ✅ DEBUG=False em produção
- ✅ SECRET_KEY em variável de ambiente
- ✅ ALLOWED_HOSTS configurado
- ✅ .env no .gitignore
- ✅ HTTPS configurado (certificado SSL)
- ✅ Firewall configurado
- ✅ Backup do banco de dados

## Monitoramento

- Logs de erro
- Monitoramento de uso da API OpenAI
- Monitoramento do Qdrant
- Monitoramento do S3
