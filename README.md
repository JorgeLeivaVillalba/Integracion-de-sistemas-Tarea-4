# Objetivos de la Tarea Actualizados: Monitor de Criptomonedas con WebSockets

**Formato de entrega:** GitHub o ZIP

El objetivo principal de esta tarea es que los alumnos demuestren su comprensión y habilidad para implementar comunicación en tiempo real utilizando WebSockets en un entorno de FastAPI.

**Puntaje Máximo:** 10 puntos

## Instrucciones

1. **Configuración Inicial:**
   - Crear un entorno virtual.
   - Instalar las dependencias:
    `python -m pip install -r requirements.txt`

---

## 1. Servir Contenido HTML Estático (0.5 puntos)

- Configurar un endpoint `GET (/)` en FastAPI para servir un archivo HTML (`crypto_monitor.html`).
- Asegurar que la ruta al archivo HTML sea robusta y funcione independientemente del directorio de ejecución del script.

---

## 2. Configurar Endpoint WebSocket (1.5 puntos)

- Crear un endpoint WebSocket (`/ws/crypto_prices`) en FastAPI.
- Aceptar y gestionar las conexiones de clientes al WebSocket.
- Implementar el manejo de desconexiones de clientes (`WebSocketDisconnect`).

---

## 3. Gestión de Conexiones Activas y Preferencias por Cliente (2 puntos)

- Mantener una estructura de datos (ej. un diccionario) que asocie cada conexión WebSocket activa con las preferencias de criptomonedas de ese cliente.
- Añadir una conexión con sus preferencias iniciales y removerla cuando se cierra.

---

## 4. Simulación de Datos en Tiempo Real (2 puntos)

- Implementar una tarea asincrónica de fondo (`send_crypto_prices_periodically`) que se ejecute de forma continua.
- Esta tarea debe generar datos simulados de precios para todas las criptomonedas disponibles (no solo las seleccionadas por defecto), de manera que el servidor pueda enviar solo las relevantes a cada cliente.
- Los datos simulados deben ser numéricos y variar ligeramente.

---

## 5. Difusión de Mensajes Personalizada por WebSocket (4 puntos)

- La tarea de fondo debe enviar los datos simulados a todos los clientes WebSocket actualmente conectados.
- Antes de enviar, filtrar los datos para enviar a cada cliente solo las criptomonedas que ese cliente ha seleccionado.
- Asegurar que los datos se envíen en formato JSON.
- Manejar posibles errores al enviar mensajes a conexiones que puedan haberse cerrado recientemente.

---

## 6. Historial Limitado de Precios (Tendencia) en el Cliente (**2 puntos extras**)

- En el lado del cliente (JavaScript), almacenar un historial limitado de los últimos X (ej. 5 o 10) precios para cada criptomoneda.
- Utilizar este historial para mostrar una indicación visual simple de la tendencia (ej. flecha verde/roja, cambio de color del precio) al actualizarse.