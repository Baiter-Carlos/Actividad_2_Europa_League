from tkinter import *
import subprocess


def abrir_gestion_deportistas():
    subprocess.Popen(["python", "deportistas.py"]) 
    ventana_menu.withdraw()  


def abrir_gestion_entrenadores():
    subprocess.Popen(["python", "entrenadores.py"])  
    ventana_menu.withdraw()  


def abrir_gestion_equipos():
    subprocess.Popen(["python", "equipos.py"])  
    ventana_menu.withdraw()  


def abrir_gestion_tabla_posiciones():
    subprocess.Popen(["python", "tabla_posiciones.py"])  
    ventana_menu.withdraw()  


def abrir_gestion_encuentros():
    subprocess.Popen(["python", "encuentros.py"])  
    ventana_menu.withdraw()  


def centrar_ventana(ventana, ancho, alto):
    
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()


    posicion_x = int((pantalla_ancho - ancho) / 2)
    posicion_y = int((pantalla_alto - alto) / 2)

   
    ventana.geometry(f"{ancho}x{alto}+{posicion_x}+{posicion_y}")


ventana_menu = Tk()
ventana_menu.title("Menú Principal - Gestión de MongoDB")


ancho_ventana = 800
alto_ventana = 600
centrar_ventana(ventana_menu, ancho_ventana, alto_ventana)  


label_tabla = Label(ventana_menu, text="Selecciona una acción:", font=("Helvetica", 18))
label_tabla.grid(row=0, column=0, padx=20, pady=20, columnspan=3)


btn_deportistas = Button(ventana_menu, text="Gestión de Deportistas", command=abrir_gestion_deportistas, font=("Helvetica", 16), width=30, height=2)
btn_deportistas.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

btn_entrenadores = Button(ventana_menu, text="Gestión de Entrenadores", command=abrir_gestion_entrenadores, font=("Helvetica", 16), width=30, height=2)
btn_entrenadores.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

btn_equipos = Button(ventana_menu, text="Gestión de Equipos", command=abrir_gestion_equipos, font=("Helvetica", 16), width=30, height=2)
btn_equipos.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

btn_tabla_posiciones = Button(ventana_menu, text="Gestión de Tabla de Posiciones", command=abrir_gestion_tabla_posiciones, font=("Helvetica", 16), width=30, height=2)
btn_tabla_posiciones.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

btn_encuentros = Button(ventana_menu, text="Gestión de Encuentros", command=abrir_gestion_encuentros, font=("Helvetica", 16), width=30, height=2)
btn_encuentros.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")

# Botón de salir
btn_salir = Button(ventana_menu, text="Salir", command=ventana_menu.destroy, font=("Helvetica", 16), width=30, height=2)
btn_salir.grid(row=6, column=0, padx=20, pady=20, sticky="nsew")


ventana_menu.grid_rowconfigure(0, weight=1)  
ventana_menu.grid_rowconfigure(1, weight=1)  
ventana_menu.grid_rowconfigure(2, weight=1)  
ventana_menu.grid_rowconfigure(3, weight=1)  
ventana_menu.grid_rowconfigure(4, weight=1)  
ventana_menu.grid_rowconfigure(5, weight=1)  
ventana_menu.grid_rowconfigure(6, weight=1)  

ventana_menu.grid_columnconfigure(0, weight=1)  

ventana_menu.mainloop()