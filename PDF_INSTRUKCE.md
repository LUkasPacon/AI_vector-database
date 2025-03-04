# Instrukce pro nahrání PDF do Pinecone

Vytvořil jsem pro vás skript `pdf_to_pinecone.py`, který umožňuje extrahovat text z PDF souboru, rozdělit ho na menší části, vytvořit embeddings pomocí modelu `multilingual-e5-large` a nahrát je do Pinecone databáze. Poté můžete v obsahu PDF vyhledávat pomocí sémantických dotazů.

## Co skript dělá

1. Extrahuje text z PDF souboru
2. Rozdělí text na menší části (chunky) s možností nastavení velikosti a překryvu
3. Vytvoří embeddings pro každý chunk pomocí modelu `multilingual-e5-large`
4. Nahraje vektory do Pinecone indexu
5. Umožňuje vyhledávat v obsahu PDF pomocí sémantických dotazů

## Instalace závislostí

Před spuštěním skriptu je potřeba nainstalovat potřebné závislosti:

```bash
python3 -m pip install pinecone-client>=3.0.0 python-dotenv PyPDF2>=3.0.0
```

## Jak skript použít

1. Otevřete macOS terminál
2. Přejděte do adresáře projektu:
   ```
   cd /Users/lukaspacon/Documents/GitHub/AI_vector-database
   ```

3. Spusťte skript:
   ```
   python3 pdf_to_pinecone.py
   ```

4. Postupujte podle interaktivních pokynů:
   - Zadejte cestu k PDF souboru
   - Volitelně nastavte velikost chunků a překryvu
   - Po nahrání dat můžete začít vyhledávat v obsahu PDF

## Příklad použití

```
Zadejte cestu k PDF souboru: /Users/lukaspacon/Desktop/Formula-Student-Czech-Republic-Handbook-2025-v1.0.pdf
Zadejte velikost chunků (výchozí: 1000): 800
Zadejte velikost překryvu (výchozí: 200): 100

...

=== Vyhledávání v PDF ===
Zadejte dotaz (nebo 'konec' pro ukončení): Jaké jsou hlavní výhody umělé inteligence?
Kolik výsledků chcete zobrazit? (výchozí: 3): 2

...

=== Vyhledávání v PDF ===
Zadejte dotaz (nebo 'konec' pro ukončení): konec
```

## Tipy pro optimální použití

1. **Velikost chunků**: 
   - Menší chunky (500-800 znaků) jsou vhodné pro přesné vyhledávání konkrétních informací
   - Větší chunky (1000-2000 znaků) zachovávají více kontextu, ale mohou být méně přesné

2. **Velikost překryvu**:
   - Větší překryv (200-300 znaků) pomáhá zachytit informace, které by jinak mohly být rozděleny mezi chunky
   - Menší překryv šetří místo v databázi

3. **Formulace dotazů**:
   - Používejte přirozené otázky nebo fráze
   - Experimentujte s různými formulacemi pro lepší výsledky

## Řešení problémů

- **Chyba při extrakci textu z PDF**: Některé PDF soubory mohou být chráněné nebo používat nestandardní formátování. Zkuste jiný PDF soubor nebo použijte nástroj pro předběžnou konverzi PDF do textu.

- **Chyba při vytváření embeddings**: Ujistěte se, že máte správně nastaven Pinecone API klíč a že model `multilingual-e5-large` je dostupný.

- **Nedostatek paměti**: Pokud zpracováváte velmi velké PDF soubory, může dojít k nedostatku paměti. Zkuste zmenšit velikost chunků nebo zpracovat PDF po částech.

## Rozšíření funkcionality

Skript můžete dále rozšířit o:

1. Podporu více formátů dokumentů (DOCX, TXT, HTML)
2. Extrakci metadat z PDF (autor, datum vytvoření, klíčová slova)
3. Filtrování výsledků podle metadat
4. Vizualizaci výsledků vyhledávání 