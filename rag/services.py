from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.qdrant import Qdrant
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.reader.pdf_reader import PDFReader
import boto3
import os

load_dotenv()


class RAGService:
    """Serviço para gerenciar operações de RAG (Retrieval-Augmented Generation)"""
    
    def __init__(self):
        # Configurar banco vetorial Qdrant
        self.vector_db = Qdrant(
            collection="documentos",
            url="http://34.235.67.215:6333",
            embedder=OpenAIEmbedder(id="text-embedding-3-small", dimensions=1536)
        )
        
        # Configurar reader com chunking
        self.pdf_reader = PDFReader(chunk_size=1000, chunk_overlap=200)
        
        # Base de conhecimento
        self.knowledge_base = Knowledge(
            name="Base de dados IA-7 CFTVIP",
            description="Base de conhecimento sobre documentos",
            vector_db=self.vector_db,
            readers={"pdf": self.pdf_reader},
            max_results=3
        )
        
        # Agente com RAG
        self.agente = Agent(
            model=OpenAIChat(
                id="gpt-4o-mini",
                temperature=0.1,
                max_tokens=300,
                timeout=60,
                max_retries=3
            ),
            knowledge=self.knowledge_base,
            description="Assistente com acesso a documentos",
            instructions=[
                "Responda com base {knowledge}",
                "Quando não encontrar a informação solicitada na documentação apenas diga: Aguardando novas informações sobre essa assunto para responder"
            ],
            markdown=True
        )
        
        self.bucket_name = os.getenv('AWS_S3_BUCKET', 'xz500bbrty-adr')
    
    def upload_pdf_to_s3(self, file_path, s3_key=None):
        """Faz upload de PDF para S3 com ACL pública"""
        if s3_key is None:
            s3_key = os.path.basename(file_path)
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        
        s3_client.upload_file(
            file_path, 
            self.bucket_name, 
            s3_key, 
            ExtraArgs={'ContentType': 'application/pdf'}
        )
        
        url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
        return url
    
    def process_document(self, file_path, metadata):
        """Processa documento: faz embedding e indexa no Qdrant"""
        self.knowledge_base.add_content(
            path=file_path,
            metadata=metadata
        )
        return True
    
    def search(self, query):
        """Busca usando agente com RAG"""
        try:
            response = self.agente.run(query)
            return response.content if response and response.content else "Sem resposta"
        except Exception as e:
            return f"Erro na busca: {str(e)}"
