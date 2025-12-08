from django.db import models

class Document(models.Model):
    """Modelo para armazenar informações dos documentos processados"""
    
    source = models.CharField(max_length=255)
    s3_url = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    author = models.CharField(max_length=255)
    date = models.CharField(max_length=50)
    language = models.CharField(max_length=10, default='pt-BR')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.source} - {self.category}"
    
    class Meta:
        ordering = ['-uploaded_at']
