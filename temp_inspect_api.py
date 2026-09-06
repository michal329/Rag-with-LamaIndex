import importlib
import llama_index
print('llama_index', llama_index.__version__)
emb = importlib.import_module('llama_index.embeddings')
print('has CohereEmbeddings', hasattr(emb, 'CohereEmbeddings'))
print('PineconeVectorStore', __import__('llama_index.vector_stores', fromlist=['PineconeVectorStore']).PineconeVectorStore)
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, ServiceContext
print('Main imports OK')
