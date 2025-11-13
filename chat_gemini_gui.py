#!/usr/bin/env python3
"""
Chat con Gemini Flash - Interfaz Gráfica Simple
"""

import os
import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox
from dotenv import load_dotenv
import google.generativeai as genai
import threading


class GeminiChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat con Gemini Flash")
        self.root.geometry("700x600")

        # Cargar variables de entorno
        load_dotenv()

        # Obtener API key y modelo
        api_key = os.getenv('GEMINI_API_KEY')
        model_name = os.getenv('GEMINI_FLASH_MODEL')

        if not api_key or not model_name:
            messagebox.showerror("Error", "No se encontraron las variables en .env")
            sys.exit(1)

        # Configurar Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.chat = self.model.start_chat(history=[])

        # Crear interfaz
        self.create_widgets()

    def create_widgets(self):
        # Área de chat
        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=("Arial", 11),
            bg="#f5f5f5",
            state=tk.DISABLED
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Configurar tags para colores
        self.chat_area.tag_config("user", foreground="#0066cc", font=("Arial", 11, "bold"))
        self.chat_area.tag_config("gemini", foreground="#00aa00", font=("Arial", 11, "bold"))
        self.chat_area.tag_config("system", foreground="#666666", font=("Arial", 10, "italic"))

        # Frame para entrada
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)

        # Campo de entrada
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="white"
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", lambda e: self.send_message())

        # Botón enviar
        self.send_button = tk.Button(
            input_frame,
            text="Enviar",
            command=self.send_message,
            font=("Arial", 11, "bold"),
            bg="#0066cc",
            fg="white",
            padx=20,
            cursor="hand2"
        )
        self.send_button.pack(side=tk.RIGHT)

        # Mensaje de bienvenida
        self.add_message("system", "Listo para conversar. Escribe tu mensaje...\n")

        # Focus en el campo de entrada
        self.input_field.focus()

    def add_message(self, tag, message):
        """Agregar mensaje al área de chat"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message, tag)
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def send_message(self):
        """Enviar mensaje al chat"""
        user_message = self.input_field.get().strip()

        if not user_message:
            return

        # Limpiar campo de entrada
        self.input_field.delete(0, tk.END)

        # Mostrar mensaje del usuario
        self.add_message("user", f"Tú: ")
        self.add_message("", f"{user_message}\n\n")

        # Deshabilitar botón mientras se procesa
        self.send_button.config(state=tk.DISABLED)
        self.input_field.config(state=tk.DISABLED)

        # Procesar en un hilo separado para no bloquear la UI
        thread = threading.Thread(target=self.get_response, args=(user_message,))
        thread.daemon = True
        thread.start()

    def get_response(self, user_message):
        """Obtener respuesta de Gemini"""
        try:
            # Enviar mensaje y obtener respuesta
            response = self.chat.send_message(user_message)

            # Mostrar respuesta
            self.root.after(0, self.add_message, "gemini", "Gemini: ")
            self.root.after(0, self.add_message, "", f"{response.text}\n\n")

        except Exception as e:
            error_msg = f"Error: {str(e)}\n\n"
            self.root.after(0, self.add_message, "system", error_msg)

        finally:
            # Rehabilitar botón y campo
            self.root.after(0, self.send_button.config, {"state": tk.NORMAL})
            self.root.after(0, self.input_field.config, {"state": tk.NORMAL})
            self.root.after(0, self.input_field.focus)


def main():
    root = tk.Tk()
    app = GeminiChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
