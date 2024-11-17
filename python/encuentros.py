from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson import ObjectId
import subprocess
from datetime import datetime


MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PUERTO}/"
MONGO_BASEDATOS = "Europa_League"
MONGO_COLECCION = "encuentros"


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
        equipo_local = documento.get("equipo_local", {}).get("nombre", "Desconocido")
        equipo_visitante = documento.get("equipo_visitante", {}).get("nombre", "Desconocido")
        tabla.insert("", "end", text=str(documento["_id"]), values=(
            equipo_local,
            equipo_visitante,
            documento.get("goles_local", ""),
            documento.get("goles_visitante", ""),
            documento.get("fecha", ""),
            documento.get("arbitro", "")
        ))


def agregar_encuentro():
    if entry_equipo_local.get() and entry_equipo_visitante.get() and entry_goles_local.get() and entry_goles_visitante.get() and entry_fecha.get() and entry_arbitro.get():
        coleccion.insert_one({
            "equipo_local": {"nombre": entry_equipo_local.get()},
            "equipo_visitante": {"nombre": entry_equipo_visitante.get()},
            "goles_local": int(entry_goles_local.get()),
            "goles_visitante": int(entry_goles_visitante.get()),
            "fecha": datetime.strptime(entry_fecha.get(), "%Y-%m-%d %H:%M:%S"),
            "arbitro": ObjectId(entry_arbitro.get())
        })
        actualizar_tabla()
        limpiar_campos()
    else:
        messagebox.showerror("Error", "Rellena todos los campos.")


def eliminar_encuentro():
    seleccionado = tabla.focus()
    if seleccionado:
        id_encuentro = tabla.item(seleccionado)["text"]
        coleccion.delete_one({"_id": ObjectId(id_encuentro)})
        actualizar_tabla()
    else:
        messagebox.showerror("Error", "Selecciona un encuentro para eliminar.")


def actualizar_encuentro():
    seleccionado = tabla.focus()
    if seleccionado:
        id_encuentro = tabla.item(seleccionado)["text"]
        nuevo_equipo_local = entry_equipo_local.get()
        nuevo_equipo_visitante = entry_equipo_visitante.get()
        nuevos_goles_local = entry_goles_local.get()
        nuevos_goles_visitante = entry_goles_visitante.get()
        nueva_fecha = entry_fecha.get()
        nuevo_arbitro = entry_arbitro.get()

        if nuevo_equipo_local and nuevo_equipo_visitante and nuevos_goles_local and nuevos_goles_visitante and nueva_fecha and nuevo_arbitro:
            coleccion.update_one(
                {"_id": ObjectId(id_encuentro)},
                {"$set": {
                    "equipo_local": {"nombre": nuevo_equipo_local},
                    "equipo_visitante": {"nombre": nuevo_equipo_visitante},
                    "goles_local": int(nuevos_goles_local),
                    "goles_visitante": int(nuevos_goles_visitante),
                    "fecha": datetime.strptime(nueva_fecha, "%Y-%m-%d %H:%M:%S"),
                    "arbitro": ObjectId(nuevo_arbitro)
                }}
            )
            actualizar_tabla()
            limpiar_campos()
        else:
            messagebox.showerror("Error", "Rellena todos los campos.")
    else:
        messagebox.showerror("Error", "Selecciona un encuentro para actualizar.")


def limpiar_campos():
    entry_equipo_local.delete(0, END)
    entry_equipo_visitante.delete(0, END)
    entry_goles_local.delete(0, END)
    entry_goles_visitante.delete(0, END)
    entry_fecha.delete(0, END)
    entry_arbitro.delete(0, END)


def volver_menu():
    subprocess.Popen(["python", "menu.py"])  
    ventana.destroy()  


