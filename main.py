from tkinter import *
import requests
from tkinter import messagebox
from datetime import datetime


# Funcion que muestra una nota
def mostrar_nota():
    response = requests.get("http://localhost:25030/nota/consultar", json={"id": nota_id.get()})
    nota = response.json()

    titulo_label.config(text=nota["titulo"])
    descripcion_text.delete(1.0, END)
    descripcion_text.insert(END, nota["descripcion"])
    fecha_label.config(text="Fecha de creación: " + obtener_fecha_formateada(nota["fecha"]))


# Funcion que obtiene la fecha formateada
def obtener_fecha_formateada(fecha):
    fecha_objeto = datetime.fromisoformat(fecha)
    dia = fecha_objeto.strftime("%d")
    mes = fecha_objeto.strftime("%m")
    anio = fecha_objeto.strftime("%Y")
    return f"{dia}-{mes}-{anio}"


# Funcion que identifica los campos de la nota para luego guardarlos en otro metodo
def guardar_nota_wrapper(titulo_entry, descripcion_text):
    guardar_nota(titulo_entry.get(), descripcion_text.get("1.0", END))


# Funcion que agrega una nota
def agregar_nota():
    global nueva_ventana
    nueva_ventana = Toplevel(window)
    nueva_ventana.title("Nueva Nota")
    nueva_ventana.geometry("400x300")

    # Crear elementos de la ventana
    titulo_label = Label(nueva_ventana, text="Título:", font=("Arial", 12))
    titulo_label.pack()
    titulo_entry = Entry(nueva_ventana, font=("Arial", 12))
    titulo_entry.pack()

    descripcion_label = Label(nueva_ventana, text="Descripción:", font=("Arial", 12))
    descripcion_label.pack()
    descripcion_text = Text(nueva_ventana, height=10, font=("Arial", 12))
    descripcion_text.pack()

    guardar_button = Button(nueva_ventana, text="Guardar", font=("Arial", 12),
                            command=lambda: guardar_nota_wrapper(titulo_entry, descripcion_text))
    guardar_button.pack()

    # Actualizar el menú de notas
    actualizar_menu_notas()


# Funcion que guarda una nota
def guardar_nota(titulo, descripcion):
    notaDTO = {"titulo": titulo, "descripcion": descripcion}

    response = requests.post("http://localhost:25030/nota/insertar", json=notaDTO)

    if response.status_code == 200:
        messagebox.showinfo("Nota Agregada", "La nota ha sido agregada exitosamente.")
        nueva_ventana.destroy()
        mostrar_notas()
    else:
        messagebox.showerror("Error", "Ocurrió un error al agregar la nota.")


# Funcion que elimina una nota
def eliminar_nota(titulo):
    notaDTO = {"titulo": titulo}
    response = requests.delete("http://localhost:25030/nota/eliminar", json=notaDTO)

    if response.status_code == 200:
        messagebox.showinfo("Nota Eliminada", "La nota ha sido eliminada exitosamente.")
        mostrar_notas()
    else:
        messagebox.showerror("Error", "Ocurrió un error al eliminar la nota.")


# Funcion que actualiza el menu de notas
def actualizar_nota(titulo, descripcion):
    global ventana_actualizar
    ventana_actualizar = Toplevel(window)
    ventana_actualizar.title("Actualizar Nota")
    ventana_actualizar.geometry("400x300")

    titulo_label = Label(ventana_actualizar, text="Título:", font=("Arial", 12))
    titulo_label.pack()
    titulo_entry = Entry(ventana_actualizar, font=("Arial", 12))
    titulo_entry.pack()
    titulo_entry.insert(END, titulo)

    descripcion_label = Label(ventana_actualizar, text="Descripción:", font=("Arial", 12))
    descripcion_label.pack()
    descripcion_text = Text(ventana_actualizar, height=10, font=("Arial", 12))
    descripcion_text.pack()
    descripcion_text.insert(END, descripcion)

    actualizar_button = Button(ventana_actualizar, text="Actualizar", font=("Arial", 12),
                               command=lambda: guardar_actualizacion(titulo_entry.get(),
                                                                     descripcion_text.get("1.0", END),
                                                                     descripcion_text))
    actualizar_button.pack()


# Funcion que guarda la actualizacion de una nota
def guardar_actualizacion(titulo, descripcion, descripcion_text):
    notaDTO = {"titulo": titulo, "descripcion": descripcion}

    response = requests.put("http://localhost:25030/nota/actualizar", json=notaDTO)

    if response.status_code == 200:
        messagebox.showinfo("Nota Actualizada", "La nota ha sido actualizada exitosamente.")
        ventana_actualizar.destroy()
        mostrar_notas()
    else:
        messagebox.showerror("Error", "Ocurrió un error al actualizar la nota.")


# Funcion que muestra las notas
def mostrar_notas():
    for frame in window.winfo_children():
        if frame != menu_frame:
            frame.destroy()

    response = requests.get("http://localhost:25030/nota/consultarTodos")
    notas = response.json()

    # Crear el canvas y el scrollbar
    canvas = Canvas(window, bg="white")
    scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for nota in notas:
        titulo = nota["titulo"]
        descripcion = nota["descripcion"]
        fecha = nota["fecha"]

        nota_frame = Frame(scrollable_frame, bg="white", padx=120, pady=50)
        nota_frame.pack(pady=10, padx=10, fill="both", expand=True)

        titulo_label = Label(nota_frame, text=titulo, font=("Arial", 14, "bold"), fg="navy")
        titulo_label.pack()

        descripcion_text = Text(nota_frame, height=5, width=30, font=("Arial", 12))
        descripcion_text.insert(END, descripcion)
        descripcion_text.pack(pady=5)

        fecha_label = Label(nota_frame, text="Fecha: " + obtener_fecha_formateada(fecha), font=("Arial", 10), fg="gray")
        fecha_label.pack()

        eliminar_button = Button(nota_frame, text="Eliminar", font=("Arial", 12),
                                 command=lambda titulo=titulo: eliminar_nota(titulo))
        eliminar_button.pack(side="left", padx=30, pady=20)

        actualizar_button = Button(nota_frame, text="Actualizar", font=("Arial", 12),
                                   command=lambda titulo=titulo, descripcion_text=descripcion_text: actualizar_nota(
                                       titulo, descripcion_text.get("1.0", END)))
        actualizar_button.pack(side="left", padx=50)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


# Funcion que actualiza el menu de notas
def actualizar_menu_notas():
    opciones_menu.delete(0, END)
    opciones_menu.add_command(label="Salir", command=window.quit)


window = Tk()
window.title("Notas")

# Establecer el tamaño de la ventana
window.geometry("560x600")
window.resizable(False, False)  # Prohibir redimensionar la ventana

# Fondo de la ventana
window.configure(bg="lightgray")

menu_frame = Frame(window)
menu_frame.pack(pady=10)

opciones_menu = Menu(window)
window.config(menu=opciones_menu)

agregar_button = Button(menu_frame, text="Agregar", font=("Arial", 12), command=agregar_nota)
agregar_button.pack(side="left")

salir_button = Button(menu_frame, text="Salir", font=("Arial", 12), command=window.quit)
salir_button.pack(side="left")

mostrar_notas()

window.mainloop()
