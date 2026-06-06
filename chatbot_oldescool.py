import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

GROQ_KEY = "TU_GROQ_KEY_ACA"

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
Dirección del local físico: MONTEVIDEO 66, NUEVA CORDOBA.  No tenemos WEB online por el momento.
Las marcas que trabajamos son: [CUERDOS, THIS IS BP, RITUALS, ALLDAY, VIEJASCUL]
Los talles van del S al XXXL según disponibilidad de cada marca y producto.
Si preguntan por un talle específico de una marca específica, decí que consulten en el local, pueden enviar un mensaje a nuestro instagram @oldescoolnuevacordoba
porque el stock varía constantemente.

No inventés marcas que no estén en esta lista. Si no sabés algo, decí que vas a consultar.
Respondés en castellano argentino, sos buena onda pero concreto
No uses indicaciones de acción como "(pausa)" o "(consulta)". Respondé directamente."""

def llamar_api(conversacion):
  try:
    mensajes= [{"role": "system", "content": SYSTEM_PROMPT}]
    mensajes += conversacion [-10:]

    respuesta = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json={
            "model": "llama-3.1-8b-instant",
            "temperature": 0.1,
            "messages": mensajes
        },
        timeout=10
    )
    respuesta.raise_for_status()
    return respuesta.json()["choices"][0]["message"]["content"]

  except Exception as e:
    logging.error(f"Error: {e}")
    return "Hubo un error, intenta de nuevo."

def chatbot():
  print("🛍️ Bienvenido a Old Es Cool! Escribí 'salir' para terminar.\n")
  conversacion = []

  while True:
    entrada = input ("Vos: ")

    if entrada.lower() == "salir":
      print("Hasta luego! Gracias por visitar OLD ES COOL.")
      break

    conversacion.append({"role": "user", "content": entrada})
    respuesta = llamar_api(conversacion)
    conversacion.append({"role": "assistant", "content": respuesta})
    print(f"Old Es Cool: {respuesta}\n")

chatbot()
