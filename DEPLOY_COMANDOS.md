# Comandos para Deploy via Git

## 1. No seu computador (Push para GitHub)

```bash
cd /home/aaharon23/Documentos/workplace/curso_django

# Inicializar Git
git init

# Adicionar remote
git remote add origin https://github.com/Aaharon23/ia_django.git

# Adicionar arquivos
git add .

# Commit
git commit -m "Deploy: Sistema RAG Lechi Analytica"

# Push
git branch -M main
git push -u origin main
```

## 2. Na EC2 (Clone e Deploy)

```bash
# Conectar na EC2
ssh -i sua-chave.pem ubuntu@SEU_IP_EC2

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3-pip python3-venv python3-dev nginx git

# Clonar repositório
cd /home/ubuntu
git clone https://github.com/Aaharon23/ia_django.git lechi-rag
cd lechi-rag

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências Python
pip install --upgrade pip
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
nano .env
# Editar com suas credenciais

# Gerar SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Copiar e colar no .env

# Rodar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Criar diretórios de log
sudo mkdir -p /var/log/gunicorn
sudo chown ubuntu:www-data /var/log/gunicorn

# Configurar Gunicorn service
sudo cp gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn

# Configurar Nginx
sudo nano nginx.conf
# Substituir SEU_DOMINIO_OU_IP pelo seu IP

sudo cp nginx.conf /etc/nginx/sites-available/lechi-rag
sudo ln -s /etc/nginx/sites-available/lechi-rag /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Configurar firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## 3. Testar

Acesse: `http://SEU_IP_EC2`

## 4. Atualizar código (futuro)

```bash
# Na EC2
cd /home/ubuntu/lechi-rag
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

## 5. Ver logs

```bash
# Logs do Gunicorn
sudo journalctl -u gunicorn -f

# Logs do Nginx
sudo tail -f /var/log/nginx/error.log
```

## 🎉 Pronto!

Seu sistema está rodando em produção!
