import os
from dotenv import load_dotenv

load_dotenv()

# Test Pinecone connection
print("Testing Pinecone connection...")

pinecone_key = os.environ.get('PINECONE_API_KEY')
print(f"Pinecone API Key loaded: {'Yes' if pinecone_key else 'No'}")

if not pinecone_key:
    print("❌ PINECONE_API_KEY not found!")
    exit(1)

try:
    print("Importing Pinecone...")
    from pinecone import Pinecone
    print("✓ Imported Pinecone")
    
    print("Creating Pinecone client...")
    pc = Pinecone(api_key=pinecone_key)
    print("✓ Pinecone client created")
    
    print("Listing indexes...")
    indexes = pc.list_indexes()
    print(f"✓ Available indexes: {indexes}")
    
    print("\nTrying to access 'rag-md' index...")
    index = pc.Index("rag-md")
    print("✓ Connected to 'rag-md' index")
    
    print("\nChecking index stats...")
    stats = index.describe_index_stats()
    print(f"Index stats: {stats}")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
