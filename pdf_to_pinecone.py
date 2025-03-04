from pinecone import Pinecone, ServerlessSpec
import os
import re
import uuid
from dotenv import load_dotenv
import PyPDF2
from typing import List, Dict, Any
from openai import OpenAI

# Načtení proměnných prostředí
load_dotenv()

# Inicializace Pinecone klienta

# Inicializace OpenAI klienta
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extrahuje text z PDF souboru"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            print(f"PDF obsahuje {num_pages} stránek")
            
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n\n"
                
        return text
    except Exception as e:
        print(f"Chyba při extrakci textu z PDF: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Rozdělí text na menší části s překryvem"""
    chunks = []
    
    # Nejprve rozdělíme text na odstavce
    paragraphs = re.split(r'\n\s*\n', text)
    
    current_chunk = ""
    for paragraph in paragraphs:
        # Pokud je odstavec příliš dlouhý, rozdělíme ho na menší části
        if len(paragraph) > chunk_size:
            words = paragraph.split()
            temp_chunk = ""
            for word in words:
                if len(temp_chunk) + len(word) + 1 <= chunk_size:
                    temp_chunk += word + " "
                else:
                    chunks.append(temp_chunk.strip())
                    # Zachováme překryv
                    overlap_words = temp_chunk.split()[-overlap//10:]
                    temp_chunk = " ".join(overlap_words) + " " + word + " "
            if temp_chunk:
                chunks.append(temp_chunk.strip())
        else:
            # Pokud se odstavec vejde do aktuálního chunku, přidáme ho
            if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                # Jinak uložíme aktuální chunk a začneme nový
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"
    
    # Přidáme poslední chunk, pokud existuje
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    print(f"Text rozdělen na {len(chunks)} částí")
    return chunks

def create_embedding(text: str) -> List[float]:
    """Vytvoří embedding pro text pomocí OpenAI API"""
    # Použití výkonnějšího modelu pro embeddings
    response = openai_client.embeddings.create(
        model="text-embedding-3-large",  # Změna na výkonnější model
        input=text,
        encoding_format="float"
    )
    return response.data[0].embedding

def create_embeddings_and_upload(chunks: List[str], pdf_name: str, index_name: str = "pdf-search"):
    """Vytvoří embeddings pro chunky a nahraje je do Pinecone"""
    try:
        # Vytvoření embeddings
        print(f"Vytvářím embeddings pro {len(chunks)} částí...")
        
        # Zpracování po dávkách, aby se vešly do API limitu
        batch_size = 20
        all_vectors = []
        
        # Nejprve vytvoříme jeden embedding, abychom zjistili dimenzi
        sample_embedding = create_embedding(chunks[0])
        embedding_dimension = len(sample_embedding)
        print(f"Dimenze embeddings: {embedding_dimension}")
        
        # Přidáme první embedding do vektorů
        all_vectors.append({
            "id": f"pdf_{pdf_name}_0",
            "values": sample_embedding,
            "metadata": {
                "text": chunks[0],
                "source": pdf_name,
                "chunk_index": 0
            }
        })
        
        # Zpracujeme zbytek chunků
        for i in range(1, len(chunks), batch_size):
            batch = chunks[i:min(i+batch_size, len(chunks))]
            print(f"Zpracovávám dávku {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")
            
            # Vytvoření embeddings pomocí OpenAI
            embeddings = []
            for chunk in batch:
                embedding = create_embedding(chunk)
                embeddings.append(embedding)
            
            # Vytvoření vektorů pro Pinecone
            for j, (chunk, embedding) in enumerate(zip(batch, embeddings)):
                chunk_id = f"pdf_{pdf_name}_{i+j}"
                all_vectors.append({
                    "id": chunk_id,
                    "values": embedding,
                    "metadata": {
                        "text": chunk,
                        "source": pdf_name,
                        "chunk_index": i+j
                    }
                })
        
        # Připojení k indexu nebo vytvoření nového
        print(f"Kontroluji index: {index_name}")
        
        # Získání seznamu existujících indexů
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        # Pokud index existuje, zkontrolujeme jeho dimenzi
        if index_name in existing_indexes:
            try:
                index_info = pc.describe_index(index_name)
                current_dimension = index_info.dimension
                
                # Pokud se dimenze neshoduje, zeptáme se uživatele, zda chce index smazat a vytvořit nový
                if current_dimension != embedding_dimension:
                    print(f"VAROVÁNÍ: Existující index má dimenzi {current_dimension}, ale embeddings mají dimenzi {embedding_dimension}.")
                    user_choice = input("Chcete smazat existující index a vytvořit nový? (ano/ne): ")
                    
                    if user_choice.lower() in ["ano", "a", "yes", "y"]:
                        print(f"Mažu index {index_name}...")
                        pc.delete_index(index_name)
                        print(f"Vytvářím nový index {index_name} s dimenzí {embedding_dimension}...")
                        # Vytvoření indexu s regionem us-east-1 (Virginia), který podporuje Starter plán
                        pc.create_index(
                            name=index_name,
                            dimension=embedding_dimension,
                            metric="cosine",
                            spec=ServerlessSpec(cloud="aws", region="us-east-1")
                        )
                    else:
                        print("Operace zrušena. Použijte jiný název indexu nebo smažte existující index ručně.")
                        return False
            except Exception as e:
                print(f"Chyba při kontrole indexu: {e}")
                return False
        else:
            # Vytvoření nového indexu
            print(f"Vytvářím nový index {index_name} s dimenzí {embedding_dimension}...")
            # Vytvoření indexu s regionem us-east-1 (Virginia), který podporuje Starter plán
            pc.create_index(
                name=index_name,
                dimension=embedding_dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        # Počkáme, až bude index připraven
        print("Čekám, až bude index připraven...")
        import time
        time.sleep(10)  # Počkáme 10 sekund
        
        # Připojení k indexu
        index = pc.Index(index_name)
        
        # Nahrání vektorů po dávkách
        upload_batch_size = 100
        for i in range(0, len(all_vectors), upload_batch_size):
            batch = all_vectors[i:i+upload_batch_size]
            print(f"Nahrávám dávku {i//upload_batch_size + 1}/{(len(all_vectors)-1)//upload_batch_size + 1}")
            index.upsert(vectors=batch)
        
        print(f"Úspěšně nahráno {len(all_vectors)} vektorů do indexu {index_name}")
        return True
    
    except Exception as e:
        print(f"Chyba při vytváření embeddings nebo nahrávání do Pinecone: {e}")
        import traceback
        traceback.print_exc()
        return False

def search_in_pdf(query: str, index_name: str = "pdf-search", top_k: int = 5):  # Zvýšení výchozího počtu výsledků
    """Vyhledá podobné chunky v Pinecone na základě dotazu"""
    try:
        # Předzpracování dotazu - odstranění nadbytečných mezer a interpunkce
        query = query.strip()
        
        print(f"Vyhledávám: '{query}'")
        
        # Vytvoření embedding pro dotaz pomocí OpenAI
        query_embedding = create_embedding(query)
        
        # Připojení k indexu
        index = pc.Index(index_name)
        
        # Vyhledání podobných vektorů
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        if not results["matches"]:
            print("Nenalezeny žádné výsledky. Zkuste přeformulovat dotaz.")
            return None
        
        print(f"\nVýsledky pro dotaz: '{query}'")
        
        # Seřazení výsledků podle skóre podobnosti
        sorted_results = sorted(results["matches"], key=lambda x: x["score"], reverse=True)
        
        for i, match in enumerate(sorted_results):
            similarity_score = match["score"]
            # Zobrazení pouze výsledků s dostatečnou podobností
            if similarity_score < 0.5:  # Filtrování výsledků s nízkým skóre
                continue
                
            print(f"\n--- Výsledek {i+1} ---")
            print(f"Skóre podobnosti: {similarity_score:.4f}")
            print(f"Zdroj: {match['metadata'].get('source', 'Neznámý')}")
            
            # Zvýraznění relevantních částí textu
            text = match['metadata']['text']
            
            # Omezení délky zobrazeného textu, ale zobrazení více kontextu
            max_display_length = 800
            if len(text) > max_display_length:
                half_length = max_display_length // 2
                display_text = text[:half_length] + "..." + text[-half_length:]
            else:
                display_text = text
                
            print(f"Text:\n{display_text}")
        
        return results
    
    except Exception as e:
        print(f"Chyba při vyhledávání: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    # Cesta k PDF souboru
    pdf_path = input("Zadejte cestu k PDF souboru: ")
    
    if not os.path.exists(pdf_path):
        print(f"Soubor {pdf_path} neexistuje!")
        return
    
    # Extrakce textu z PDF
    print(f"Extrahuji text z {pdf_path}...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("Nepodařilo se extrahovat text z PDF.")
        return
    
    print(f"Extrahováno {len(text)} znaků textu.")
    
    # Rozdělení textu na chunky
    chunk_size = input("Zadejte velikost chunků (výchozí: 800): ")  # Menší výchozí velikost chunků
    if not chunk_size:
        chunk_size = 800
    else:
        chunk_size = int(chunk_size)
    
    overlap = input("Zadejte velikost překryvu (výchozí: 200): ")
    if not overlap:
        overlap = 200
    else:
        overlap = int(overlap)
    
    chunks = chunk_text(text, chunk_size, overlap)
    
    # Získání názvu PDF bez cesty a přípony
    pdf_name = os.path.basename(pdf_path)
    pdf_name = os.path.splitext(pdf_name)[0]
    
    # Zadání názvu indexu
    index_name = input("Zadejte název indexu (výchozí: pdf-search): ")
    if not index_name:
        index_name = "pdf-search"
    
    # Validace názvu indexu - pouze malá písmena, číslice a pomlčky
    if not re.match(r'^[a-z0-9\-]+$', index_name):
        print("Název indexu může obsahovat pouze malá písmena, číslice a pomlčky.")
        # Automaticky opravíme název indexu
        index_name = re.sub(r'[^a-z0-9\-]', '-', index_name.lower())
        print(f"Název indexu byl upraven na: {index_name}")
    
    # Vytvoření embeddings a nahrání do Pinecone
    success = create_embeddings_and_upload(chunks, pdf_name, index_name)
    
    if success:
        print("\nPDF úspěšně nahráno do Pinecone!")
        
        # Vyhledávání
        while True:
            print("\n=== Vyhledávání v PDF ===")
            print("Tipy pro lepší výsledky:")
            print("- Používejte konkrétní dotazy")
            print("- Zkuste různé formulace stejného dotazu")
            print("- Používejte klíčová slova z dokumentu")
            
            query = input("\nZadejte dotaz (nebo 'konec' pro ukončení): ")
            
            if query.lower() == "konec":
                break
            
            top_k = input("Kolik výsledků chcete zobrazit? (výchozí: 5): ")
            if not top_k:
                top_k = 5
            else:
                top_k = int(top_k)
            
            search_in_pdf(query, index_name, top_k=top_k)

if __name__ == "__main__":
    main()