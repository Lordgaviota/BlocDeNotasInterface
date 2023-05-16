from tkinter import *
import requests
from tkinter import messagebox


def mostrar_nota():
    response = requests.get("http://localhost:25030/nota/consultar", json={"id": nota_id.get()})
    nota = response.json()

    titulo_label.config(text=nota["titulo"])
    descripcion_text.delete(1.0, END)
    descripcion_text.insert(END, nota["descripcion"])
    fecha_label.config(text="Fecha de creación: " + nota["fecha"])


def guardar_nota_wrapper(ventana, titulo_entry, descripcion_text):
    guardar_nota(ventana, titulo_entry.get(), descripcion_text.get("1.0", END))


def agregar_nota():
    nueva_ventana = Toplevel(window)
    nueva_ventana.title("Nueva Nota")

    titulo_label = Label(nueva_ventana, text="Título:")
    titulo_label.pack()
    titulo_entry = Entry(nueva_ventana)
    titulo_entry.pack()

    descripcion_label = Label(nueva_ventana, text="Descripción:")
    descripcion_label.pack()
    descripcion_text = Text(nueva_ventana)
    descripcion_text.pack()

    guardar_button = Button(nueva_ventana, text="Guardar", command=lambda: guardar_nota_wrapper(nueva_ventana, titulo_entry, descripcion_text))
    guardar_button.pack()

    # Actualizar el menú de notas
    actualizar_menu_notas()


def guardar_nota(ventana, titulo, descripcion):
    notaDTO = {"titulo": titulo, "descripcion": descripcion}

    response = requests.post("http://localhost:25030/nota/insertar", json=notaDTO)

    if response.status_code == 200:
        messagebox.showinfo("Nota Agregada", "La nota ha sido agregada exitosamente.")
        ventana.destroy()
        mostrar_notas()
    else:
        messagebox.showerror("Error", "Ocurrió un error al agregar la nota.")


def mostrar_notas():
    for frame in window.winfo_children():
        if frame != menu_frame:
            frame.destroy()

    response = requests.get("http://localhost:25030/nota/consultarTodos")
    notas = response.json()

    for nota in notas:
        titulo = nota["titulo"]
        descripcion = nota["descripcion"]
        fecha = nota["fecha"]

        nota_frame = Frame(window, bg="white", padx=120, pady=50)
        nota_frame.pack(pady=10, padx=10, fill="both", expand=True)

        titulo_label = Label(nota_frame, text=titulo, font=("Arial", 14, "bold"), fg="navy")
        titulo_label.pack()

        descripcion_label = Label(nota_frame, text=descripcion, font=("Arial", 12), wraplength=400, justify="left")
        descripcion_label.pack(pady=5)

        fecha_label = Label(nota_frame, text=f"Fecha: {fecha}", font=("Arial", 10), fg="gray")
        fecha_label.pack()


def actualizar_menu_notas():
    opciones_menu.delete(0, "end")
    opciones_menu.add_command(label="Salir", command=window.quit)


window = Tk()
window.title("Notas")

# Fondo de la ventana
window.configure(bg="lightgray")

menu_frame = Frame(window)
menu_frame.pack()

agregar_button = Button(menu_frame, text="Agregar", command=agregar_nota)
agregar_button.pack(side="left")

mostrar_notas()

window.mainloop()