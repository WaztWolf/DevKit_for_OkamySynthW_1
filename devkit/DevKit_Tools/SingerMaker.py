import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
import random
import re

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso empaquetado."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


class DeckitGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("GBV for Okamy Synth W - Devkit")
        root.iconbitmap(resource_path("Assets/icon.ico"))

        self.nombre_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.version_var = tk.StringVar(value="1.0.0")
        self.editor_version_var = tk.StringVar(value="1.0.0")
        self.lenguaje_var = tk.StringVar(value="0")
        self.vendor_var = tk.StringVar(value="0")
        self.editor_var = tk.StringVar(value="0")
        self.puid_var = tk.StringVar()
        self.dictionary_path_var = tk.StringVar()
        self.carpeta_seleccionada = ""

        tk.Label(root, text="Nombre del banco de voz:").pack(pady=5)
        tk.Entry(root, textvariable=self.nombre_var).pack(pady=5)

        tk.Label(root, text="Descripción:").pack(pady=5)
        tk.Entry(root, textvariable=self.descripcion_var).pack(pady=5)

        tk.Label(root, text="Versión:").pack(pady=5)
        tk.Entry(root, textvariable=self.version_var).pack(pady=5)

        tk.Label(root, text="Editor Versión:").pack(pady=5)
        tk.Entry(root, textvariable=self.editor_version_var).pack(pady=5)

        tk.Label(root, text="Lenguaje (0=Spanish, 1=English, 2=Japanese, 3=Multilenguaje):").pack(pady=5)
        tk.OptionMenu(root, self.lenguaje_var, "0", "1", "2", "3").pack(pady=5)

        tk.Label(root, text="Vendor (0=Wazt Okami, 1=Not Provided, 2=Other):").pack(pady=5)
        tk.OptionMenu(root, self.vendor_var, "0", "1", "2").pack(pady=5)

        tk.Label(root, text="Editor (0=W1, 1=UTAU Original, 2=VOCALOID Original):").pack(pady=5)
        tk.OptionMenu(root, self.editor_var, "0", "1", "2").pack(pady=5)

        tk.Button(root, text="Generar PUID", command=self.generar_puid).pack(pady=10)
        tk.Label(root, textvariable=self.puid_var).pack(pady=5)

        tk.Button(root, text="Seleccionar Carpeta de Destino", command=self.seleccionar_carpeta).pack(pady=10)
        self.seleccion_label = tk.Label(root, text="Ninguna carpeta seleccionada")
        self.seleccion_label.pack(pady=5)

        tk.Button(root, text="Seleccionar Diccionario", command=self.seleccionar_diccionario).pack(pady=10)
        tk.Label(root, textvariable=self.dictionary_path_var).pack(pady=5)

        tk.Button(root, text="Generar Banco de Voz", command=self.generar_banco_voz).pack(pady=10)

        tk.Button(root, text="?", command=self.abrir_ventana_explicaciones).pack(side=tk.BOTTOM, pady=10)

    def generar_puid(self):
        """
        Genera el PUID basado en las opciones seleccionadas.
        """
        zero1=0
        zero2=0
        lenguaje = self.lenguaje_var.get()
        vendor = self.vendor_var.get()
        editor = self.editor_var.get()
        productcode = random.randrange(1, 99)
        puid = f"{zero1}{lenguaje}{vendor}{editor}{zero2}{productcode:02}"
        self.puid_var.set(f"PUID generado: {puid}")
        return puid

    def seleccionar_carpeta(self):
        """
        Abre un cuadro de diálogo para seleccionar la carpeta donde se creará el banco de voz.
        """
        self.carpeta_seleccionada = filedialog.askdirectory()
        if self.carpeta_seleccionada:
            self.seleccion_label.config(text=f"Carpeta seleccionada: {self.carpeta_seleccionada}")
        else:
            self.seleccion_label.config(text="No se ha seleccionado ninguna carpeta")

    def seleccionar_diccionario(self):
        """
        Abre un cuadro de diálogo para seleccionar manualmente el diccionario que se usará.
        """
        diccionario_path = filedialog.askopenfilename(
            title="Seleccionar diccionario",
            filetypes=[("Archivos de diccionario", "*.dict")]
        )
        if diccionario_path:
            self.dictionary_path_var.set(f"Diccionario seleccionado: {diccionario_path}")
        else:
            self.dictionary_path_var.set("No se ha seleccionado ningún diccionario")

    def extraer_DUID(self):
        """
        Extrae el número DUID de la segunda línea de un archivo .dict seleccionado.
        """
        diccionario = self.dictionary_path_var.get().replace("Diccionario seleccionado: ", "")
    
        try:
            with open(diccionario, 'r') as archivo:
                lineas = archivo.readlines()

            if len(lineas) >= 2:
                segunda_linea = lineas[1]
                duid_match = re.search(r'DUID\s*=\s*(\d+)', segunda_linea)
                if duid_match:
                    self.duid = duid_match.group(1) 
                    print(f"DUID extraído: {self.duid}")
                    return self.duid
                else:
                    print("No se encontró el formato de DUID en la segunda línea.")
            else:
                print("El archivo no tiene suficientes líneas.")
        except FileNotFoundError:
            print("No se pudo abrir el archivo seleccionado.")

    def generar_banco_voz(self):
        """
        Crea la estructura del banco de voz en la carpeta seleccionada.
        """
        nombre = self.nombre_var.get()
        descripcion = self.descripcion_var.get()
        version = self.version_var.get()
        editor_version = self.editor_version_var.get()
        puid = self.generar_puid()
        carpeta = self.carpeta_seleccionada
        diccionario = self.dictionary_path_var.get().replace("Diccionario seleccionado: ", "")

        if not nombre or not carpeta:
            messagebox.showwarning("Advertencia", "Debes ingresar un nombre y seleccionar una carpeta.")
            return

        if not diccionario:
            messagebox.showwarning("Advertencia", "Debes seleccionar un diccionario.")
            return

        voicebank_folder = os.path.join(carpeta, nombre)
        samples_folder = os.path.join(voicebank_folder, "samples")
        os.makedirs(samples_folder, exist_ok=True)
        
        inf_path = os.path.join(voicebank_folder, "singer.inf")
        with open(inf_path, 'w') as inf_file:
            inf_file.write(f'name={nombre}\n')
            inf_file.write(f'version={version}\n')
            inf_file.write(f'editor-version={editor_version}\n')
            inf_file.write(f'descripcion={descripcion}\n')
            inf_file.write(f'dictionary={self.duid}\n')
            inf_file.write(f'dictionary-path="voicebank/{nombre}/dictionary.dict"\n')
            inf_file.write(f'samples="voicebank/{nombre}/samples"\n')
            inf_file.write(f'pitch_data="voicebank/{nombre}/pitch_data.csv"\n')
            inf_file.write(f'PUID={puid}\n')

        dict_path = os.path.join(voicebank_folder, "dictionary.dict")
        with open(diccionario, 'r') as original_dict:
            with open(dict_path, 'w') as new_dict:
                new_dict.write(original_dict.read())

        messagebox.showinfo("Éxito", f"Banco de voz '{nombre}' generado exitosamente en {carpeta}")

    def abrir_ventana_explicaciones(self):
        """
        Abre una ventana emergente con explicaciones o información adicional.
        """
        ventana_explicaciones = tk.Toplevel(self.root)
        ventana_explicaciones.title("Explicaciones")

        texto_explicaciones = """
        Explicaciones de GBV for Okamy Synth W - Devkit:
        GBV=Generador de Bancos de Voz(SOLO LA BASE)

        1. Nombre: Nombre del banco de voz que se va a crear.
        2. Descripción: Descripción opcional sobre el banco de voz.
        3. Versión: Versión del banco de voz.
        4. Editor Versión: Versión del editor utilizado para crear el banco de voz.
        5. Lenguaje: El lenguaje del banco de voz (0 = Español, 1 = Inglés, 2 = Japonés, 3 = Multilenguaje).
        6. Vendor: Indica quién es el autor del banco de voz.
        7. Editor: Selecciona el editor utilizado para las muestras (0 = W1, 1 = UTAU Original, 2 = VOCALOID Original).
        8. Diccionario: Selecciona manualmente el archivo .dict que contiene el diccionario fonético.
        """

        tk.Label(ventana_explicaciones, text=texto_explicaciones, justify="left", padx=10, pady=10).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = DeckitGenerator(root)
    root.mainloop()
