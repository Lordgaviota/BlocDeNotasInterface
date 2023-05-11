# Importacion de librerias
from tkinter import *
import requests


# Funciones para llamar a los metodos del controlador de Java
def mostrar_nota():
    # Realizar una petición GET a la API Java para consultar una nota
    response = requests.get("http://localhost:25030/nota/consultar", json={"id": nota_id.get()})
    nota = response.json()

    # Actualizar los campos de la interfaz con los datos de la nota
    titulo_label.config(text=nota["titulo"])
    descripcion_text.delete(1.0, END)
    descripcion_text.insert(END, nota["descripcion"])
    fecha_label.config(text="Fecha de creación: " + nota["fecha"])


# Resto del código para crear la interfaz gráfica...
window = Tk()
window.title("Notas")

# Agregar un campo de texto para ingresar el ID de la nota
nota_id_label = Label(window, text="ID de la nota")
nota_id_label.pack()
nota_id = Entry(window)
nota_id.pack()

# Agregar un botón "Mostrar Nota" que llama a la función mostrar_nota
mostrar_button = Button(window, text="Mostrar Nota", command=mostrar_nota)
mostrar_button.pack()

# Agregar un campo de texto para mostrar el título de la nota
titulo_label = Label(window, text="Título")
titulo_label.pack()

# Agregar un campo de texto para mostrar la descripción de la nota
descripcion_text = Text(window)
descripcion_text.pack()

# Agregar una etiqueta para mostrar la fecha de creación de la nota
fecha_label = Label(window, text="")
fecha_label.pack()

# El método mainloop() es usado cuando su aplicación está lista para correr.
# mainloop() es un bucle infinito usado para ejecutar la aplicación, esperando
window.mainloop()
