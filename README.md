# Chat con Sans - Undertale Style

Chat interactivo con Gemini Flash que simula una conversación con Sans de Undertale.

## Características

💀 **Personalidad de Sans**: El modelo responde como Sans, con sus juegos de palabras, humor relajado y referencias a física

⚡ **Streaming en tiempo real**: Las respuestas aparecen palabra por palabra, como Character.AI

🎭 **Animación facial**: La cara de Sans se muestra al lado y su boca se mueve mientras habla

🔊 **Sonido de Undertale**: Reproduce el característico sonido "beep" de Undertale con cada palabra

## Instalación

```bash
# Crear entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

### Versión Web (Recomendada)
```bash
./chat_web.sh
```

Luego abre tu navegador en: **http://localhost:5001**

**Nota**: Haz clic en cualquier parte de la página para activar el audio (requerido por los navegadores modernos)

### Versión Terminal
```bash
./chat.sh
```

## Configuración

Las variables de entorno están en el archivo `.env`:

- `GEMINI_API_KEY`: Tu API key de Google Gemini
- `GEMINI_FLASH_MODEL`: Modelo a usar (gemini-2.5-flash)

## Ajustes

### Velocidad del streaming
Modifica el delay en `chat_gemini_web.py` línea 71:
```python
time.sleep(0.03)  # 30ms entre palabras (actual)
time.sleep(0.01)  # Más rápido
time.sleep(0.05)  # Más lento
```

### Tono del sonido
Modifica la frecuencia en `templates/chat.html` línea 353:
```javascript
oscillator.frequency.value = 100 + Math.random() * 50;  // Actual (grave para Sans)
oscillator.frequency.value = 200 + Math.random() * 100; // Más agudo
```

## Tecnologías

- **Backend**: Python + Flask + Google Gemini API
- **Frontend**: HTML + CSS + JavaScript (Vanilla)
- **Audio**: Web Audio API
- **Streaming**: Server-Sent Events (SSE)

## Autor

Creado con Claude Code
