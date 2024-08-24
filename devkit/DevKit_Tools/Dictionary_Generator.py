import tkinter as tk
from tkinter import filedialog, messagebox
import random
import sys
import os

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso empaquetado."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class DictionaryGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("GD for Okamy Synth W - Devkit")
        root.iconbitmap(resource_path("Assets/icon.ico"))

        # Variables
        self.duid = None

        # Widgets UI
        tk.Label(root, text="Tipo de diccionario:").grid(row=0, column=0, padx=10, pady=5)
        self.dic_type_var = tk.StringVar(value="0")
        tk.Radiobutton(root, text="Base", variable=self.dic_type_var, value="0").grid(row=0, column=1)
        tk.Radiobutton(root, text="Custom", variable=self.dic_type_var, value="1").grid(row=0, column=2)

        tk.Label(root, text="Idioma:").grid(row=1, column=0, padx=10, pady=5)
        self.language_var = tk.StringVar(value="0")
        tk.Radiobutton(root, text="Español", variable=self.language_var, value="0").grid(row=1, column=1)
        tk.Radiobutton(root, text="Inglés", variable=self.language_var, value="1").grid(row=1, column=2)
        tk.Radiobutton(root, text="Japonés", variable=self.language_var, value="2").grid(row=1, column=3)
        tk.Radiobutton(root, text="Multilenguaje", variable=self.language_var, value="3").grid(row=1, column=4)

        tk.Label(root, text="Vendor:").grid(row=2, column=0, padx=10, pady=5)
        self.vendor_var = tk.StringVar(value="0")
        tk.Radiobutton(root, text="Wazt Okami", variable=self.vendor_var, value="0").grid(row=2, column=1)
        tk.Radiobutton(root, text="No proporcionado", variable=self.vendor_var, value="1").grid(row=2, column=2)
        tk.Radiobutton(root, text="Otro", variable=self.vendor_var, value="2").grid(row=2, column=3)

        tk.Label(root, text="¿Es un diccionario base?").grid(row=4, column=0, padx=10, pady=5)
        self.is_base_var = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="Sí", variable=self.is_base_var).grid(row=4, column=1, columnspan=2)

        tk.Button(root, text="Generar DUID", command=self.generate_duid).grid(row=5, column=0, pady=10)
        self.duid_label = tk.Label(root, text="DUID: No generado")
        self.duid_label.grid(row=5, column=1, columnspan=2)

        tk.Label(root, text="Nombre del archivo:").grid(row=6, column=0, padx=10, pady=5)
        self.filename_var = tk.StringVar(value="dictionary")
        tk.Entry(root, textvariable=self.filename_var).grid(row=6, column=1, columnspan=2)

        tk.Button(root, text="Elegir ubicación y guardar", command=self.choose_location_and_save).grid(row=7, column=0, columnspan=3, pady=10)

    def generate_duid(self):
        product_code = random.randrange(0,99)

        """
        Genera el DUID basado en los parámetros seleccionados.
        """
        dic_type = self.dic_type_var.get()
        language = self.language_var.get()
        vendor = self.vendor_var.get()

        # Formatea el DUID
        self.duid = f"{dic_type}{language}{vendor}{product_code}"
        self.duid_label.config(text=f"DUID: {self.duid}")

    def generate_dictionary_content(self):
        """
        Genera el contenido del archivo de diccionario basado en el DUID y el tipo de diccionario.
        """
        if not self.duid:
            messagebox.showerror("Error", "Genera el DUID primero.")
            return

        is_base = self.is_base_var.get()
        if is_base:
            dictionary_content = f"""# Dictionary 2024
# DUID = {self.duid}
          
vowels:
    a
    e
    i
    o
    u
consonants:
    b
    d
    f
    g
    h
    j
    k
    l
    m
    n
    ny
    p
    q
    r
    rr
    s
    t
    v
    x
    w
    y
    z
breaths:
    br
    br1
aspirations:
    asp
    asp1
unvoiced:
    h
"""
        else:
            dictionary_content = f"""# Dictionary 2024
# DUID = {self.duid}
          
vowels:
consonants:
breaths:
aspirations:
unvoiced:
"""
        
        return dictionary_content

    def choose_location_and_save(self):
        """
        Muestra un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo, y guarda el diccionario.
        """
        dictionary_content = self.generate_dictionary_content()
        if not dictionary_content:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".dict",
            filetypes=[("Archivos de diccionario", "*.dict")],
            initialfile=self.filename_var.get()
        )

        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(dictionary_content)
                messagebox.showinfo("Éxito", f"Archivo de diccionario guardado como {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo de diccionario: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryGenerator(root)
    root.mainloop()
