import importlib
import sys
print('python', sys.version)
import llama_index
print('llama_index imported')
emb = importlib.import_module('llama_index.embeddings')
print('emb module loaded:', emb.__name__)
vs = importlib.import_module('llama_index.vector_stores')
print('vector_stores module loaded:', vs.__name__)
try:
    from llama_index.embeddings import CohereEmbeddings
    print('CohereEmbeddings OK')
except Exception as e:
    print('CohereEmbeddings FAIL', e)
try:
    from llama_index.vector_stores import PineconeVectorStore
    print('PineconeVectorStore OK')
except Exception as e:
    print('PineconeVectorStore FAIL', e)
