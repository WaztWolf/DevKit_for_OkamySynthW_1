import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import sys
import os

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso empaquetado."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class SingerInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cargador de Informacion de Cantante")
        root.iconbitmap(resource_path("Assets/icon.ico"))
        
        self.select_button = tk.Button(root, text="Seleccionar archivo singer.inf", command=self.seleccionar_archivo)
        self.select_button.pack(pady=20)

    def seleccionar_archivo(self):
        ruta_inf = filedialog.askopenfilename(
            title="Selecciona el archivo singer.inf",
            filetypes=[("Archivos INF", "*.inf")],
            defaultextension=".inf"
        )
        
        if ruta_inf:
            try:
                self.info = self.leer_singer_inf(ruta_inf)
                self.mostrar_informacion()
                self.cargar_diccionario()
                self.cargar_segmentacion()
                if 'PUID' in self.info:
                    self.descomponer_puid(self.info['PUID'])
                if 'dictionary' in self.info:
                    self.descomponer_duid(self.info['dictionary'])
            except Exception as e:
                messagebox.showerror("Error", f"Error al leer el archivo: {e}")

    def leer_singer_inf(self, ruta_inf):
        info = {}
        if not os.path.isfile(ruta_inf):
            raise FileNotFoundError(f"No se encontro el archivo {ruta_inf}")

        with open(ruta_inf, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea or linea.startswith('#'):
                    continue

                try:
                    clave, valor = linea.split('=', 1)
                    clave = clave.strip()
                    valor = valor.strip().strip('"')
                    info[clave] = valor
                except ValueError:
                    raise ValueError(f"Error al procesar la linea: {linea}")

        return info

    def cargar_diccionario(self):
        diccionario_path = self.info.get('dictionary-path', None)
        if not diccionario_path or not os.path.isfile(diccionario_path):
            raise FileNotFoundError(f"No se encontro el diccionario en {diccionario_path}")

        self.diccionario = {}
        with open(diccionario_path, 'r') as f:
            seccion = None
            for linea in f:
                linea = linea.strip()
                if linea.endswith(':'):
                    seccion = linea[:-1]
                    self.diccionario[seccion] = []
                elif linea and seccion:
                    self.diccionario[seccion].append(linea)

    def cargar_segmentacion(self):
        samples_path = self.info.get('samples', None)
        if not samples_path or not os.path.isdir(samples_path):
            raise FileNotFoundError(f"No se encontro la carpeta de samples en {samples_path}")

        self.segmentacion = {}
        for archivo in os.listdir(samples_path):
            if archivo.endswith('.seg'):
                ruta_seg = os.path.join(samples_path, archivo)
                try:
                    self.procesar_segmentacion(ruta_seg)
                except Exception as e:
                    print(f"Error al procesar {ruta_seg}: {e}")

    def procesar_segmentacion(self, ruta_seg):
        if not os.path.isfile(ruta_seg):
            raise FileNotFoundError(f"No se encontro el archivo {ruta_seg}")

        print(f"Procesando archivo: {ruta_seg}")

        with open(ruta_seg, 'r') as archivo:
            lineas = archivo.readlines()
            
            if len(lineas) <= 1:
                print("El archivo no contiene datos de segmentacion válidos.")
                return
            
            encabezado = lineas[0]
            
            for linea in lineas[1:]:
                linea = linea.strip()
                if not linea or ',' not in linea:
                    continue  

                try:
                    partes = linea.split(',', 4)
                    fonema = partes[0].strip().strip("'")
                    fonema = fonema.strip("'")
                    
                    if fonema:
                        print(f"Fonema encontrado: {fonema}")

                        if fonema not in self.segmentacion:
                            self.segmentacion[fonema] = 0
                        self.segmentacion[fonema] += 1
                except (IndexError, ValueError) as e:
                    print(f"Error al procesar la linea: {linea}. Excepcion: {e}")

        print(f"Conteo actual de fonemas: {self.segmentacion}")

    def mostrar_informacion(self):
        ventana_info = tk.Toplevel(self.root)
        ventana_info.title("Informacion del Cantante")

        texto_info = scrolledtext.ScrolledText(ventana_info, width=60, height=20)
        texto_info.pack(padx=10, pady=10)

        texto_info.insert(tk.END, "Informacion del Cantante:\n")
        texto_info.insert(tk.END, f"Nombre: {self.info.get('name', 'Desconocido')}\n")
        texto_info.insert(tk.END, f"Version: {self.info.get('version', 'Desconocida')}\n")
        texto_info.insert(tk.END, f"Version del Editor: {self.info.get('editor-version', 'Desconocida')}\n")
        texto_info.insert(tk.END, f"DUID del Diccionario: {self.info.get('dictionary', 'Desconocido')}\n")
        texto_info.insert(tk.END, f"Ruta del Diccionario: {self.info.get('dictionary-path', 'Desconocida')}\n")
        texto_info.insert(tk.END, f"Ruta de los Samples: {self.info.get('samples', 'Desconocida')}\n")
        texto_info.insert(tk.END, f"Ruta del archivo de guardado de tonos: {self.info.get('pitch_data', 'Desconocida')}\n")
        
        if 'PUID' in self.info:
            puid_info = self.descomponer_puid(self.info['PUID'])
            texto_info.insert(tk.END, "\nInformacion del PUID:\n")
            for clave, valor in puid_info.items():
                texto_info.insert(tk.END, f"{clave}: {valor}\n")

        if 'dictionary' in self.info:
            duid_info = self.descomponer_duid(self.info['dictionary'])
            texto_info.insert(tk.END, "\nInformacion del DUID:\n")
            for clave, valor in duid_info.items():
                texto_info.insert(tk.END, f"{clave}: {valor}\n")

        boton_fonemas = tk.Button(ventana_info, text="Mostrar Fonemas Segmentados", command=self.mostrar_fonemas)
        boton_fonemas.pack(pady=10)

        texto_info.config(state=tk.DISABLED)

    def descomponer_puid(self, puid):
        """
        Descompone el PUID en su estructura codificada y devuelve un diccionario con la informacion descompuesta.
        """
        if not puid or len(puid) != 8:
            raise ValueError("El PUID debe ser un codigo de 8 caracteres.")

        info = {}
        
        try:
            pi = puid[:5]
            pc = puid[5:]
            
            languages = ["Spanish", "English", "Japanese", "Multilenguaje"]
            vendors = ["Wazt Okami", "Not Provided", "Other"]
            editors = ["W1", "Utau Original", "Vocaloid Original"]

            info["Language"] = languages[int(pi[0])]
            info["Vendor"] = vendors[int(pi[1])]
            info["Editor"] = editors[int(pi[2])]
            
            editor_version = pi[3:]
            if editor_version.startswith('0'):
                editor_version = editor_version.lstrip('0')

            if editor_version:
                editor_version = str(int(editor_version))

            info["Editor Version"] = editor_version
            info["Product Code"] = pc

        except (IndexError, ValueError) as e:
            raise ValueError(f"Error al descomponer el PUID: {e}")
        
        return info

    def descomponer_duid(self, duid):
        """
        Descompone el DUID en su estructura codificada y devuelve un diccionario con la informacion descompuesta.
        """
        if not duid or len(duid) != 5:
            raise ValueError("El DUID debe ser un codigo de 5 caracteres.")

        info = {}

        try:
            dsc = duid[:3] 
            product = duid[3:]  
            
            tipo = int(dsc[0])
            idioma = int(dsc[1])
            proveedor = int(dsc[2])

            tipos = ["Base", "Custom"]
            idiomas = ["Spanish", "English", "Japanese", "Multilenguaje"]
            proveedores = ["Wazt Okami", "Not Provided", "Other"]

            info["Tipo"] = tipos[tipo]
            info["Idioma"] = idiomas[idioma]
            info["Proveedor"] = proveedores[proveedor]
            info["Product Code"] = product

        except (IndexError, ValueError) as e:
            raise ValueError(f"Error al descomponer el DUID: {e}")
        
        return info

    def mostrar_fonemas(self):
        ventana_fonemas = tk.Toplevel(self.root)
        ventana_fonemas.title("Fonemas Segmentados")

        tree = ttk.Treeview(ventana_fonemas, columns=("Fonema", "Cantidad"), show='headings')
        tree.heading("Fonema", text="Fonema")
        tree.heading("Cantidad", text="Cantidad")
        tree.pack(padx=10, pady=10)

        fonemas_diccionario = sum(
            [self.diccionario.get(seccion, []) for seccion in ['vowels', 'consonants', 'breaths', 'aspirations', 'unvoiced']],
            []
        )
        
        fonemas_segmentados = {fonema: self.segmentacion.get(fonema, 0) for fonema in fonemas_diccionario}

        for fonema in fonemas_diccionario:
            cantidad = fonemas_segmentados.get(fonema, 0)
            tree.insert("", tk.END, values=(fonema, cantidad))

if __name__ == "__main__":
    root = tk.Tk()
    app = SingerInfoApp(root)
    root.mainloop()
