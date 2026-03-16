import os
import json
import time
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

def create_novotel_vector_store():
    # Initialize Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    index_name = "novotel-hf"
    dimension = 384

    # Check if index exists, if not create it
    if index_name not in pc.list_indexes().names():
        print(f"Creating index {index_name}...")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
            )
        )
        # Wait for index to be ready
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
        print(f"Index {index_name} is ready.")
    else:
        print(f"Index {index_name} already exists.")

    # Initialize Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Load and process Novotel Services JSON
    with open('novotel_services.json', 'r', encoding='utf-8') as f:
        services_data = json.load(f)

    documents = []
    for item in services_data:
        # Create a rich text representation for the vector search
        content = f"Service/Room Name: {item.get('dish_name')} \n" \
                  f"Category: {item.get('category')} \n" \
                  f"Price: Rs {item.get('price')} \n" \
                  f"Details: {item.get('veg_nonveg')} \n" \
                  f"Primary Focus: {item.get('main_ingredient')} \n" \
                  f"Amenities/Features: {', '.join(item.get('secondary_ingredients', []))} \n" \
                  f"Style: {item.get('cooking_method', '')} \n" \
                  f"Target Segment: {item.get('cooking_style', '')} \n" \
                  f"Brand Alignment: {item.get('spice_level', '')} \n"
        
        metadata = {
            "name": item.get("dish_name"),
            "category": item.get("category"),
            "price": item.get("price")
        }
        
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)

    print(f"Loaded {len(documents)} service items as documents.")

    # Read novotel_info.txt context
    try:
        with open('novotel_info.txt', 'r', encoding='utf-8') as f:
            info_content = f.read()
            info_doc = Document(
                page_content=info_content,
                metadata={"category": "hotel_context", "name": "About Novotel"}
            )
            documents.append(info_doc)
            print("Loaded novotel_info.txt hotel context.")
    except Exception as e:
        print(f"Warning: Could not load novotel_info.txt context: {e}")

    # Store in Pinecone
    print("Uploading vectors to Pinecone...")
    vectorstore = PineconeVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        index_name=index_name
    )
    print("Upload complete! Novotel knowledge base is ready.")

if __name__ == "__main__":
    create_novotel_vector_store()
