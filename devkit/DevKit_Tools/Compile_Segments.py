import pandas as pd
import os
from tkinter import filedialog, Tk, Text, Button, messagebox
import tkinter
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso empaquetado."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class SegToCsvApp:
    def __init__(self, root):
        self.root = root
        self.root.title("STCSV-SEG | Devkit for Okamy Synth W")
        self.csv_file_path = None
        root.iconbitmap(resource_path("Assets/icon.ico"))
        
        tkinter.Label(root, text="Abrir el archivo .seg, aunque te pedira el archivo .csv que si no tienes tendras", font=("Arial", 10)).pack(pady=10)
        tkinter.Label(root, text="que crearlo y llamarlo 'pitch_data' y se seleccionara.", font=("Arial", 10)).pack(pady=10)
        tkinter.Label(root, text="Luego tendras que seleccionar el archivo .seg del cual quieres añadir la informacion.", font=("Arial", 10)).pack(pady=10)

        self.select_seg_button = Button(root, text="Seleccionar archivo .seg", command=self.process_file)
        self.select_seg_button.pack()

        self.text_area = Text(root, height=30, width=100)
        self.text_area.pack()

    def select_or_create_csv_file(self):
        self.csv_file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        if not self.csv_file_path:
            self.csv_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

            if self.csv_file_path:
                self.create_new_csv(self.csv_file_path)
                messagebox.showinfo("Información", "Archivo CSV creado exitosamente.")
        else:
            self.update_text_area()

    def create_new_csv(self, csv_file_path):
        header = ['fonema', 'path', 'tiempo_inicio', 'tiempo_fin', 'pitch', 'pitch_midi']
        df = pd.DataFrame(columns=header)
        df.to_csv(csv_file_path, mode='w', header=True, index=False)

    def update_text_area(self):
        try:
            if self.csv_file_path and os.path.exists(self.csv_file_path):
                df = pd.read_csv(self.csv_file_path)
                self.text_area.delete(1.0, "end")
                self.text_area.insert("end", df.to_string(index=False))
            else:
                self.text_area.delete(1.0, "end")
                self.text_area.insert("end", "No se ha seleccionado ningún archivo CSV.")
        except pd.errors.EmptyDataError:
            self.text_area.delete(1.0, "end")
            self.text_area.insert("end", "El archivo CSV está vacío o no tiene columnas válidas.")

    def process_file(self):
        if not self.csv_file_path:
            self.select_or_create_csv_file()

        if not self.csv_file_path:
            return

        seg_file_path = filedialog.askopenfilename(filetypes=[("SEG Files", "*.seg")])
        if not seg_file_path:
            return
        
        self.process_seg_to_csv(seg_file_path, self.csv_file_path)
        self.update_text_area()

    def process_seg_to_csv(self, seg_file_path, csv_file_path):
        with open(seg_file_path, 'r') as seg_file:
            lines = seg_file.readlines()

        audio_file = None
        data_lines = []
        header = ['fonema', 'path', 'tiempo_inicio', 'tiempo_fin', 'pitch', 'pitch_midi']

        for i, line in enumerate(lines):
            line = line.strip()

            if i < 2:
                continue

            if line.startswith('# seg for'):
                audio_file = line.replace('# seg for ', '').strip()
                continue

            if len(line) > 0:
                parts = line.split(',')
                if len(parts) == 6:
                    fonema = parts[0].strip()
                    path = audio_file if audio_file else parts[1].strip()  # Usa audio_file si está disponible
                    tiempo_inicio = parts[2].strip()
                    tiempo_fin = parts[3].strip()
                    pitch = parts[4].strip()
                    pitch_midi = parts[5].strip()
                    
                    data_lines.append([fonema, path, tiempo_inicio, tiempo_fin, pitch, pitch_midi])

        if not data_lines:
            print("No se encontraron datos válidos en el archivo .seg")
            return

        df = pd.DataFrame(data_lines, columns=header)

        if os.path.exists(csv_file_path):
            existing_df = pd.read_csv(csv_file_path)
            
            if existing_df.columns.tolist() == header:
                df.to_csv(csv_file_path, mode='a', header=False, index=False)
            else:
                df.to_csv(csv_file_path, mode='a', header=True, index=False)
        else:
            df.to_csv(csv_file_path, mode='w', header=True, index=False)

if __name__ == "__main__":
    root = Tk()
    app = SegToCsvApp(root)
    root.mainloop()
