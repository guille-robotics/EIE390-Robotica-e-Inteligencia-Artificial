import uvicorn
from fastapi import FastAPI

# Instanciamos la aplicación FastAPI
app = FastAPI()

# Definimos el endpoint raíz (GET)
@app.get("/")
def mensaje_bienvenida():
    """
    Este es un endpoint básico. Al ingresar a http://127.0.0.1:8000/
    el servidor retornará este diccionario que FastAPI convierte a JSON.
    """
    return {"estado": "Servidor FastAPI funcionando correctamente", "curso": "EIE 390"}

# Bloque principal de ejecución
if __name__ == "__main__":
    # Ejecutamos el servidor internamente usando uvicorn.run
    # Nota: Para usar reload=True, el nombre de la app debe ir entre comillas "main:app"
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)