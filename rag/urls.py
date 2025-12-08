from django.urls import path
from . import views

urlpatterns = [
    path('rag/', views.upload_document, name='upload'),
    path('search/', views.search_documents, name='search'),
]
