#!/usr/bin/env python3
"""
Chat interactivo con Gemini Flash a través de la terminal
"""

import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

def main():
    # Cargar variables de entorno
    load_dotenv()

    # Obtener API key y modelo
    api_key = os.getenv('GEMINI_API_KEY')
    model_name = os.getenv('GEMINI_FLASH_MODEL')

    if not api_key:
        print("❌ Error: GEMINI_API_KEY no encontrada en .env")
        sys.exit(1)

    if not model_name:
        print("❌ Error: GEMINI_FLASH_MODEL no encontrada en .env")
        sys.exit(1)

    # Configurar Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    # Iniciar chat
    chat = model.start_chat(history=[])

    print(f"💬 Chat con {model_name}")
    print("=" * 50)
    print("Escribe 'salir', 'exit' o 'quit' para terminar\n")

    try:
        while True:
            # Obtener input del usuario
            user_input = input("Tú: ").strip()

            if not user_input:
                continue

            # Verificar comandos de salida
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Hasta luego!")
                break

            try:
                # Enviar mensaje y obtener respuesta
                response = chat.send_message(user_input)
                print(f"\nGemini: {response.text}\n")

            except Exception as e:
                print(f"\n❌ Error al obtener respuesta: {e}\n")

    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
        sys.exit(0)

if __name__ == "__main__":
    main()
