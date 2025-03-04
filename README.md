# PDF to Pinecone Vector Database

Tento projekt umožňuje extrakci textu z PDF dokumentů, jeho rozdělení na menší části, vytvoření vektorových reprezentací pomocí OpenAI embeddings a následné uložení do Pinecone vektorové databáze pro efektivní sémantické vyhledávání.

## Funkce

- **Extrakce textu z PDF** - Automatické načtení a extrakce textu z PDF dokumentů
- **Inteligentní chunking** - Rozdělení textu na menší části s nastavitelnou velikostí a překryvem
- **Vektorizace pomocí OpenAI** - Vytvoření kvalitních embeddings pomocí modelu `text-embedding-3-large`
- **Ukládání do Pinecone** - Efektivní ukládání vektorů do Pinecone databáze
- **Sémantické vyhledávání** - Vyhledávání relevantních informací pomocí přirozeného jazyka
- **Interaktivní rozhraní** - Jednoduché uživatelské rozhraní pro nahrávání a vyhledávání

## Požadavky

- Python 3.7+
- OpenAI API klíč
- Pinecone API klíč
- Nainstalované závislosti z `requirements.txt`

## Instalace

1. Naklonujte repozitář:
   ```bash
   git clone <url-repozitáře>
   cd <název-adresáře>
   ```

2. Nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```

3. Vytvořte soubor `.env` s vašimi API klíči:
   ```
   OPENAI_API_KEY=váš-openai-api-klíč
   PINECONE_API_KEY=váš-pinecone-api-klíč
   ```

## Použití

Spusťte skript příkazem:
```bash
python3 pdf_to_pinecone.py
```

### Nahrání PDF do Pinecone

1. Vyberte možnost nahrání PDF do Pinecone
2. Zadejte cestu k PDF souboru
3. Volitelně nastavte velikost chunků a překryv
4. Počkejte na dokončení procesu

### Vyhledávání v dokumentu

1. Vyberte možnost vyhledávání v dokumentu
2. Zadejte váš dotaz v přirozeném jazyce
3. Prohlédněte si výsledky seřazené podle relevance

## Jak to funguje

### 1. Extrakce textu z PDF
Skript používá knihovnu PyPDF2 k extrakci textu ze všech stránek PDF dokumentu.

### 2. Rozdělení textu na části (chunking)
Extrahovaný text je rozdělen na menší překrývající se části (chunky) pro efektivní zpracování a vyhledávání.

### 3. Vytváření embeddings
Pro každý chunk je vytvořen embedding (vektorová reprezentace) pomocí OpenAI API a modelu `text-embedding-3-large`.

### 4. Ukládání do Pinecone
Embeddings jsou uloženy do Pinecone vektorové databáze spolu s metadaty obsahujícími původní text a informace o pozici v dokumentu.

### 5. Vyhledávání
Při vyhledávání je dotaz převeden na embedding a porovnán s uloženými vektory v Pinecone. Výsledky jsou seřazeny podle podobnosti.

## Optimalizace

- **Velikost chunků**: Menší chunky (500-1000 znaků) jsou vhodné pro přesné vyhledávání konkrétních informací, větší chunky (1500-2000 znaků) zachovávají více kontextu.
- **Překryv**: Větší překryv (200-300 znaků) zajišťuje, že informace na hranicích chunků nejsou ztraceny.
- **Model embeddings**: Model `text-embedding-3-large` poskytuje vysoce kvalitní vektorové reprezentace pro přesné vyhledávání.

## Struktura projektu

- `pdf_to_pinecone.py` - Hlavní skript
- `requirements.txt` - Seznam závislostí
- `.env` - Soubor s API klíči (není součástí repozitáře)
- `PDF_INSTRUKCE.md` - Podrobné instrukce k použití
- `PDFs/` - Adresář pro ukládání PDF souborů

## Licence

Tento projekt je licencován pod Apache License 2.0 - viz [oficiální text licence](https://www.apache.org/licenses/LICENSE-2.0).

### Shrnutí licence Apache 2.0:
- Můžete svobodně používat, upravovat a distribuovat tento software
- Můžete používat software pro komerční účely
- Nemusíte sdílet zdrojový kód vašich modifikací
- Musíte zachovat informace o autorských právech a licenci
- Poskytuje explicitní udělení patentových práv od přispěvatelů
- Neposkytuje žádnou záruku a odmítá odpovědnost za škody 