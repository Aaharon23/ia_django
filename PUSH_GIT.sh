#!/bin/bash
# Script para fazer push do código para GitHub

echo "=== Push para GitHub ==="

cd /home/aaharon23/Documentos/workplace/curso_django

# Inicializar Git (se ainda não foi)
git init

# Adicionar remote
git remote add origin https://github.com/Aaharon23/ia_django.git

# Ou se já existe, atualizar
git remote set-url origin https://github.com/Aaharon23/ia_django.git

# Adicionar todos os arquivos
git add .

# Commit
git commit -m "Deploy: Sistema RAG Lechi Analytica"

# Push para main
git branch -M main
git push -u origin main

echo "=== Push concluído! ==="
