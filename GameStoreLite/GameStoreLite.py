"""
GameStoreLite Management System - Interfaz Gráfica Mejorada
Autor: [Tu Nombre]
Descripción: Aplicación GUI para gestionar géneros, clientes, juegos, ventas y detalles de ventas
             en una tienda de videojuegos. Usa MySQL y procedimientos almacenados.
             Interfaz rediseñada con estilo moderno y documentación completa.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector


# ==============================================================================
# CONFIGURACIÓN DE CONEXIÓN A LA BASE DE DATOS
# ==============================================================================
def get_connection():
    """
    Establece y devuelve una conexión a la base de datos MySQL.
    Cambia 'tu_password' por tu contraseña real de MySQL.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password= '',  # ⚠️ Cambia esto por tu contraseña real
        database="GameStoreLite"
    )


# ==============================================================================
# FUNCIONES CRUD GENÉRICAS (REUTILIZABLES)
# ==============================================================================

def limpiar_campos(entries):
    """
    Limpia todos los campos de entrada (Entry, DateEntry, etc.) de un formulario.
    :param entries: Diccionario con los widgets de entrada (clave=nombre, valor=widget)
    """
    for widget in entries.values():
        if isinstance(widget, tk.Entry) or isinstance(widget, ttk.Entry):
            widget.delete(0, tk.END)
        elif isinstance(widget, DateEntry):
            widget.set_date("")  # Reinicia el DateEntry


