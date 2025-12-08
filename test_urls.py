#!/usr/bin/env python3
"""Script para testar se as URLs estão configuradas"""

print("=== Testando configuração das URLs ===\n")

# Testar imports
try:
    from rag import views
    print("✓ Views importadas com sucesso")
    print(f"  - upload_document: {views.upload_document}")
    print(f"  - search_documents: {views.search_documents}")
except Exception as e:
    print(f"✗ Erro ao importar views: {e}")

print("\n=== URLs configuradas ===")
print("POST /rag/     -> upload_document")
print("POST /search/  -> search_documents")

print("\n=== Como testar ===")
print("1. Ative o ambiente virtual")
print("2. Execute: python3 manage.py runserver")
print("3. Teste com curl ou Postman:")
print("\n   Upload:")
print('   curl -X POST http://localhost:8000/rag/ -F "pdf_file=@arquivo.pdf"')
print("\n   Busca:")
print('   curl -X POST http://localhost:8000/search/ -d "query=teste"')
