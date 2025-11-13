#!/usr/bin/env python3
"""
Chat con Gemini Flash - Interfaz Web Simple
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

# Cargar variables de entorno
load_dotenv()

# Configurar Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Obtener API key y modelo
api_key = os.getenv('GEMINI_API_KEY')
model_name = os.getenv('GEMINI_FLASH_MODEL')

if not api_key or not model_name:
    print("Error: Variables de entorno no encontradas")
    exit(1)

# Configurar Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name)

# Almacenar sesiones de chat (en memoria)
chat_sessions = {}


@app.route('/')
def index():
    return render_template('chat.html', model_name=model_name)


@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')

    if not user_message:
        return jsonify({'error': 'Mensaje vacío'}), 400

    try:
        # Crear o recuperar sesión de chat
        if session_id not in chat_sessions:
            # Inicializar chat con personalidad de Sans
            chat_sessions[session_id] = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": ["A partir de ahora, eres Sans de Undertale. REGLAS: 1) Respuestas MUY CORTAS (máximo 2-3 oraciones), 2) Usa *asteriscos* para énfasis y acciones, 3) Haz juegos de palabras con huesos, 4) Usa 'eh', 'meh', 'nah' frecuentemente, 5) Habla relajado y casual, 6) Llámame 'compadre' o 'kid', 7) Haz referencias ocasionales a física. Ejemplo: 'eh, qué tal compadre. *guiño* todo bien por aquí. jeje.' NO digas que eres una IA."]
                },
                {
                    "role": "model",
                    "parts": ["eh, entendido compadre. respuestas cortas con *énfasis*. listo."]
                }
            ])

        chat = chat_sessions[session_id]

        # Función generadora para streaming palabra por palabra
        def generate():
            try:
                import time
                response = chat.send_message(user_message, stream=True)

                for chunk in response:
                    if chunk.text:
                        # Dividir en palabras y enviar una por una
                        words = chunk.text.split(' ')
                        for i, word in enumerate(words):
                            # Agregar espacio después de cada palabra excepto la última
                            if i < len(words) - 1:
                                yield f"data: {word} \n\n"
                            else:
                                yield f"data: {word}\n\n"
                            time.sleep(0.08)  # Delay más largo para que se vea mejor

                yield "data: [DONE]\n\n"
            except Exception as e:
                yield f"data: [ERROR]{str(e)}\n\n"

        return app.response_class(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no'
            }
        )

    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/clear', methods=['POST'])
def clear_chat():
    data = request.json
    session_id = data.get('session_id', 'default')

    if session_id in chat_sessions:
        del chat_sessions[session_id]

    return jsonify({'success': True})


if __name__ == '__main__':
    print(f"🚀 Abriendo chat con {model_name}")
    print("📱 Accede desde: http://localhost:5001")
    print("🛑 Presiona Ctrl+C para detener\n")
    app.run(debug=True, port=5001)
