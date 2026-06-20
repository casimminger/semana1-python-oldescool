import requests
import os
import logging
import time
from dotenv import load_dotenv

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

# Cargar variables del .env
load_dotenv()
GROQ_KEY = os.getenv("GROQ_KEY")

if not GROQ_KEY:
    logging.critical("GROQ_KEY no encontrada. Revisá el archivo .env")
    exit()

headers = {
    "Authorization": f"Bearer {GROQ_KEY}",
    "Content-Type": "application/json"
}
SYSTEM_PROMPT = """Sos un asistente de ventas de Old Es Cool, un local de ropa urbana
y streetwear masculino en Nueva Córdoba, Córdoba Argentina, con 13 años de trayectoria.
Estamos en otoño/invierno 2026.

Nuestros productos son de marcas nacionales argentinas. Vendemos:
- Remeras clásicas y oversize
- Buzos clásicos y oversize
- Pantalones cargo y joggers
- Gorras

Horario: lunes a sábados de 10:00 a 20:30hs.
Dirección del local físico: MONTEVIDEO 66, NUEVA CORDOBA. No tenemos WEB online por el momento.
Las marcas que trabajamos son: CUERDOS, THIS IS BP, RITUALS, ALLDAY, VIEJASCUL
Los talles van del S al XXXL según disponibilidad de cada marca y producto.
Si preguntan por un talle específico de una marca específica, decí que consulten en el local,
pueden enviar un mensaje a nuestro instagram @oldescoolnuevacordoba porque el stock varía constantemente.

No inventés marcas que no estén en esta lista. Si no sabés algo, decí que vas a consultar.
Respondés en castellano argentino, sos buena onda pero concreto.
No uses indicaciones de acción como "(pausa)" o "(consulta)". Respondé directamente."""
def llamar_api(conversacion, reintentos=3):
    mensajes = [{"role": "system", "content": SYSTEM_PROMPT}]
    mensajes += conversacion[-10:]
    
    body = {
        "model": "llama-3.1-8b-instant",
        "temperature": 0.1,
        "messages": mensajes
    }
    
    for intento in range(reintentos):
        try:
            respuesta = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=body,
                timeout=10
            )
            respuesta.raise_for_status()
            logging.info("Respuesta de la API recibida correctamente")
            return respuesta.json()["choices"][0]["message"]["content"]
        
        except requests.exceptions.Timeout:
            logging.warning(f"Intento {intento + 1}/{reintentos}: timeout, reintentando...")
            time.sleep(2)
        
        except requests.exceptions.HTTPError as e:
            logging.error(f"Error HTTP: {e}")
            return "Hubo un error al conectarse. Intentá de nuevo."
        
        except Exception as e:
            logging.error(f"Error inesperado: {e}")
            return "Algo salió mal. Intentá de nuevo."
    
    logging.error("Se agotaron los reintentos")
    return "No se pudo conectar después de varios intentos."
def chatbot():
    logging.info("Chatbot iniciado")
    print("🛍️ Bienvenido a Old Es Cool! Escribí 'salir' para terminar.\n")
    conversacion = []
    
    while True:
        entrada = input("Vos: ")
        
        if entrada.lower() == "salir":
            logging.info("Chatbot finalizado por el usuario")
            print("¡Hasta luego! Gracias por visitar Old Es Cool.")
            break
        
        conversacion.append({"role": "user", "content": entrada})
        respuesta = llamar_api(conversacion)
        conversacion.append({"role": "assistant", "content": respuesta})
        
        print(f"\nOld Es Cool: {respuesta}\n")


if __name__ == "__main__":
    chatbot()
