import subprocess
import os

py311 = r'C:\Users\User\AppData\Local\Programs\Python\Python311\python.exe'
project = r'C:\Users\User\Desktop\AI008'
os.chdir(project)
print('using', py311)
steps = [
    [py311, '-m', 'venv', '.venv311'],
    [os.path.join(project, '.venv311', 'Scripts', 'python.exe'), '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'],
    [os.path.join(project, '.venv311', 'Scripts', 'python.exe'), '-m', 'pip', 'install', 'llama-index', 'llama-index-vector-stores-pinecone', 'pinecone-client', 'gradio'],
    [os.path.join(project, '.venv311', 'Scripts', 'python.exe'), '-m', 'pip', 'install', 'llama-index-embeddings-cohere'],
]
for step in steps:
    print('\nSTEP', step)
    p = subprocess.run(step, capture_output=True, text=True)
    print('rc', p.returncode)
    print('out', p.stdout[:4000])
    print('err', p.stderr[:4000])
    if p.returncode != 0:
        break
