#!/usr/bin/env python3
"""
Chat con Gemini Flash - Adaptado para Vercel Serverless
"""

import os
import json
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Obtener API key y modelo desde variables de entorno
api_key = os.environ.get('GEMINI_API_KEY')
model_name = os.environ.get('GEMINI_FLASH_MODEL', 'gemini-2.5-flash')

# Configurar Gemini
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
else:
    model = None

# Almacenar sesiones de chat (en memoria - limitado en serverless)
chat_sessions = {}


@app.route('/')
def index():
    return render_template('chat.html', model_name=model_name)


@app.route('/send', methods=['POST'])
def send_message():
    if not model:
        return jsonify({'error': 'API key no configurada'}), 500

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

        return Response(
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


# Handler para Vercel
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
