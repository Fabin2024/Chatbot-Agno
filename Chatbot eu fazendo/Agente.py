# vector_store.py
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.redis import RedisDb
from dotenv import load_dotenv

load_dotenv()

# IDs e ranges
SAMPLE_SPREADSHEET_ID = "1gU14rrzskA3hJT8aJcYCFYlK3Rr3zvWyjni68ABfL5w"
SAMPLE_RANGE_NAME = "Página1!A1:E"  # Começa da linha 1 pra incluir cabeçalho

# Conexão com Redis
db = RedisDb(db_url="redis://redis:6379/6")

# 1️⃣ Banco vetorial
vector_store = ChromaDb(
    collection="Contexto",
    path="rag_files",
    embedder=OpenAIEmbedder,
    persistent_client=True,
)

# 2️⃣ Conhecimento (RAG)
rag = Knowledge(
    vector_db=vector_store,
    readers=PDFReader(chunking_strategy=SemanticChunking)
)


agente = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=rag,
    db=db,
    add_history_to_context=True,
    num_history_messages=5,
)
