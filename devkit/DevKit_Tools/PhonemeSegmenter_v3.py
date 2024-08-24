import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext
import numpy as np
import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Slider
import sys
import librosa
import math

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso empaquetado."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class EditorFonemas:
    def __init__(self, root):
        self.root = root
        self.root.title("Segmentador de Fonemas v3 | Okamy Synth W DevKit W1")
        root.iconbitmap(resource_path("Assets/icon.ico"))

        self.audio = None
        self.samplerate = None
        self.segmentos = []
        self.inicio_segmento = None
        self.fin_segmento = None
        self.reproduciendo = False
        self.tiempo_actual = 0
        self.zoom_nivel = 1
        self.fonemas = []
        self.fonema_index = 0
        self.pitch = None 
        self.mostrar_pitch = False

        self.select_audio_button = tk.Button(root, text="Seleccionar archivo de audio", command=self.cargar_audio)
        self.select_audio_button.pack(pady=10)

        self.load_transcription_button = tk.Button(root, text="Cargar Transcripción de Fonemas", command=self.cargar_transcripcion)
        self.load_transcription_button.pack(pady=10)

        self.toggle_pitch_button = tk.Button(root, text="Alternar Pitch/Audio", command=self.toggle_pitch)
        self.toggle_pitch_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Guardar Segmentación", command=self.guardar_segmentacion)
        self.save_button.pack(pady=10)

        self.info_text = scrolledtext.ScrolledText(root, width=60, height=15)
        self.info_text.pack(padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(pady=10)

        self.slider_ax = self.fig.add_axes([0.1, 0.1, 0.8, 0.03], facecolor='lightgoldenrodyellow')
        self.slider = Slider(self.slider_ax, 'Tiempo', 0, 1, valinit=0)
        self.slider.on_changed(self.actualizar_posicion)

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)

    def cargar_audio(self):
        ruta_audio = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=[("Archivos de audio", "*.wav")]
        )
        
        if ruta_audio:
            self.audio, self.samplerate = sf.read(ruta_audio)
            self.ruta_audio = os.path.relpath(ruta_audio)
            self.info_text.insert(tk.END, f"Archivo de audio cargado:\n {self.ruta_audio}\n")
            
            self.calcular_pitch()

            self.mostrar_audio()

    def calcular_pitch(self):
        """Calcula el pitch (frecuencia fundamental) usando librosa."""
        audio_mono = librosa.to_mono(self.audio.T)

        pitches, magnitudes = librosa.core.piptrack(y=audio_mono, sr=self.samplerate)

        self.pitch = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch_value = pitches[index, t]
            if pitch_value > 0:
                self.pitch.append(pitch_value)
            else:
                self.pitch.append(np.nan)

        self.info_text.insert(tk.END, "Pitch calculado.\n")

    def calcular_pitch_segmento(self, segmento):
        """Calcula el pitch promedio en el segmento seleccionado."""
        inicio_muestra = int(segmento['inicio'] * self.samplerate)
        fin_muestra = int(segmento['fin'] * self.samplerate)
        segmento_audio = self.audio[inicio_muestra:fin_muestra]
        
        pitches, magnitudes = librosa.core.piptrack(y=segmento_audio, sr=self.samplerate)
        pitch_values = pitches[magnitudes > np.median(magnitudes)]
        
        if len(pitch_values) > 0:
            pitch_promedio = np.mean(pitch_values)
        else:
            pitch_promedio = 0
        return pitch_promedio

    def pitch_a_midi(self, pitch):
        """Convierte el pitch (Hz) a una nota MIDI y devuelve la nota y el rango."""
        if pitch <= 0:
            return '0', 0
        nota_midi = int(69 + 12 * math.log2(pitch / 440.0))
        notas = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        nota = notas[nota_midi % 12]
        rango = (nota_midi // 12) - 1
        return nota, rango

    def cargar_transcripcion(self):
        ruta_transcripcion = filedialog.askopenfilename(
            title="Seleccionar archivo de transcripción",
            filetypes=[("Archivos de transcripción", "*.segt")]
        )
        
        if ruta_transcripcion:
            self.fonemas = self.leer_transcripcion_segt(ruta_transcripcion)
            self.fonema_index = 0
            self.info_text.insert(tk.END, f"Transcripción cargada:\n {ruta_transcripcion}\n")
            self.info_text.insert(tk.END, f"Fonemas a segmentar:\n {self.fonemas}\n")

    def leer_transcripcion_segt(self, ruta_segt):
        fonemas = []
        with open(ruta_segt, 'r') as f:
            for linea in f:
                if 'transcription:' in linea:
                    fonemas = next(f).strip().split()
                    fonemas = [fonema.strip('[]') for fonema in fonemas]
                    break
        return fonemas

    def mostrar_audio(self):
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        self.tiempo = np.linspace(0., len(self.audio) / self.samplerate, len(self.audio))
        self.ax.plot(self.tiempo, self.audio, label='Audio')
        self.ax.set_title('Visualización del Audio')
        self.ax.set_xlabel('Tiempo [s]')
        self.ax.set_ylabel('Amplitud')

        if self.mostrar_pitch and self.pitch is not None:
            tiempo_pitch = np.linspace(0., len(self.audio) / self.samplerate, len(self.pitch))
            self.ax.plot(tiempo_pitch, self.pitch, label='Pitch', color='orange')

        for segmento in self.segmentos:
            self.ax.axvline(segmento['inicio'], color='blue', linestyle='--', linewidth=1)
            self.ax.axvline(segmento['fin'], color='red', linestyle='--', linewidth=1)
            self.ax.text(segmento['inicio'], max(self.audio), f"{segmento['fonema']}", color='red', verticalalignment='center')

        self.linea_reproduccion, = self.ax.plot([], [], color='red', linestyle='--', label='Posición Actual')
        self.ax.legend()

        self.slider_ax.clear()
        self.slider_ax = self.fig.add_axes([0.1, 0.1, 0.8, 0.03], facecolor='lightgoldenrodyellow')
        self.slider = Slider(self.slider_ax, 'Tiempo', 0, len(self.audio) / self.samplerate, valinit=0)
        self.slider.on_changed(self.actualizar_posicion)
        
        self.canvas.draw()

    def toggle_pitch(self):
        self.mostrar_pitch = not self.mostrar_pitch
        self.mostrar_audio()

    def onclick(self, event):
        if event.xdata is None:
            return

        if self.inicio_segmento is None:
            self.inicio_segmento = event.xdata
            self.info_text.insert(tk.END, f'Inicio del segmento: {self.inicio_segmento:.3f}s\n')
        else:
            self.fin_segmento = event.xdata
            self.info_text.insert(tk.END, f'Fin del segmento: {self.fin_segmento:.3f}s\n')

            if self.fonema_index < len(self.fonemas):
                etiqueta = self.fonemas[self.fonema_index]
                segmento = {
                    'fonema': etiqueta,
                    'inicio': self.inicio_segmento,
                    'fin': self.fin_segmento
                }
                
                pitch_promedio = self.calcular_pitch_segmento(segmento)
                nota_midi, rango = self.pitch_a_midi(pitch_promedio)
                segmento['pitch_promedio'] = pitch_promedio
                segmento['nota_midi'] = f"{nota_midi}{rango + 1}"
                
                self.segmentos.append(segmento)
                self.info_text.insert(tk.END, f'Segmento añadido: {etiqueta} ({self.inicio_segmento:.3f}s - {self.fin_segmento:.3f}s) | Pitch Promedio: {pitch_promedio:.2f} Hz | Nota MIDI: {nota_midi}{rango + 1}\n')

                self.ax.axvspan(self.inicio_segmento, self.fin_segmento, color='green', alpha=0.3)
                self.ax.axvline(self.inicio_segmento, color='blue', linestyle='--', linewidth=1)
                self.ax.axvline(self.fin_segmento, color='red', linestyle='--', linewidth=1)
                self.ax.text(self.inicio_segmento, max(self.audio), f"{etiqueta}", color='blue', verticalalignment='bottom')
                self.canvas.draw()

                self.fonema_index += 1

                if self.fonema_index == len(self.fonemas):
                    self.info_text.insert(tk.END, "Todos los fonemas han sido segmentados.\n")

            self.inicio_segmento = None
            self.fin_segmento = None

    def on_key(self, event):
        if event.key == ' ':
            if self.reproduciendo:
                self.detener_audio()
            else:
                self.reproducir_audio()

    def on_scroll(self, event):
        if event.button == 'up':
            self.zoom(0.8)
        elif event.button == 'down':
            self.zoom(1.2)

    def zoom(self, factor):
        xlim = self.ax.get_xlim()
        centro = (xlim[0] + xlim[1]) / 2
        rango_actual = xlim[1] - xlim[0]
        nuevo_rango = rango_actual * factor
        self.ax.set_xlim([centro - nuevo_rango / 2, centro + nuevo_rango / 2])
        self.canvas.draw()

    def reproducir_audio(self):
        if self.audio is None or self.samplerate is None:
            return

        self.info_text.insert(tk.END, f'Reproduciendo desde {self.tiempo_actual:.3f}s\n')
        self.reproduciendo = True
        self.audio_reproducido = self.audio[int(self.tiempo_actual * self.samplerate):]
        sd.play(self.audio_reproducido, samplerate=self.samplerate)

    def detener_audio(self):
        self.info_text.insert(tk.END, 'Audio pausado\n')
        self.reproduciendo = False
        sd.stop()

    def actualizar_posicion(self, val):
        if not self.reproduciendo:
            self.tiempo_actual = self.slider.val
            self.linea_reproduccion.set_xdata([self.tiempo_actual, self.tiempo_actual])
            self.canvas.draw()

    def guardar_segmentacion(self):
        if self.audio is None or self.samplerate is None or len(self.audio) == 0:
            messagebox.showwarning("Advertencia", "No hay audio cargado.")
            return

        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar Segmentación",
            defaultextension=".seg",
            filetypes=[("Archivos SEG", "*.seg")]
        )

        if ruta_salida:
            with open(ruta_salida, 'w') as f:
                f.write(f"# seg for {self.ruta_audio}\n")
                f.write("fonema,audio,tiempo_inicio,tiempo_fin,pitch,pitch_midi\n")
                for segmento in self.segmentos:
                    fonema_limpio = segmento['fonema'].strip('[]')
                    f.write(f"{fonema_limpio},{self.ruta_audio},{segmento['inicio']:.3f},{segmento['fin']:.3f},{segmento['pitch_promedio']:.2f},{segmento['nota_midi']}\n")
            messagebox.showinfo("Guardar Segmentación", f"Segmentación guardada en: {ruta_salida}")

if __name__ == "__main__":
    root = tk.Tk()
    editor = EditorFonemas(root)
    root.mainloop()
