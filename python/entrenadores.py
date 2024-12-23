from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson import ObjectId
import subprocess


MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PUERTO}/"
MONGO_BASEDATOS = "Europa_League"
MONGO_COLECCION = "entrenadores"


try:
    cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
    baseDatos = cliente[MONGO_BASEDATOS]
    coleccion = baseDatos[MONGO_COLECCION]
    print("Conexión exitosa a MongoDB.")
except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
    print(f"Error: {errorTiempo}")
except pymongo.errors.ConnectionFailure as errorConexion:
    print(f"Error de conexión: {errorConexion}")


def actualizar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)
    for documento in coleccion.find():
        tabla.insert("", "end", text=str(documento["_id"]), values=(
            documento.get("nombre", ""),
            documento.get("edad", ""),
            documento.get("nacionalidad", ""),
            documento.get("experiencia", ""),
            documento.get("equipo_actual", "")
        ))


def agregar_entrenador():
    if entry_nombre.get() and entry_edad.get() and entry_nacionalidad.get() and entry_experiencia.get() and entry_equipo.get():
        coleccion.insert_one({
            "nombre": entry_nombre.get(),
            "edad": int(entry_edad.get()),
            "nacionalidad": entry_nacionalidad.get(),
            "experiencia": entry_experiencia.get(),
            "equipo_actual": entry_equipo.get()
        })
        actualizar_tabla()
        limpiar_campos()
    else:
        messagebox.showerror("Error", "Rellena todos los campos.")


def eliminar_entrenador():
    seleccionado = tabla.focus()
    if seleccionado:
        id_entrenador = tabla.item(seleccionado)["text"]
        coleccion.delete_one({"_id": ObjectId(id_entrenador)})
        actualizar_tabla()
    else:
        messagebox.showerror("Error", "Selecciona un entrenador para eliminar.")


def actualizar_entrenador():
    seleccionado = tabla.focus()
    if seleccionado:
        id_entrenador = tabla.item(seleccionado)["text"]
        nuevo_nombre = entry_nombre.get()
        nueva_edad = entry_edad.get()
        nueva_nacionalidad = entry_nacionalidad.get()
        nueva_experiencia = entry_experiencia.get()
        nuevo_equipo = entry_equipo.get()

        if nuevo_nombre and nueva_edad and nueva_nacionalidad and nueva_experiencia and nuevo_equipo:
            coleccion.update_one(
                {"_id": ObjectId(id_entrenador)},
                {"$set": {
                    "nombre": nuevo_nombre,
                    "edad": int(nueva_edad),
                    "nacionalidad": nueva_nacionalidad,
                    "experiencia": nueva_experiencia,
                    "equipo_actual": nuevo_equipo
                }}
            )
            actualizar_tabla()
            limpiar_campos()
        else:
            messagebox.showerror("Error", "Rellena todos los campos.")
    else:
        messagebox.showerror("Error", "Selecciona un entrenador para actualizar.")


def limpiar_campos():
    entry_nombre.delete(0, END)
    entry_edad.delete(0, END)
    entry_nacionalidad.delete(0, END)
    entry_experiencia.delete(0, END)
    entry_equipo.delete(0, END)


def volver_menu():
    subprocess.Popen(["python", "menu.py"])  
    ventana.destroy() 


def seleccionar_entrenador(event):
    seleccionado = tabla.focus()
    if seleccionado:
        datos_entrenador = tabla.item(seleccionado)["values"]
        entry_nombre.delete(0, END)
        entry_nombre.insert(0, datos_entrenador[0])
        entry_edad.delete(0, END)
        entry_edad.insert(0, datos_entrenador[1])
        entry_nacionalidad.delete(0, END)
        entry_nacionalidad.insert(0, datos_entrenador[2])
        entry_experiencia.delete(0, END)
        entry_experiencia.insert(0, datos_entrenador[3])
        entry_equipo.delete(0, END)
        entry_equipo.insert(0, datos_entrenador[4])



ventana = Tk()
ventana.title("Gestión de Entrenadores")
ventana.geometry("800x600")


frame_principal = Frame(ventana, padx=10, pady=10)
frame_principal.pack(fill=BOTH, expand=True)


Button(ventana, text="Volver al Menú", command=volver_menu, bg="lightblue", padx=20).pack(side=TOP, pady=10)


frame_tabla = Frame(frame_principal)
frame_tabla.pack(fill=BOTH, expand=True)

tabla = ttk.Treeview(frame_tabla, columns=("Nombre", "Edad", "Nacionalidad", "Experiencia", "Equipo Actual"))
tabla.pack(fill=BOTH, expand=True, padx=5, pady=5)

tabla.heading("#0", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Edad", text="Edad")
tabla.heading("Nacionalidad", text="Nacionalidad")
tabla.heading("Experiencia", text="Experiencia")
tabla.heading("Equipo Actual", text="Equipo Actual")


frame_campos = Frame(frame_principal)
frame_campos.pack(side=BOTTOM, fill=X, pady=10)


Label(frame_campos, text="Nombre").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = Entry(frame_campos)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

Label(frame_campos, text="Edad").grid(row=0, column=2, padx=5, pady=5)
entry_edad = Entry(frame_campos)
entry_edad.grid(row=0, column=3, padx=5, pady=5)

Label(frame_campos, text="Nacionalidad").grid(row=0, column=4, padx=5, pady=5)
entry_nacionalidad = Entry(frame_campos)
entry_nacionalidad.grid(row=0, column=5, padx=5, pady=5)

Label(frame_campos, text="Experiencia").grid(row=0, column=6, padx=5, pady=5)
entry_experiencia = Entry(frame_campos)
entry_experiencia.grid(row=0, column=7, padx=5, pady=5)

Label(frame_campos, text="Equipo Actual").grid(row=0, column=8, padx=5, pady=5)
entry_equipo = Entry(frame_campos)
entry_equipo.grid(row=0, column=9, padx=5, pady=5)


frame_botones = Frame(frame_principal)
frame_botones.pack(side=BOTTOM, fill=X)

Button(frame_botones, text="Agregar Entrenador", command=agregar_entrenador).pack(side=LEFT, padx=10)
Button(frame_botones, text="Eliminar Entrenador", command=eliminar_entrenador).pack(side=LEFT, padx=10)
Button(frame_botones, text="Actualizar Entrenador", command=actualizar_entrenador).pack(side=LEFT, padx=10)


tabla.bind("<ButtonRelease-1>", seleccionar_entrenador)
actualizar_tabla()

ventana.mainloop()