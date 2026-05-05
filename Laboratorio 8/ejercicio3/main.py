import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
import serial 
import time
from contextlib import asynccontextmanager

ser = None 
ultimo_valor_sensor = "0"

@asynccontextmanager
async def lifespan(app: FastAPI):
    global ser
    try:
        # dsrdtr=False y rtscts=False ayudan a que la Pico no se resetee al conectar
        ser = serial.Serial('COM3', 115200, timeout=0.1, dsrdtr=False, rtscts=False)
        time.sleep(1) 
        # Limpiamos todo lo que Thonny pudo haber dejado pendiente
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        print("✅ Puerto serial conectado y buffer limpio.")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        
    yield 
    
    if ser is not None and ser.is_open:
        ser.close()
        print("🔌 Puerto cerrado.")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def cargar_interfaz():
    return FileResponse("page/index.html")

@app.get("/sensor")
def leer_sensor():
    global ultimo_valor_sensor
    
    if ser is not None and ser.is_open:
        try:
            # Si hay datos acumulados (más de 10 bytes), limpiamos para buscar el último
            if ser.in_waiting > 0:
                # Leemos todas las líneas acumuladas
                lineas = ser.readlines() 
                if lineas:
                    # Extraemos la última línea válida
                    ultima_linea = lineas[-1].decode('utf-8').strip()
                    
                    # Verificamos que sea un número (para evitar errores de decodificación)
                    if ultima_linea.isdigit():
                        ultimo_valor_sensor = ultima_linea
                        print(f"Dato fresco: {ultimo_valor_sensor}") # Mira tu terminal de VS Code
        except Exception as e:
            print(f"Error de lectura: {e}")
            
    return {"valor": ultimo_valor_sensor}

if __name__ == "__main__":
    # IMPORTANTE: Prueba con reload=False una vez para descartar conflictos de procesos
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)