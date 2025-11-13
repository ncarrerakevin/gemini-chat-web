#!/bin/bash

# Script para ejecutar el chat con interfaz gráfica

# Activar entorno virtual
source venv/bin/activate

# Ejecutar la interfaz gráfica
python chat_gemini_gui.py

# Desactivar entorno virtual al salir
deactivate