def seleccionar_encuentro(event):
    seleccionado = tabla.focus()
    if seleccionado:
        datos_encuentro = tabla.item(seleccionado)["values"]
        entry_equipo_local.delete(0, END)
        entry_equipo_local.insert(0, datos_encuentro[0])
        entry_equipo_visitante.delete(0, END)
        entry_equipo_visitante.insert(0, datos_encuentro[1])
        entry_goles_local.delete(0, END)
        entry_goles_local.insert(0, datos_encuentro[2])
        entry_goles_visitante.delete(0, END)
        entry_goles_visitante.insert(0, datos_encuentro[3])
        entry_fecha.delete(0, END)
        entry_fecha.insert(0, datos_encuentro[4])
        entry_arbitro.delete(0, END)
        entry_arbitro.insert(0, datos_encuentro[5])



ventana = Tk()
ventana.title("Encuentros")
ventana.geometry("800x600")


frame_principal = Frame(ventana, padx=10, pady=10)
frame_principal.pack(fill=BOTH, expand=True)


Button(ventana, text="Volver al Menú", command=volver_menu, bg="lightblue", padx=20).pack(side=TOP, pady=10)


frame_tabla = Frame(frame_principal)
frame_tabla.pack(fill=BOTH, expand=True)

tabla = ttk.Treeview(frame_tabla, columns=("Equipo Local", "Equipo Visitante", "Goles Local", "Goles Visitante", "Fecha", "Árbitro"))
tabla.pack(fill=BOTH, expand=True, padx=5, pady=5)

tabla.heading("#0", text="ID")
tabla.heading("Equipo Local", text="Equipo Local")
tabla.heading("Equipo Visitante", text="Equipo Visitante")
tabla.heading("Goles Local", text="Goles Local")
tabla.heading("Goles Visitante", text="Goles Visitante")
tabla.heading("Fecha", text="Fecha")
tabla.heading("Árbitro", text="Árbitro")


frame_campos = Frame(frame_principal)
frame_campos.pack(side=BOTTOM, fill=X, pady=10)


Label(frame_campos, text="Equipo Local").grid(row=0, column=0, padx=5, pady=5)
entry_equipo_local = Entry(frame_campos)
entry_equipo_local.grid(row=0, column=1, padx=5, pady=5)

Label(frame_campos, text="Equipo Visitante").grid(row=0, column=2, padx=5, pady=5)
entry_equipo_visitante = Entry(frame_campos)
entry_equipo_visitante.grid(row=0, column=3, padx=5, pady=5)

Label(frame_campos, text="Goles Local").grid(row=1, column=0, padx=5, pady=5)
entry_goles_local = Entry(frame_campos)
entry_goles_local.grid(row=1, column=1, padx=5, pady=5)

Label(frame_campos, text="Goles Visitante").grid(row=1, column=2, padx=5, pady=5)
entry_goles_visitante = Entry(frame_campos)
entry_goles_visitante.grid(row=1, column=3, padx=5, pady=5)

Label(frame_campos, text="Fecha (YYYY-MM-DD HH:MM:SS)").grid(row=2, column=0, padx=5, pady=5)
entry_fecha = Entry(frame_campos)
entry_fecha.grid(row=2, column=1, padx=5, pady=5)

Label(frame_campos, text="Árbitro (ID)").grid(row=2, column=2, padx=5, pady=5)
entry_arbitro = Entry(frame_campos)
entry_arbitro.grid(row=2, column=3, padx=5, pady=5)


frame_botones = Frame(frame_principal)
frame_botones.pack(side=BOTTOM, fill=X)

Button(frame_botones, text="Agregar Encuentro", command=agregar_encuentro).pack(side=LEFT, padx=10)
Button(frame_botones, text="Eliminar Encuentro", command=eliminar_encuentro).pack(side=LEFT, padx=10)
Button(frame_botones, text="Actualizar Encuentro", command=actualizar_encuentro).pack(side=LEFT, padx=10)

tabla.bind("<ButtonRelease-1>", seleccionar_encuentro)


actualizar_tabla()


ventana.mainloop()