def ejecutar_sp(nombre_sp, params=()):
    """
    Ejecuta un procedimiento almacenado en la base de datos.
    :param nombre_sp: Nombre del procedimiento almacenado (ej: 'sp_InsertGenre')
    :param params: Tupla con los parámetros a pasar al SP
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc(nombre_sp, params)
        conn.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Error de Base de Datos", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def guardar(sp_name, entries, campos):
    """
    Guarda un nuevo registro llamando al SP correspondiente.
    Valida que ningún campo esté vacío.
    :param sp_name: Nombre del procedimiento almacenado para INSERT
    :param entries: Diccionario de widgets de entrada
    :param campos: Lista de nombres de campos a extraer (sin ID si es autoincremental)
    """
    datos = [entries[c].get() for c in campos]
    if any(v.strip() == "" for v in datos):  # Validación de campos vacíos
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return
    ejecutar_sp(sp_name, tuple(datos))
    messagebox.showinfo("Éxito", "Registro guardado correctamente")
    limpiar_campos(entries)


def actualizar(sp_name, entries, campos):
    """
    Actualiza un registro existente usando su ID.
    :param sp_name: Nombre del procedimiento almacenado para UPDATE
    :param entries: Diccionario de widgets de entrada
    :param campos: Lista de TODOS los campos, incluyendo el ID
    """
    datos = [entries[c].get() for c in campos]
    if any(v.strip() == "" for v in datos):
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return
    ejecutar_sp(sp_name, tuple(datos))
    messagebox.showinfo("Éxito", "Registro actualizado correctamente")
    limpiar_campos(entries)


def eliminar(sp_name, id_value):
    """
    Elimina un registro por su ID.
    :param sp_name: Nombre del procedimiento almacenado para DELETE
    :param id_value: Valor del ID a eliminar (como string)
    """
    if not id_value.strip():
        messagebox.showwarning("Advertencia", "Debe ingresar un ID válido")
        return
    if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?"):
        return
    ejecutar_sp(sp_name, (id_value,))
    messagebox.showinfo("Éxito", "Registro eliminado correctamente")


# ==============================================================================
# ESTILO GLOBAL DE LA INTERFAZ (MODERNO Y COHERENTE)
# ==============================================================================

def aplicar_estilo():
    """
    Aplica un estilo visual moderno a toda la aplicación usando ttk.Style.
    Define colores, fuentes y estilos para botones, etiquetas, entradas, etc.
    """
    style = ttk.Style()

    # Tema moderno (puedes probar también 'clam', 'alt', 'default')
    style.theme_use('clam')

    # Colores personalizados
    bg_color = "#f0f2f5"  # Fondo claro
    accent_color = "blue"  # Azul moderno (botones principales)
    delete_color = "red"  # Rojo para botones de eliminar
    text_color = "black"  # Texto oscuro
    frame_bg = "#ffffff"  # Fondo de frames

    # Configuración de la ventana principal
    root.configure(bg=bg_color)

    # Estilo para etiquetas
    style.configure("TLabel",
                    background=frame_bg,
                    foreground=text_color,
                    font=("Segoe UI", 11, "bold"))

    # Estilo para entradas
    style.configure("TEntry",
                    fieldbackground="white",
                    foreground=text_color,
                    font=("Segoe UI", 10))

    # Estilo para botones GUARDAR/ACTUALIZAR
    style.configure("Action.TButton",
                    background=accent_color,
                    foreground="white",
                    font=("Segoe UI", 10, "bold"),
                    padding=6)
    style.map("Action.TButton",
              background=[('active', '#357abd')])

    # Estilo para botones ELIMINAR
    style.configure("Delete.TButton",
                    background=delete_color,
                    foreground="white",
                    font=("Segoe UI", 10, "bold"),
                    padding=6)
    style.map("Delete.TButton",
              background=[('active', '#c0392b')])

    # Estilo para botones LIMPIAR
    style.configure("Clear.TButton",
                    background="#95a5a6",
                    foreground="white",
                    font=("Segoe UI", 10, "bold"),
                    padding=6)
    style.map("Clear.TButton",
              background=[('active', '#7f8c8d')])

    # Estilo para pestañas
    style.configure("TNotebook.Tab",
                    font=("Segoe UI", 11, "bold"),
                    padding=[12, 6])
    style.map("TNotebook.Tab",
              background=[("selected", accent_color)],
              foreground=[("selected", "white")])


# ==============================================================================
# CREACIÓN DE LA VENTANA PRINCIPAL Y PESTAÑAS
# ==============================================================================

root = tk.Tk()
root.title("🎮 GameStoreLite Management")
root.geometry("1000x800")
root.minsize(500, 500)

# Aplicar estilo global
aplicar_estilo()

# Fondo principal
root.configure(bg="#f0f2f4")

# Título superior
title_label = tk.Label(root,
                       text="GameStoreLite Management System",
                       font=("Segoe UI", 18, "bold"),
                       bg="#4a90e2",
                       fg="white",
                       pady=15)
title_label.pack(fill=tk.X)

# Notebook (pestañas)
notebook = ttk.Notebook(root, style="TNotebook")
notebook.pack(expand=True, fill="both", padx=20, pady=20)

tabs = {}
tab_names = ["Genres", "Customers", "Games", "Sales", "SaleDetails"]
for name in tab_names:
    tab = ttk.Frame(notebook, style="TFrame")
    tab.configure(style="TFrame")  # Asegurar estilo
    tabs[name] = tab
    notebook.add(tab, text=f"  {name}  ")  # Espaciado para mejor apariencia


# ==============================================================================
# FUNCIÓN AUXILIAR: CREAR FORMULARIO GENÉRICO
# ==============================================================================

def crear_formulario(tab, fields, entries_dict, date_fields=None):
    """
    Crea un formulario genérico con etiquetas y campos de entrada.
    :param tab: Frame donde se colocará el formulario
    :param fields: Lista de nombres de campos
    :param entries_dict: Diccionario donde se guardarán las referencias a los widgets
    :param date_fields: Lista de campos que deben ser DateEntry (opcional)
    :return: Frame contenedor del formulario
    """
    if date_fields is None:
        date_fields = []

    form_frame = tk.Frame(tab, bg="white", padx=30, pady=30, relief="groove", bd=2)
    form_frame.pack(pady=30, padx=40, fill="x")

    for i, field in enumerate(fields):
        # Etiqueta
        label = ttk.Label(form_frame, text=f"{field}:", style="TLabel")
        label.grid(row=i, column=0, padx=15, pady=12, sticky="e")

        # Campo de entrada
        if field in date_fields:
            entry = DateEntry(form_frame,
                              width=25,
                              background='#4a90e2',
                              foreground='white',
                              borderwidth=2,
                              date_pattern="yyyy-mm-dd",
                              font=("Segoe UI", 10))
        else:
            entry = ttk.Entry(form_frame, width=30, font=("Segoe UI", 10))

        entry.grid(row=i, column=1, padx=15, pady=12, sticky="w")
        entries_dict[field] = entry

        # Separador visual
        sep = ttk.Separator(form_frame, orient='horizontal')
        sep.grid(row=i + 1, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 10))

    return form_frame


# ==============================================================================
# FUNCIÓN AUXILIAR: CREAR BOTONES DE ACCIÓN
# ==============================================================================

def crear_botones_accion(tab, sp_insert, sp_update, sp_delete, entries_dict, id_field, campos_insert, campos_update):
    """
    Crea la barra de botones de acción (Guardar, Actualizar, Eliminar, Limpiar).
    :param tab: Frame donde se colocarán los botones
    :param sp_insert: Nombre del SP para insertar
    :param sp_update: Nombre del SP para actualizar
    :param sp_delete: Nombre del SP para eliminar
    :param entries_dict: Diccionario de widgets de entrada
    :param id_field: Nombre del campo ID (para eliminar)
    :param campos_insert: Campos necesarios para insertar (sin ID)
    :param campos_update: Campos necesarios para actualizar (con ID)
    """
    btn_frame = tk.Frame(tab, bg="white")
    btn_frame.pack(pady=20)

    # Botón Guardar
    btn_guardar = ttk.Button(btn_frame,
                             text="💾 Guardar",
                             style="Action.TButton",
                             command=lambda: guardar(sp_insert, entries_dict, campos_insert))
    btn_guardar.pack(side=tk.LEFT, padx=8)

    # Botón Actualizar
    btn_actualizar = ttk.Button(btn_frame,
                                text="🔄 Actualizar",
                                style="Action.TButton",
                                command=lambda: actualizar(sp_update, entries_dict, campos_update))
    btn_actualizar.pack(side=tk.LEFT, padx=8)

    # Botón Eliminar
    btn_eliminar = ttk.Button(btn_frame,
                              text="🗑️ Eliminar",
                              style="Delete.TButton",
                              command=lambda: eliminar(sp_delete, entries_dict[id_field].get()))
    btn_eliminar.pack(side=tk.LEFT, padx=8)

    # Botón Limpiar
    btn_limpiar = ttk.Button(btn_frame,
                             text="🧹 Limpiar",
                             style="Clear.TButton",
                             command=lambda: limpiar_campos(entries_dict))
    btn_limpiar.pack(side=tk.LEFT, padx=8)


# ==============================================================================
# CONFIGURACIÓN DE CADA PESTAÑA
# ==============================================================================

# -------- PESTAÑA: GENRES --------
genres_fields = ["GenreID", "GenreName", "Description"]
genres_entries = {}
crear_formulario(tabs["Genres"], genres_fields, genres_entries)
crear_botones_accion(tabs["Genres"],
                     "sp_InsertGenre", "sp_UpdateGenre", "sp_DeleteGenre",
                     genres_entries, "GenreID",
                     genres_fields[1:], genres_fields)

# -------- PESTAÑA: CUSTOMERS --------
customers_fields = ["CustomerID", "FullName", "Email", "City", "Country"]
customers_entries = {}
crear_formulario(tabs["Customers"], customers_fields, customers_entries)
crear_botones_accion(tabs["Customers"],
                     "sp_InsertCustomer", "sp_UpdateCustomer", "sp_DeleteCustomer",
                     customers_entries, "CustomerID",
                     customers_fields[1:], customers_fields)

# -------- PESTAÑA: GAMES --------
games_fields = ["GameID", "GameTitle", "GenreID", "Platform", "Price"]
games_entries = {}
crear_formulario(tabs["Games"], games_fields, games_entries)
crear_botones_accion(tabs["Games"],
                     "sp_InsertGame", "sp_UpdateGame", "sp_DeleteGame",
                     games_entries, "GameID",
                     games_fields[1:], games_fields)

# -------- PESTAÑA: SALES --------
sales_fields = ["SaleID", "CustomerID", "SaleDate"]
sales_entries = {}
crear_formulario(tabs["Sales"], sales_fields, sales_entries, date_fields=["SaleDate"])
crear_botones_accion(tabs["Sales"],
                     "sp_InsertSale", "sp_UpdateSale", "sp_DeleteSale",
                     sales_entries, "SaleID",
                     ["CustomerID", "SaleDate"], sales_fields)

# -------- PESTAÑA: SALEDETAILS --------
sd_fields = ["SaleDetailID", "SaleID", "GameID", "Quantity"]
sd_entries = {}
crear_formulario(tabs["SaleDetails"], sd_fields, sd_entries)
crear_botones_accion(tabs["SaleDetails"],
                     "sp_InsertSaleDetail", "sp_UpdateSaleDetail", "sp_DeleteSaleDetail",
                     sd_entries, "SaleDetailID",
                     sd_fields[1:], sd_fields)

# ==============================================================================
# PIE DE PÁGINA
# ==============================================================================

footer = tk.Label(root,
                  text="© 2025 GameStoreLite - Sistema de Gestión de Tienda de Videojuegos - HECHO POR LUIS ROJO",
                  bg="#f0f2f5",
                  fg="#7f8c8d",
                  font=("Segoe UI", 9))
footer.pack(side=tk.BOTTOM, pady=10)

# ==============================================================================
# INICIAR APLICACIÓN
# ==============================================================================

if __name__ == "__main__":
    root.mainloop()