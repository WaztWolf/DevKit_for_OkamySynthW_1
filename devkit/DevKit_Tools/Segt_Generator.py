import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso empaquetado."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class DevkitEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("GSEGT for Okamy Synth W - Devkit")
        root.iconbitmap(resource_path("Assets/icon.ico"))

        self.audio_path = None
        self.segt_path = None

        tk.Button(root, text="Seleccionar Audio", command=self.seleccionar_audio).pack(pady=10)
        tk.Button(root, text="Generar .segt", command=self.generar_segt).pack(pady=10)
        tk.Button(root, text="Cargar .segt", command=self.cargar_segt).pack(pady=10)

        self.text_area = tk.Text(root, height=20, width=80)
        self.text_area.pack(padx=10, pady=10)

        tk.Button(root, text="Guardar Cambios", command=self.guardar_segt).pack(pady=10)

        tk.Button(root, text="?", command=self.mostrar_ayuda).pack(side=tk.BOTTOM, pady=10)

    def seleccionar_audio(self):
        """
        Abre un cuadro de diálogo para seleccionar un archivo de audio.
        """
        self.audio_path = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=[("Archivos de audio", "*.wav")]
        )
        if self.audio_path:
            messagebox.showinfo("Audio Seleccionado", f"Archivo de audio seleccionado: {self.audio_path}")
        else:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ningún archivo de audio.")

    def generar_segt(self):
        """
        Genera un archivo .segt básico a partir del archivo de audio seleccionado.
        """
        if not self.audio_path:
            messagebox.showwarning("Advertencia", "Primero selecciona un archivo de audio.")
            return

        base_name = os.path.splitext(os.path.basename(self.audio_path))[0]
        
        segt_path = os.path.join(os.path.dirname(self.audio_path), base_name + '.segt')
        with open(segt_path, 'w') as f:
            f.write("# DUID = \n")
            f.write("transcription:\n")
            f.write("    []\n")  

        self.segt_path = segt_path
        messagebox.showinfo("Generación Completa", f"Archivo .segt generado: {self.segt_path}")

    def cargar_segt(self):
        """
        Abre un cuadro de diálogo para seleccionar un archivo .segt y carga su contenido en el editor.
        """
        self.segt_path = filedialog.askopenfilename(
            title="Seleccionar archivo .segt",
            filetypes=[("Archivos .segt", "*.segt")]
        )
        if self.segt_path:
            try:
                with open(self.segt_path, 'r') as f:
                    contenido = f.read()
                self.text_area.delete(1.0, tk.END)  
                self.text_area.insert(tk.END, contenido)
                messagebox.showinfo("Archivo Cargado", f"Archivo .segt cargado: {self.segt_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo .segt: {e}")
        else:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ningún archivo .segt.")

    def guardar_segt(self):
        """
        Guarda los cambios realizados en el archivo .segt.
        """
        if not self.segt_path:
            messagebox.showwarning("Advertencia", "Primero carga un archivo .segt para editar.")
            return

        contenido = self.text_area.get(1.0, tk.END)
        try:
            with open(self.segt_path, 'w') as f:
                f.write(contenido)
            messagebox.showinfo("Guardado Completo", f"Cambios guardados en: {self.segt_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los cambios: {e}")

    def mostrar_ayuda(self):
        """
        Muestra una ventana con información de ayuda.
        """
        ventana_ayuda = tk.Toplevel(self.root)
        ventana_ayuda.title("Ayuda")

        texto_ayuda = tk.Text(ventana_ayuda, height=15, width=60)
        texto_ayuda.pack(padx=10, pady=10)
        
        ayuda = (
            "Este Devkit permite generar y editar archivos .segt (transcripciones).\n\n"
            "1. Seleccionar Audio:\n"
            "   - Selecciona un archivo de audio (.wav o .mp3) para generar un archivo .segt.\n\n"
            "2. Generar .segt:\n"
            "   - Genera un archivo .segt básico con un encabezado DUID vacío y una transcripción de ejemplo.\n\n"
            "3. Cargar .segt:\n"
            "   - Carga un archivo .segt existente para editar su contenido.\n\n"
            "4. Guardar Cambios:\n"
            "   - Guarda los cambios realizados en el archivo .segt.\n\n"
            "El DUID es el valor que hay en el diccionario previamente generado\n"
            "con el Dictionary_Generator.py, el DUID se tiene que poner ahi.\n"
            "Dentro de los [] hay que poner los fonemas que se encuentran en el audio.\n"
            "Tienen que estar en el diccionario.\n"
            "Para más detalles, consulta la documentación."
        )

        texto_ayuda.insert(tk.END, ayuda)

if __name__ == "__main__":
    root = tk.Tk()
    app = DevkitEditor(root)
    root.mainloop()
