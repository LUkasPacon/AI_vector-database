import openai
import traceback
import os

# Vymazat předchozí log
if os.path.exists("api_test_log.txt"):
    os.remove("api_test_log.txt")

# Funkce pro zápis do logu
def log_to_file(message):
    with open("api_test_log.txt", "a") as f:
        f.write(message + "\n")

try:
    # Zadejte API klíč přímo zde
    api_key = "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"
    
    log_to_file(f"Používám API klíč: {api_key[:8]}...{api_key[-4:]}")
    
    # Inicializace klienta
    client = openai.OpenAI(api_key=api_key)
    log_to_file("Klient OpenAI byl inicializován")
    
    # Jednoduchý test
    log_to_file("Odesílám požadavek na OpenAI API...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Řekni 'Ahoj, svět!' v češtině."}
        ]
    )
    
    # Výpis odpovědi
    log_to_file("\nÚspěšné připojení k OpenAI API!")
    log_to_file(f"Model: {response.model}")
    log_to_file(f"Odpověď: {response.choices[0].message.content}")
    log_to_file(f"Tokeny: {response.usage.total_tokens}")
    
except Exception as e:
    log_to_file(f"\nChyba při připojení k OpenAI API: {e}")
    log_to_file("\nPodrobnosti chyby:")
    log_to_file(traceback.format_exc())

log_to_file("Test dokončen") 