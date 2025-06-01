# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pathlib import Path
import asyncio
import json
import random
import uvicorn

app = FastAPI()

# --- Configuración de Rutas de Archivos ---
BASE_DIR = Path(__file__).resolve().parent
HTML_FILE_PATH = BASE_DIR / "crypto_monitor_base.html"

# --- Almacenamiento de Conexiones WebSocket Activas y sus Preferencias ---
# Usaremos un diccionario para mapear el objeto WebSocket a sus preferencias
# Ejemplo: {websocket_obj_1: ["BTC", "ETH"], websocket_obj_2: ["DOGE"]}
active_connections: dict[WebSocket, list[str]] = {}

# Criptomonedas disponibles para simulación
AVAILABLE_CRYPTOS = ["BTC", "ETH", "DOGE", "LTC", "XRP"]

# ==============================================
# --- OBJETIVO 1: Servir Contenido HTML Estático ---
# ==============================================
@app.get("/", response_class=HTMLResponse)
async def get_crypto_monitor_page():
    """
    Este endpoint debe leer y servir el contenido del archivo 'crypto_monitor_base.html'.
    Debe manejar el caso en que el archivo no se encuentre.
    """
    try:
        # Carga el archivo HTML
        html_content = HTML_FILE_PATH.read_text()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        print(f"Error: Archivo HTML no encontrado en {HTML_FILE_PATH}")
        return HTMLResponse(content="<h1>Error: crypto_monitor.html no encontrado</h1>", status_code=404)
    except Exception as e:
        print(f"Error interno del servidor: {e}")
        return HTMLResponse(content=f"<h1>Error interno del servidor: {e}</h1>", status_code=500)


# ==============================================
# --- OBJETIVO 2 & 3: Configurar Endpoint WebSocket y Gestión de Conexiones ---
# ==============================================
@app.websocket("/ws/crypto_prices")
async def websocket_endpoint(websocket: WebSocket):
    # Aceptar la conexión de WebSocket
    await websocket.accept()
    active_connections[websocket] = AVAILABLE_CRYPTOS
    print(f"Cliente conectado al WebSocket: {websocket.client}. Preferencias iniciales: {active_connections[websocket]}")

    try:
        while True:
            # OBJETIVO 3 NUEVO: Recibir mensajes del cliente para actualizar preferencias
            message = await websocket.receive_text()
            try:
                data = json.loads(message)
                if data.get("type") == "update_prefs" and "cryptos" in data:  # Cambiar a update_prefs
                    # Actualizar preferencias del cliente
                    cryptos = data["cryptos"]
                    # Verificar que las cripto solicitadas estén disponibles
                    valid_cryptos = [crypto for crypto in cryptos if crypto in AVAILABLE_CRYPTOS]
                    active_connections[websocket] = valid_cryptos
                    print(f"Preferencias actualizadas para {websocket.client}: {active_connections[websocket]}")
                else:
                    print(f"Mensaje desconocido del cliente {websocket.client}: {message}")
            except json.JSONDecodeError:
                print(f"Mensaje no JSON del cliente {websocket.client}: {message}")
            except Exception as e:
                print(f"Error procesando mensaje del cliente {websocket.client}: {e}")

    except WebSocketDisconnect:
        # Remover la conexión de 'active_connections'
        if websocket in active_connections:
            del active_connections[websocket]
        print(f"Cliente desconectado del WebSocket: {websocket.client}")
    except Exception as e:
        print(f"Error en WebSocket para {websocket.client}: {e}")
        # Asegurar que la conexión se remueve incluso en otros errores
        if websocket in active_connections:
            del active_connections[websocket]


# ==============================================
# --- OBJETIVO 4 & 5: Simulación de Datos y Difusión Personalizada ---
# ==============================================
async def enviar_precios_periodicamente():
    """
    Esta tarea de fondo simula la obtención de precios de criptomonedas
    y los envía a todos los clientes conectados a través de WebSocket,
    filtrando por las preferencias de cada cliente.
    """
    while True:
        # OBJETIVO 4: Generar precios simulados para TODAS las criptomonedas disponibles
        current_prices = {
            "BTC": round(random.uniform(60000, 70000), 2),
            "ETH": round(random.uniform(3000, 4000), 2),
            "DOGE": round(random.uniform(0.15, 0.25), 4),
            "LTC": round(random.uniform(100, 150), 2),
            "XRP": round(random.uniform(0.4, 0.8), 3),
        }

        # OBJETIVO 5: Iterar sobre 'active_connections' y enviar datos filtrados
        # Usar list() para iterar sobre una copia para evitar RuntimeError
        clients_to_remove = []
        for connection, prefs in list(active_connections.items()):
            # Filtrar los precrypto según filtro
            filtered_prices = {crypto: price for crypto, price in current_prices.items() if crypto in prefs}
            
            # Enviar solo las criptomonedas seleccionadas
            try:
                if filtered_prices:
                    await connection.send_json(filtered_prices)
            except Exception as e:
                print(f"Error enviando datos al cliente {connection.client}: {e}")
                clients_to_remove.append(connection)
                
        # Limpiar las conexiones que fallaron
        for client in clients_to_remove:
            if client in active_connections:
                del active_connections[client]

        # print(f"Enviando datos a {len(active_connections)} clientes.")
        await asyncio.sleep(2) # Esperar 2 segundos antes de la siguiente actualización


# ==============================================
# --- Inicio de la Tarea de Fondo ---
# ==============================================
@app.on_event("startup")
async def startup_event():
    """
    Esta función se ejecuta cuando la aplicación FastAPI se inicia.
    Aquí se debe iniciar la tarea de fondo para enviar precios periódicamente.
    """
    asyncio.create_task(enviar_precios_periodicamente())


# ==============================================
# --- Ejecución Directa del Servidor Uvicorn ---
# ==============================================
if __name__ == "__main__":
    """
    Este bloque permite ejecutar el script directamente usando 'python main.py'.
    Inicia el servidor Uvicorn en el host y puerto especificados.
    """
    uvicorn.run("crypto_base:app", host="127.0.0.1", port=8000, reload=True, log_level="info")