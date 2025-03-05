# PDFIntelliSearch Instructions / Instrukce

## English Instructions

### Quick Start

1. **Installation**:
   ```bash
   # Install dependencies
   python3 -m pip install -r requirements.txt
   
   # Create .env file with your API keys
   echo "OPENAI_API_KEY=your_key_here" > .env
   echo "PINECONE_API_KEY=your_key_here" >> .env
   ```

2. **Running the Application**:
   
   GUI Mode (Recommended):
   ```bash
   streamlit run streamlit_app.py
   ```
   
   CLI Mode:
   ```bash
   python3 pdfintelisearch.py
   ```

### Using the GUI

1. **Upload PDF**:
   - Click "Upload PDF" in the sidebar
   - Drag & drop your PDF file
   - Click "Process PDF" to start extraction

2. **Configure Settings**:
   - Adjust chunk size (300-2000)
   - Set overlap (50-500)
   - Tune similarity threshold (0.0-1.0)
   - Select number of results (1-10)

3. **Search**:
   - Select an index from the dropdown
   - Enter your question
   - View results and AI-generated answers
   - Expand source chunks for details

### Using the CLI

1. **Main Menu**:
   - Option 1: Upload new PDF
   - Option 2: Search existing index
   - Option 3: Exit

2. **PDF Upload**:
   - Enter PDF path
   - Set chunk size and overlap
   - Choose index name
   - Wait for processing

3. **Search Mode**:
   - Select index number
   - Enter search query
   - View results and AI answers

### Tips for Better Results

1. **PDF Quality**:
   - Use searchable PDFs
   - Ensure clear formatting
   - Check text extraction quality

2. **Search Queries**:
   - Be specific
   - Use natural language
   - Include relevant keywords

3. **Settings Optimization**:
   - Larger chunks for context
   - More overlap for connectivity
   - Lower threshold for more results

## České Instrukce

### Rychlý Start

1. **Instalace**:
   ```bash
   # Instalace závislostí
   python3 -m pip install -r requirements.txt
   
   # Vytvoření .env souboru s API klíči
   echo "OPENAI_API_KEY=vas_klic" > .env
   echo "PINECONE_API_KEY=vas_klic" >> .env
   ```

2. **Spuštění Aplikace**:
   
   GUI Režim (Doporučeno):
   ```bash
   streamlit run streamlit_app.py
   ```
   
   CLI Režim:
   ```bash
   python3 pdfintelisearch.py
   ```

### Použití GUI

1. **Nahrání PDF**:
   - Klikněte na "Upload PDF" v postranním panelu
   - Přetáhněte PDF soubor
   - Klikněte na "Process PDF" pro zahájení extrakce

2. **Nastavení**:
   - Velikost chunků (300-2000)
   - Překryv (50-500)
   - Práh podobnosti (0.0-1.0)
   - Počet výsledků (1-10)

3. **Vyhledávání**:
   - Vyberte index z rozbalovací nabídky
   - Zadejte otázku
   - Prohlédněte si výsledky a AI odpovědi
   - Rozbalte zdrojové chunky pro detaily

### Použití CLI

1. **Hlavní Menu**:
   - Volba 1: Nahrát nové PDF
   - Volba 2: Vyhledávat v existujícím indexu
   - Volba 3: Ukončit

2. **Nahrávání PDF**:
   - Zadejte cestu k PDF
   - Nastavte velikost chunků a překryv
   - Zvolte název indexu
   - Počkejte na zpracování

3. **Režim Vyhledávání**:
   - Vyberte číslo indexu
   - Zadejte vyhledávací dotaz
   - Prohlédněte si výsledky a AI odpovědi

### Tipy pro Lepší Výsledky

1. **Kvalita PDF**:
   - Používejte prohledávatelná PDF
   - Zajistěte čisté formátování
   - Zkontrolujte kvalitu extrakce textu

2. **Vyhledávací Dotazy**:
   - Buďte konkrétní
   - Používejte přirozený jazyk
   - Zahrňte relevantní klíčová slova

3. **Optimalizace Nastavení**:
   - Větší chunky pro kontext
   - Větší překryv pro spojitost
   - Nižší práh pro více výsledků

## API Usage / Použití API

### OpenAI API
- Used for embeddings (text-embedding-3-large)
- Used for answer generation (GPT-4 Turbo)
- Costs apply based on token usage

### Pinecone API
- Free tier: 5 indexes maximum
- Serverless deployment on AWS
- 3072-dimensional vectors
- Cosine similarity search 