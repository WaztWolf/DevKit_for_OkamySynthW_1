import os
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso empaquetado."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def crear_estructura(carpeta_base):

    carpetas = [
        'OkamySynthW-1.0.0/Devkit',
        'OkamySynthW-1.0.0/Editor',
        'OkamySynthW-1.0.0/voicebank'
    ]
    
    for carpeta in carpetas:
        os.makedirs(os.path.join(carpeta_base, carpeta), exist_ok=True)

def seleccionar_ubicacion():
    carpeta_base = filedialog.askdirectory(title="Selecciona la ubicación para crear la estructura de carpetas")
    if carpeta_base:
        crear_estructura(carpeta_base)
        messagebox.showinfo("Creado", "La estructura de carpetas se creó con éxito.")
        messagebox.showinfo("Tip", "Recomendamos poner la herramienta 'DevKit_for_OSW' en la carpeta de 'DevKit'.")
    else:
        messagebox.showwarning("Advertencia", "No seleccionaste ninguna ubicación.")

root = tk.Tk()
root.title("S&F_Creator for OSW | Tool")
root.iconbitmap(resource_path("Assets/icon.ico"))

mensaje = tk.Label(root, text="Herramienta para crear la estructura del Sintesizador.", padx=20, pady=10)
mensaje.pack()

btn = tk.Button(root, text="Seleccionar Ubicación y Crear Estructura", command=seleccionar_ubicacion)
btn.pack(pady=20)

root.mainloop()
