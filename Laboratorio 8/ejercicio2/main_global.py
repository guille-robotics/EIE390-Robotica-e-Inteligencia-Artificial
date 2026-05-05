import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
import serial 
import time
from contextlib import asynccontextmanager 

# Variable global para el puerto serial
ser = None 

# --- MANEJO DEL CICLO DE VIDA (Lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global ser
    try:
        ser = serial.Serial('COM3', 115200, timeout=1, dsrdtr=False)
        time.sleep(2) 
        print("✅ Puerto serial abierto exitosamente por el Servidor.")
    except Exception as e:
        print(f"❌ Advertencia: No se pudo abrir el puerto serial. Detalle: {e}")
        
    yield 
    
    if ser is not None and ser.is_open:
        ser.close()
        print("🔌 Puerto serial cerrado correctamente.")
# -----------------------------------------------------------

app = FastAPI(lifespan=lifespan)

@app.get("/")
def cargar_interfaz():
    return FileResponse("page/index.html")

@app.get("/led/{estado}")
def controlar_led(estado: str):
    
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
    # ¡MODIFICACIÓN AQUÍ! 
    # host="0.0.0.0" permite que la API sea visible en tu red local (Wi-Fi/Ethernet)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)