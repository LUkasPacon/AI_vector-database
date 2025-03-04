import openai

# Zadejte API klíč přímo zde
api_key = "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"

print(f"Používám API klíč: {api_key[:8]}...{api_key[-4:]}")

try:
    # Inicializace klienta
    client = openai.OpenAI(api_key=api_key)
    
    # Jednoduchý test
    print("Odesílám požadavek na OpenAI API...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Řekni 'Ahoj, svět!' v češtině."}
        ]
    )
    
    # Výpis odpovědi
    print("\nÚspěšné připojení k OpenAI API!")
    print(f"Model: {response.model}")
    print(f"Odpověď: {response.choices[0].message.content}")
    print(f"Tokeny: {response.usage.total_tokens}")
    
except Exception as e:
    print(f"\nChyba při připojení k OpenAI API: {e}")
    import traceback
    traceback.print_exc() 