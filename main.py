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


def guardar_nota_wrapper(titulo_entry, descripcion_text):
    guardar_nota(titulo_entry.get(), descripcion_text.get("1.0", END))


def agregar_nota():
    global nueva_ventana
    nueva_ventana = Toplevel(window)
    nueva_ventana.title("Nueva Nota")
    nueva_ventana.geometry("400x300")

    # Crear elementos de la ventana
    titulo_label = Label(nueva_ventana, text="Título:")
    titulo_label.pack()
    titulo_entry = Entry(nueva_ventana)
    titulo_entry.pack()

    descripcion_label = Label(nueva_ventana, text="Descripción:")
    descripcion_label.pack()
    descripcion_text = Text(nueva_ventana, height=10)
    descripcion_text.pack()

    guardar_button = Button(nueva_ventana, text="Guardar",
                            command=lambda: guardar_nota_wrapper(titulo_entry, descripcion_text))
    guardar_button.pack()

    # Actualizar el menú de notas
    actualizar_menu_notas()


def guardar_nota(titulo, descripcion):
    notaDTO = {"titulo": titulo, "descripcion": descripcion}

    response = requests.post("http://localhost:25030/nota/insertar", json=notaDTO)

    if response.status_code == 200:
        messagebox.showinfo("Nota Agregada", "La nota ha sido agregada exitosamente.")
        nueva_ventana.destroy()
        mostrar_notas()
    else:
        messagebox.showerror("Error", "Ocurrió un error al agregar la nota.")


def eliminar_nota(titulo):
    notaDTO = {"titulo": titulo}
    response = requests.delete("http://localhost:25030/nota/eliminar", json=notaDTO)

    if response.status_code == 200:
        messagebox.showinfo("Nota Eliminada", "La nota ha sido eliminada exitosamente.")
        mostrar_notas()
    else:
        messagebox.showerror("Error", "Ocurrió un error al eliminar la nota.")


def mostrar_notas():
    for frame in window.winfo_children():
        if frame != menu_frame:
            frame.destroy()

    response = requests.get("http://localhost:25030/nota/consultarTodos")
    notas = response.json()

    # Crear el canvas y el scrollbar para hacer la lista de notas scrollable
    canvas = Canvas(window, bg="white")
    scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    # Configurar el scrollbar y el scrollregion del canvas
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

        # Crear un frame para cada nota
        nota_frame = Frame(scrollable_frame, bg="white", padx=120, pady=50)
        nota_frame.pack(pady=10, padx=10, fill="both", expand=True)

        titulo_label = Label(nota_frame, text=titulo, font=("Arial", 14, "bold"), fg="navy")
        titulo_label.pack(pady=(10, 5))

        descripcion_label = Label(nota_frame, text=descripcion, font=("Arial", 12), wraplength=200, justify="center")
        descripcion_label.pack(pady=(5, 10))  # Agregar espacio de separación después del texto de descripción

        fecha_label = Label(nota_frame, text=f"Fecha: {fecha}", font=("Arial", 10), fg="gray")
        fecha_label.pack(pady=(5, 20))

        eliminar_button = Button(nota_frame, text="Eliminar", command=lambda titulo=titulo: eliminar_nota(titulo))
        eliminar_button.pack()

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")


def actualizar_menu_notas():
    opciones_menu.delete(0, END)
    opciones_menu.add_command(label="Salir", command=window.quit)


window = Tk()
window.title("Notas")

# Establecer el tamaño de la ventana
window.geometry("400x600")

# Fondo de la ventana
window.configure(bg="lightgray")

menu_frame = Frame(window)
menu_frame.pack(pady=10)

opciones_menu = Menu(window)
window.config(menu=opciones_menu)

agregar_button = Button(menu_frame, text="Agregar", command=agregar_nota)
agregar_button.pack(side="left")

scrollable_frame = Frame(window)
scrollable_frame.pack(fill="both", expand=True)

canvas = Canvas(scrollable_frame, bg="white")
scrollbar = Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)

# Agregar el scrollbar al canvas
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

mostrar_notas()

window.mainloop()
