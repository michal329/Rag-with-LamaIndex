import importlib, pkgutil
mod = importlib.import_module('llama_index')
print('llama_index path', getattr(mod,'__file__', getattr(mod,'__path__', None)))
print('submodules of llama_index:')
for info in pkgutil.iter_modules(mod.__path__):
    print('  ', info.name)
print('--- embeddings submodules ---')
emb = importlib.import_module('llama_index.embeddings')
for info in pkgutil.iter_modules(emb.__path__):
    print('  ', info.name)
print('--- vector_stores submodules ---')
vs = importlib.import_module('llama_index.vector_stores')
for info in pkgutil.iter_modules(vs.__path__):
    print('  ', info.name)
