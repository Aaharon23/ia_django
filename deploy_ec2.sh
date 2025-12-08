#!/bin/bash
# Script de deploy para EC2 - Lechi Analytica RAG

echo "=== Deploy EC2 - Lechi Analytica ==="

# 1. Atualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar Python e dependências
sudo apt install -y python3-pip python3-venv nginx

# 3. Criar diretório do projeto
cd /home/ubuntu
git clone SEU_REPOSITORIO lechi-rag
cd lechi-rag

# 4. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 5. Instalar dependências
pip install -r requirements.txt

# 6. Configurar variáveis de ambiente
cp .env.example .env
nano .env  # Editar com suas credenciais

# 7. Gerar SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 8. Rodar migrações
python manage.py makemigrations
python manage.py migrate

# 9. Criar superusuário
python manage.py createsuperuser

# 10. Coletar arquivos estáticos
python manage.py collectstatic --noinput

# 11. Testar
python manage.py runserver 0.0.0.0:8000

echo "=== Deploy concluído! ==="
