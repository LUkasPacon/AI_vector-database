# Test OpenAI API

Jednoduchý Python skript pro testování připojení k OpenAI API.

## Požadavky

- Python 3.6+
- OpenAI API klíč

## Instalace

1. Naklonujte tento repozitář nebo stáhněte soubory.
2. Nainstalujte potřebné závislosti:

```bash
pip install -r requirements.txt
```

## Použití

Existují dva způsoby, jak poskytnout API klíč:

### Metoda 1: Použití .env souboru

1. Přejmenujte soubor `.env.example` na `.env`
2. Nahraďte `your_openai_api_key_here` vaším skutečným OpenAI API klíčem

### Metoda 2: Zadání klíče při spuštění

Spusťte skript a zadejte API klíč, když budete vyzváni:

```bash
python openai_api_test.py
```

## Co skript dělá

Skript provede jednoduché volání OpenAI API pomocí modelu GPT-3.5 Turbo a zobrazí odpověď. Tím ověříte, že:

1. Váš API klíč je platný
2. Máte přístup k API
3. Můžete úspěšně získat odpovědi

## Řešení problémů

Pokud se zobrazí chyba, ujistěte se, že:

- Váš API klíč je správný
- Máte dostatečný kredit na vašem OpenAI účtu
- Máte stabilní připojení k internetu 