import importlib
import llama_index
print('llama_index package', getattr(llama_index, '__file__', getattr(llama_index, '__path__', None)))
print('llama_index dir:', [x for x in dir(llama_index) if x[0].isupper() or 'emb' in x.lower() or 'vector' in x.lower()])
emb = importlib.import_module('llama_index.embeddings')
print('emb dir:', [x for x in dir(emb) if 'Coh' in x or 'Embed' in x or 'coh' in x])
for sub in ['cohere','cohere_embeddings','cohere_embedding','cohere_embed','cohere']: 
    try:
        mod = importlib.import_module(f'llama_index.embeddings.{sub}')
        print('found module', sub, 'dir', [x for x in dir(mod) if 'Coh' in x or 'Embed' in x or 'coh' in x])
    except Exception as e:
        print('module', sub, 'fail', e)
vs = importlib.import_module('llama_index.vector_stores')
print('vs dir:', [x for x in dir(vs) if 'Pine' in x or 'Vector' in x or 'pine' in x])
for sub in ['pinecone','pinecone_vector','pinecone_store','pinecone_store_vector']:
    try:
        mod = importlib.import_module(f'llama_index.vector_stores.{sub}')
        print('found vs module', sub, 'dir', [x for x in dir(mod) if 'Pine' in x or 'Vector' in x or 'pine' in x])
    except Exception as e:
        print('vs module', sub, 'fail', e)
