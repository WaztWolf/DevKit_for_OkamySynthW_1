import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import subprocess
import os
import sys
import shutil  # Necesario para copiar archivos

class AppLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Okamy Synth W Devkit 1.0.0")

        self.root.iconbitmap(self.resource_path("devkit/DevKit_Tools/Assets/icon.ico"))

        self.show_splash_screen()

    def resource_path(self, relative_path):
        """Obtiene la ruta absoluta al recurso empaquetado."""
        try:
            base_path = sys._MEIPASS  
        except Exception:
            base_path = os.path.dirname(__file__) 
        return os.path.join(base_path, relative_path)

    def show_splash_screen(self):
        splash = tk.Toplevel(self.root)
        splash.title("Cargando...")
        splash.geometry("600x500")
        
        splash.iconbitmap(self.resource_path("devkit/DevKit_Tools/Assets/Bot_2.png"))

        img = Image.open(self.resource_path("devkit/DevKit_Tools/Assets/Bot_2.png"))
        img = img.resize((600, 450), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        img_label = tk.Label(splash, image=img)
        img_label.image = img
        img_label.pack()

        label = tk.Label(splash, text="Okamy Synth V Devkit 1.0.0 loading...", font=("Arial", 14))
        label.pack(pady=10)

        splash.after(3500, lambda: self.show_main_menu(splash))

    def show_main_menu(self, splash):
        splash.destroy()

        self.root.geometry("700x675")
        tk.Label(self.root, text="Okamy Synth W Devkit Tools", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Generacion y Edicion del diccionario", font=("Arial", 12)).pack(pady=7)
        tk.Button(self.root, text="Generar Diccionario", command=self.open_dictionary_generator, width=30).pack(pady=5)
        tk.Button(self.root, text="Editar Diccionario", command=self.open_dicedit, width=30).pack(pady=5)
        tk.Label(self.root, text="Generacion del modelo de Voicebank", font=("Arial",12)).pack(pady=7)
        tk.Button(self.root, text="Generar modelo", command=self.open_singer_creator, width=30).pack(pady=5)
        tk.Label(self.root, text="Generacion de las transcripciones del Voicebank", font=("Arial", 12)).pack(pady=7)
        tk.Button(self.root, text="Generador de transcripciones", command=self.open_transgen, width=30).pack(pady=5)
        tk.Label(self.root, text="Segmentar los samples para el Voicebank", font=("Arial", 12)).pack(pady=7)
        tk.Button(self.root, text="Herramienta de segmentacion v3", command=self.open_segtool, width=30).pack(pady=5)
        tk.Label(self.root, text="Informacion de tu Voicebank", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Información de Cantante", command=self.open_singer_info, width=30).pack(pady=5)
        tk.Label(self.root, text="Guardas segmentacion de audio .csv", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Herramienta de guardado .csv", command=self.open_save_csv, width=30).pack(pady=5)
        tk.Label(self.root, text="Generar estructura del Sintesizador", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Herramienta automatica", command=self.open_struct_creator, width=30).pack(pady=5)

        tk.Label(self.root, text="Documentación/Documentation", font=("Arial", 12)).pack(pady=10)
        
        tk.Button(self.root, text="Documentacion ES", command=self.copy_file1, width=20).pack(pady=5)
        tk.Button(self.root, text="Documentation EN", command=self.copy_file2, width=20).pack(pady=5)

    def copy_file(self, source_path):
        destination_folder = filedialog.askdirectory(title="Seleccionar carpeta de destino")
        if destination_folder:
            try:
                shutil.copy(source_path, destination_folder)
                messagebox.showinfo("Éxito", f"Archivo copiado a {destination_folder}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo copiar el archivo.\nError: {e}")

    def copy_file1(self):
        source_path = self.resource_path("devkit\DevKit_Tools\Documentation\OSW-Docs-ES.pdf")  
        self.copy_file(source_path)

    def copy_file2(self):
        source_path = self.resource_path("devkit\DevKit_Tools\Documentation\OSW-Docs-EN.pdf")  
        self.copy_file(source_path)

    def open_transgen(self):
        self.run_script(self.resource_path("devkit/DevKit_Tools/Segt_Generator.py"))
    
    def open_save_csv(self):
        self.run_script(self.resource_path("devkit/DevKit_Tools/Compile_Segments.py"))

    def open_segtool(self):
        self.run_script(self.resource_path("devkit/DevKit_Tools/PhonemeSegmenter_v3.py"))

    def open_segtoolv2(self):
        self.run_script(self.resource_path("devkit/DevKit_Tools/PhonemeSegmenter_v2.py"))

    def open_dicedit(self):
        self.run_script(self.resource_path("devkit/DevKit_Tools/Dictionary_Editor.py"))

    def open_dictionary_generator(self):
        self.run_script(self.resource_path("devkit/DevKit_Tools/Dictionary_Generator.py"))

    def open_singer_info(self):
        self.run_script(self.resource_path("devkit/DevKit_Tools/SingerInfo.py"))

    def open_singer_creator(self):
        self.run_script(self.resource_path("devkit/DevKit_Tools/SingerMaker.py"))

    def open_struct_creator(self):
        self.run_script(self.resource_path("devkit/DevKit_Tools/Generate_Structure.py"))

    def run_script(self, script_name):
        try:
            file_path = self.resource_path(script_name)
            subprocess.Popen(["python", file_path], shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir {script_name}.\nError: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppLauncher(root)
    root.mainloop()
