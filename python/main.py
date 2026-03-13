import serial
import threading
import queue
import time
import csv
from datetime import datetime
import dearpygui.dearpygui as dpg

PORTA_SERIALE = 'COM8' 
BAUD_RATE = 9600
FILE_CSV = "monitoraggio_energetico.csv"

coda_dati = queue.Queue()

def lettore_seriale():
    try:
        ser = serial.Serial(PORTA_SERIALE, BAUD_RATE, timeout=1)
        print(f"Connesso alla porta {PORTA_SERIALE}")
        while True:
            if ser.in_waiting > 0:
                linea = ser.readline().decode('utf-8').strip()
                if linea:
                    coda_dati.put((datetime.now().strftime("%H:%M:%S"), linea))
    except Exception as e:
        print(f"Errore nella comunicazione seriale: {e}")

class MonitorEnergia:
    def __init__(self):
        self.dati_temp_x = []
        self.dati_temp_y = []
        self.temp_corrente = 0.0
        self.umid_corrente = 0.0
        self.testo_stato = "In attesa di dati..."

    def aggiorna_logica(self):
        while not coda_dati.empty():
            timestamp, dati_grezzi = coda_dati.get()
            try:
                t, h = map(float, dati_grezzi.split(','))
                self.temp_corrente = t
                self.umid_corrente = h
                
                with open(FILE_CSV, mode='a', newline='') as f:
                    scrittore = csv.writer(f)
                    scrittore.writerow([timestamp, t, h])

                self.dati_temp_x.append(len(self.dati_temp_x))
                self.dati_temp_y.append(t)
                
                if t > 25:
                    self.testo_stato = "ATTENZIONE: Temperatura alta! Spegnere riscaldamento."
                elif 18 <= t <= 25:
                    self.testo_stato = "Comfort: Efficienza energetica ottimale."
                else:
                    self.testo_stato = "Temperatura bassa: Considera di isolare l'ambiente."

                dpg.set_value("testo_temp", f"Temperatura: {t} °C")
                dpg.set_value("testo_umid", f"Umidità: {h} %")
                dpg.set_value("etichetta_stato", self.testo_stato)
                dpg.set_value("serie_grafico", [self.dati_temp_x, self.dati_temp_y])
                
            except ValueError:
                print("Errore nel formato dati ricevuto")

monitor = MonitorEnergia()

dpg.create_context()
dpg.create_viewport(title='Sistema di Monitoraggio Energetico', width=800, height=600)

with dpg.window(label="Dashboard Ambientale", width=780, height=580):
    dpg.add_text("Monitoraggio in Tempo Reale", color=[0, 255, 0])
    dpg.add_separator()
    
    with dpg.group(horizontal=True):
        dpg.add_text("Stato:", tag="etichetta_stato")
    
    dpg.add_text("Temperatura: --", tag="testo_temp")
    dpg.add_text("Umidità: --", tag="testo_umid")
    
    with dpg.plot(label="Andamento Temperatura", height=300, width=-1):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, label="Campionamenti")
        with dpg.plot_axis(dpg.mvYAxis, label="Gradi Celsius"):
            dpg.add_line_series([], [], label="Temp", tag="serie_grafico")

dpg.setup_dearpygui()
dpg.show_viewport()

thread = threading.Thread(target=lettore_seriale, daemon=True)
thread.start()

while dpg.is_dearpygui_running():
    monitor.aggiorna_logica() 
    dpg.render_dearpygui_frame()

dpg.destroy_context()