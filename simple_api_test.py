import openai
import os

# Vymazat předchozí výsledek, pokud existuje
if os.path.exists("api_result.txt"):
    os.remove("api_result.txt")

# Funkce pro zápis do souboru
def write_result(message):
    with open("api_result.txt", "a") as f:
        f.write(message + "\n")

# API klíč
api_key = "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"

try:
    # Inicializace klienta
    client = openai.OpenAI(api_key=api_key)
    write_result("OpenAI klient byl inicializován")
    
    # Jednoduchý test
    write_result("Odesílám požadavek...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Řekni 'Test API byl úspěšný' v češtině."}
        ]
    )
    
    # Zápis výsledku
    write_result("\nTest byl úspěšný!")
    write_result(f"Model: {response.model}")
    write_result(f"Odpověď: {response.choices[0].message.content}")
    
except Exception as e:
    write_result(f"Chyba: {str(e)}")

write_result("Test dokončen") 