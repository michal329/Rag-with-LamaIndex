import subprocess
import os
project = r'C:\Users\User\Desktop\AI008'
py = os.path.join(project, '.venv311', 'Scripts', 'python.exe')
for pkg in ['llama-index','llama-index-vector-stores-pinecone','pinecone-client','gradio','llama-index-embeddings-cohere']:
    p = subprocess.run([py, '-m', 'pip', 'show', pkg], capture_output=True, text=True)
    print('PACKAGE', pkg)
    print('RC', p.returncode)
    print(p.stdout.strip())
    print('---')
