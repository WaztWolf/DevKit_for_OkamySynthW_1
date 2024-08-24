import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import sys
import os

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso empaquetado."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class DictionaryEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Dictionary Editor")
        root.iconbitmap(resource_path("Assets/icon.ico"))

        self.root.geometry("600x400")

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Abrir Diccionario", command=self.open_file, width=15).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Guardar", command=self.save_file, width=15).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Guardar como...", command=self.save_as_file, width=15).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Salir", command=self.root.quit, width=15).grid(row=0, column=3, padx=5)

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Courier New", 12))
        self.text_area.pack(expand=1, fill=tk.BOTH)

        self.current_file = None

    def open_file(self):
        """
        Función para abrir un archivo de diccionario (.dict) y cargarlo en el editor.
        """
        file_path = filedialog.askopenfilename(
            defaultextension=".dict",
            filetypes=[("Archivos de diccionario", "*.dict"), ("Todos los archivos", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()

                self.text_area.delete(1.0, tk.END)  
                self.text_area.insert(tk.END, content)  
                self.current_file = file_path  
                self.root.title(f"Dictionary Editor - {file_path}")  

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

    def save_file(self):
        """
        Función para guardar el archivo actual si ya se ha abierto.
        """
        if self.current_file:
            try:
                with open(self.current_file, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END))  

                messagebox.showinfo("Guardado", f"Archivo guardado: {self.current_file}")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        """
        Función para guardar el archivo con un nuevo nombre.
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".dict",
            filetypes=[("Archivos de diccionario", "*.dict"), ("Todos los archivos", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END))  

                self.current_file = file_path  
                self.root.title(f"Dictionary Editor - {file_path}")  

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryEditor(root)
    root.mainloop()
