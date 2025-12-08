from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .services import RAGService
import os


def home(request):
    """Página inicial da Lechi Analytica"""
    return render(request, 'rag/home.html')


def login_view(request):
    """Página de login customizada"""
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/search/')
            return redirect(next_url)
        else:
            return render(request, 'rag/login.html', {'error': 'Usuário ou senha inválidos'})
    
    return render(request, 'rag/login.html')


@csrf_exempt
def upload_document(request):
    """GET /rag/ - Página de upload | POST /rag/ - Processa upload"""
    if request.method == 'GET':
        return render(request, 'rag/upload.html')
    
    if not request.FILES.get('pdf_file'):
        return JsonResponse({'error': 'Envie um arquivo PDF via POST'}, status=400)
    
    pdf_file = request.FILES['pdf_file']
    temp_path = default_storage.save(f'temp/{pdf_file.name}', ContentFile(pdf_file.read()))
    full_path = default_storage.path(temp_path)
    
    try:
        rag_service = RAGService()
        s3_url = rag_service.upload_pdf_to_s3(full_path)
        
        metadata = {
            "source": pdf_file.name,
            "type": request.POST.get('type', 'technical_document'),
            "category": request.POST.get('category', 'general'),
            "author": request.POST.get('author', 'Unknown'),
            "date": request.POST.get('date', '2024'),
            "language": request.POST.get('language', 'pt-BR')
        }
        
        rag_service.process_document(full_path, metadata)
        default_storage.delete(temp_path)
        
        return JsonResponse({
            'success': True,
            'message': 'Documento processado com sucesso!',
            's3_url': s3_url
        })
        
    except Exception as e:
        if default_storage.exists(temp_path):
            default_storage.delete(temp_path)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required(login_url='/login/')
@csrf_exempt
def search_documents(request):
    """GET /search/ - Página de busca | POST /search/ - Processa busca"""
    if request.method == 'GET':
        return render(request, 'rag/search.html')
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Use POST'}, status=400)
    
    query = request.POST.get('query', '')
    if not query:
        return JsonResponse({'error': 'Parâmetro query obrigatório'}, status=400)
    
    try:
        rag_service = RAGService()
        response = rag_service.search(query)
        
        return JsonResponse({
            'success': True,
            'query': query,
            'response': response
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
