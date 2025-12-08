# Deploy na AWS EC2 - Guia Completo

## 1. Preparar EC2

### Criar instância EC2
- **AMI**: Ubuntu Server 22.04 LTS
- **Tipo**: t2.medium (mínimo) ou t2.large (recomendado)
- **Storage**: 20GB mínimo
- **Security Group**: 
  - SSH (22) - Seu IP
  - HTTP (80) - 0.0.0.0/0
  - HTTPS (443) - 0.0.0.0/0
  - Custom (8000) - Seu IP (temporário para testes)

### Conectar via SSH
```bash
ssh -i sua-chave.pem ubuntu@SEU_IP_EC2
```

## 2. Instalar Dependências

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python, pip, venv
sudo apt install -y python3-pip python3-venv python3-dev

# Instalar Nginx
sudo apt install -y nginx

# Instalar Git
sudo apt install -y git
```

## 3. Clonar Projeto

```bash
cd /home/ubuntu
git clone SEU_REPOSITORIO lechi-rag
cd lechi-rag
```

## 4. Configurar Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configurar Variáveis de Ambiente

```bash
cp .env.example .env
nano .env
```

Editar com:
```env
SECRET_KEY=GERAR_NOVA_CHAVE
DEBUG=False
ALLOWED_HOSTS=SEU_IP_OU_DOMINIO
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
AWS_S3_BUCKET=...
OPENAI_API_KEY=...
```

Gerar SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 6. Configurar Django

```bash
# Migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Criar diretórios de log
sudo mkdir -p /var/log/gunicorn
sudo chown ubuntu:www-data /var/log/gunicorn
```

## 7. Configurar Gunicorn

```bash
# Copiar arquivo de serviço
sudo cp gunicorn.service /etc/systemd/system/

# Recarregar systemd
sudo systemctl daemon-reload

# Iniciar Gunicorn
sudo systemctl start gunicorn

# Habilitar no boot
sudo systemctl enable gunicorn

# Verificar status
sudo systemctl status gunicorn
```

## 8. Configurar Nginx

```bash
# Editar configuração
sudo nano nginx.conf
# Substituir SEU_DOMINIO_OU_IP pelo seu IP/domínio

# Copiar para sites-available
sudo cp nginx.conf /etc/nginx/sites-available/lechi-rag

# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/lechi-rag /etc/nginx/sites-enabled/

# Remover configuração padrão
sudo rm /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

## 9. Configurar Firewall (UFW)

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## 10. Testar

Acesse: `http://SEU_IP_EC2`

## 11. Configurar HTTPS (Opcional mas Recomendado)

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obter certificado SSL
sudo certbot --nginx -d seudominio.com -d www.seudominio.com

# Renovação automática já está configurada
```

## 12. Monitoramento e Logs

```bash
# Ver logs do Gunicorn
sudo journalctl -u gunicorn -f

# Ver logs do Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Ver logs do Gunicorn (custom)
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/gunicorn/access.log
```

## 13. Comandos Úteis

```bash
# Reiniciar Gunicorn
sudo systemctl restart gunicorn

# Reiniciar Nginx
sudo systemctl restart nginx

# Atualizar código
cd /home/ubuntu/lechi-rag
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn

# Backup do banco
python manage.py dumpdata > backup.json
```

## 14. Troubleshooting

### Erro 502 Bad Gateway
```bash
sudo systemctl status gunicorn
sudo journalctl -u gunicorn -n 50
```

### Erro de permissão
```bash
sudo chown -R ubuntu:www-data /home/ubuntu/lechi-rag
sudo chmod -R 755 /home/ubuntu/lechi-rag
```

### Arquivos estáticos não carregam
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

## 15. Segurança Adicional

- Configurar backup automático do banco
- Configurar monitoramento (CloudWatch)
- Configurar alertas de erro
- Limitar tentativas de login
- Configurar rate limiting no Nginx
- Manter sistema atualizado

## 🎉 Deploy Completo!

Seu sistema está rodando em produção na EC2!
