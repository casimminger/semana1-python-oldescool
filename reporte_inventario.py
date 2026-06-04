import requests
import csv

class Producto:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def valor_total(self):
        return self.precio * self.stock

    def mostrar(self):
        print(f"{self.nombre} - ${self.precio} - Stock: {self.stock} - Valor total: ${self.valor_total()}")

remera = Producto("remera", 12000, 5)
buzo = Producto("buzo", 15000, 8)
gorra = Producto("gorra", 8000, 12)

inventario = [remera, buzo, gorra]

respuesta = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
datos = respuesta.json()
tipo_cambio = datos["rates"]["ARS"]

print(f"Tipo de cambio: ${tipo_cambio}")

with open("reporte_inventario", "w", newline="") as archivo:
  escritor= csv.DictWriter(archivo, fieldnames=["nombre", "precio_ars", "precio_usd", "stock","valor_total"])
  escritor.writeheader()

  for producto in inventario:
    precio_usd = round(producto.precio / tipo_cambio, 2)
    escritor.writerow({
        "nombre": producto.nombre,
        "precio_ars": producto.precio,
        "precio_usd": precio_usd,
        "stock": producto.stock,
        "valor_total": producto.valor_total()
    })
print("reporte guardado en reporte_inventario.csv")

