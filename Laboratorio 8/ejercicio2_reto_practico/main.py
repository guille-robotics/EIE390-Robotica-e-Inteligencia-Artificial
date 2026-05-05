import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
import serial 
import time
from contextlib import asynccontextmanager

# Variable global inicializada de forma segura
ser = None 

# --- MANEJO DEL CICLO DE VIDA (Lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al iniciar el servidor
    global ser
    try:
        # Recuerda a los alumnos ajustar 'COM3' si es necesario
        ser = serial.Serial('COM3', 115200, timeout=1, dsrdtr=False)
        time.sleep(2)
        print(" Puerto serial abierto exitosamente.")
    except Exception as e:
        print(f" Advertencia: No se pudo abrir el puerto serial. Detalle: {e}")
        
    yield # Aquí el servidor web empieza a funcionar
    
    # Al apagar el servidor (Ctrl+C)
    if ser is not None and ser.is_open:
        ser.close()
        print(" Puerto serial cerrado correctamente.")
# -------------------------------------------

# Instanciamos la aplicación asignando el lifespan
app = FastAPI(lifespan=lifespan)

# Carga de la interfaz HTML
@app.get("/")
def cargar_interfaz():
    return FileResponse("page/index.html")

# ==========================================
# CÓDIGO BASE: Control del LED 1 (Pin GP15)
# ==========================================
@app.get("/led/{estado}")
def controlar_led_1(estado: str):
    
    # Validación de seguridad
    if ser is None or not ser.is_open:
        return {"status": "Error: Puerto serial no disponible"}

    if estado == "1":
        ser.write(b'E') 
        mensaje = "Se envió el comando: Encender LED 1"
    elif estado == "0":
        ser.write(b'A') 
        mensaje = "Se envió el comando: Apagar LED 1"
    else:
        mensaje = "Comando no válido para LED 1"
        
    print(mensaje)
    return {"status": mensaje}

# ==========================================
# RETO PRÁCTICO: Control del LED 2 (Pin GP14)
# ==========================================
@app.get("/led2/{estado}")
def controlar_led_2(estado: str):
    """
    Este nuevo endpoint escucha peticiones en la ruta /led2/.
    Envía comandos distintos ('X' e 'Y') para no interferir con el LED 1.
    """
    
    # Validación de seguridad replicada para el segundo actuador
    if ser is None or not ser.is_open:
        return {"status": "Error: Puerto serial no disponible"}

    if estado == "1":
        ser.write(b'X') 
        mensaje = "Se envió el comando: Encender LED 2"
    elif estado == "0":
        ser.write(b'Y') 
        mensaje = "Se envió el comando: Apagar LED 2"
    else:
        mensaje = "Comando no válido para LED 2"
        
    print(mensaje)
    return {"status": mensaje}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)