from dotenv import load_dotenv
import os

load_dotenv()
print('dotenv loaded', 'COHERE_API_KEY' in os.environ, 'PINECONE_API_KEY' in os.environ)
print('COHERE_API_KEY=', os.environ.get('COHERE_API_KEY'))
print('PINECONE_API_KEY=', os.environ.get('PINECONE_API_KEY'))
