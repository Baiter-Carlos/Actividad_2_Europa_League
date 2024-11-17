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
MONGO_COLECCION = "tabla_posiciones"


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
            documento.get("posicion", ""),
            documento.get("puntos", ""),
            documento.get("encuentros_disputados", "")
        ))


def agregar_posicion():
    if entry_nombre.get() and entry_posicion.get() and entry_puntos.get() and entry_encuentros.get():
        coleccion.insert_one({
            "nombre": entry_nombre.get(),
            "posicion": int(entry_posicion.get()),
            "puntos": int(entry_puntos.get()),
            "encuentros_disputados": int(entry_encuentros.get())
        })
        actualizar_tabla()
        limpiar_campos()
    else:
        messagebox.showerror("Error", "Rellena todos los campos.")


def eliminar_posicion():
    seleccionado = tabla.focus()
    if seleccionado:
        id_posicion = tabla.item(seleccionado)["text"]
        coleccion.delete_one({"_id": ObjectId(id_posicion)})
        actualizar_tabla()
    else:
        messagebox.showerror("Error", "Selecciona una posición para eliminar.")


def actualizar_posicion():
    seleccionado = tabla.focus()
    if seleccionado:
        id_posicion = tabla.item(seleccionado)["text"]
        nuevo_nombre = entry_nombre.get()
        nueva_posicion = entry_posicion.get()
        nuevos_puntos = entry_puntos.get()
        nuevos_encuentros = entry_encuentros.get()

        if nuevo_nombre and nueva_posicion and nuevos_puntos and nuevos_encuentros:
            coleccion.update_one(
                {"_id": ObjectId(id_posicion)},
                {"$set": {
                    "nombre": nuevo_nombre,
                    "posicion": int(nueva_posicion),
                    "puntos": int(nuevos_puntos),
                    "encuentros_disputados": int(nuevos_encuentros)
                }}
            )
            actualizar_tabla()
            limpiar_campos()
        else:
            messagebox.showerror("Error", "Rellena todos los campos.")
    else:
        messagebox.showerror("Error", "Selecciona una posición para actualizar.")


def limpiar_campos():
    entry_nombre.delete(0, END)
    entry_posicion.delete(0, END)
    entry_puntos.delete(0, END)
    entry_encuentros.delete(0, END)


def volver_menu():
    subprocess.Popen(["python", "menu.py"])  
    ventana.destroy()  


def seleccionar_posicion(event):
    seleccionado = tabla.focus()
    if seleccionado:
        datos_posicion = tabla.item(seleccionado)["values"]
        entry_nombre.delete(0, END)
        entry_nombre.insert(0, datos_posicion[0])
        entry_posicion.delete(0, END)
        entry_posicion.insert(0, datos_posicion[1])
        entry_puntos.delete(0, END)
        entry_puntos.insert(0, datos_posicion[2])
        entry_encuentros.delete(0, END)
        entry_encuentros.insert(0, datos_posicion[3])



ventana = Tk()
ventana.title("Tabla de Posiciones")
ventana.geometry("800x600")


frame_principal = Frame(ventana, padx=10, pady=10)
frame_principal.pack(fill=BOTH, expand=True)


Button(ventana, text="Volver al Menú", command=volver_menu, bg="lightblue", padx=20).pack(side=TOP, pady=10)


frame_tabla = Frame(frame_principal)
frame_tabla.pack(fill=BOTH, expand=True)

tabla = ttk.Treeview(frame_tabla, columns=("Nombre", "Posición", "Puntos", "Encuentros"))
tabla.pack(fill=BOTH, expand=True, padx=5, pady=5)

tabla.heading("#0", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Posición", text="Posición")
tabla.heading("Puntos", text="Puntos")
tabla.heading("Encuentros", text="Encuentros Disputados")


frame_campos = Frame(frame_principal)
frame_campos.pack(side=BOTTOM, fill=X, pady=10)


Label(frame_campos, text="Nombre").grid(row=0, column=0, padx=5, pady=5)
entry_nombre = Entry(frame_campos)
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

Label(frame_campos, text="Posición").grid(row=0, column=2, padx=5, pady=5)
entry_posicion = Entry(frame_campos)
entry_posicion.grid(row=0, column=3, padx=5, pady=5)

Label(frame_campos, text="Puntos").grid(row=1, column=0, padx=5, pady=5)
entry_puntos = Entry(frame_campos)
entry_puntos.grid(row=1, column=1, padx=5, pady=5)

Label(frame_campos, text="Encuentros Disputados").grid(row=1, column=2, padx=5, pady=5)
entry_encuentros = Entry(frame_campos)
entry_encuentros.grid(row=1, column=3, padx=5, pady=5)


frame_botones = Frame(frame_principal)
frame_botones.pack(side=BOTTOM, fill=X)

Button(frame_botones, text="Agregar Posición", command=agregar_posicion).pack(side=LEFT, padx=10)
Button(frame_botones, text="Eliminar Posición", command=eliminar_posicion).pack(side=LEFT, padx=10)
Button(frame_botones, text="Actualizar Posición", command=actualizar_posicion).pack(side=LEFT, padx=10)


actualizar_tabla()


tabla.bind("<ButtonRelease-1>", seleccionar_posicion)


ventana.mainloop()