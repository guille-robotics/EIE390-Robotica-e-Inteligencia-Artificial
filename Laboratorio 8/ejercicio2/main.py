import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
import serial 
import time
from contextlib import asynccontextmanager # NUEVO: Importación para el ciclo de vida

# Variable global para el puerto serial
ser = None 

# --- NUEVO ESTÁNDAR DE FASTAPI: LIFESPAN (Ciclo de vida) ---
# Esta función maneja lo que pasa al prender y al apagar el servidor
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. LO QUE OCURRE AL INICIAR (Startup)
    global ser
    try:
        # Ajustar 'COM3' al puerto que corresponda
        ser = serial.Serial('COM3', 115200, timeout=1, dsrdtr=False)
        time.sleep(2) # Tiempo para que la conexión se estabilice
        print("Puerto serial abierto exitosamente por el Servidor.")
    except Exception as e:
        print(f"Advertencia: No se pudo abrir el puerto serial. Detalle: {e}")
        
    # El 'yield' pausa esta función y le dice a FastAPI: "Arranca la página web"
    yield 
    
    # 2. LO QUE OCURRE AL APAGAR (Shutdown) - Cuando presionamos Ctrl+C
    if ser is not None and ser.is_open:
        ser.close()
        print("Puerto serial cerrado correctamente.")
# -----------------------------------------------------------

# Instanciamos FastAPI y le pasamos nuestra función de ciclo de vida
app = FastAPI(lifespan=lifespan)

@app.get("/")
def cargar_interfaz():
    """Sirve la interfaz gráfica (HTML) al navegador"""
    return FileResponse("page/index.html")

@app.get("/led/{estado}")
def controlar_led(estado: str):
    """Recibe la orden desde la web y la envía por el puerto serial"""
    
    # Validación de seguridad
    if ser is None or not ser.is_open:
        print("Error: Se intentó enviar un comando, pero la Pico no está conectada.")
        return {"status": "Error de hardware: Puerto serial no disponible"}

    if estado == "1":
        ser.write(b'E') 
        mensaje = "Se envió el comando: Encender"
        print(mensaje) 
        
    elif estado == "0":
        ser.write(b'A') 
        mensaje = "Se envió el comando: Apagar"
        print(mensaje)
        
    else:
        mensaje = "Comando no válido"
        
    return {"status": mensaje}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)