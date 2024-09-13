import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox, Toplevel
from message_sender import send_messages
import pandas as pd
import sqlite3
from PIL import Image, ImageTk

# Variable para almacenar el mensaje configurado
configured_message = ""

# Configura la conexión a la base de datos SQLite
def connect_db():
    return sqlite3.connect('contactos.db')

# Crear la tabla si no existe
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()  # Crear la tabla si no existe

# Función para agregar un contacto a la base de datos
def add_contact(nombre, telefono):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contactos (nombre, telefono) VALUES (?, ?)", (nombre, telefono))
    conn.commit()
    conn.close()

# Función para eliminar un contacto de la base de datos
def delete_contact(contacto_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contactos WHERE id = ?", (contacto_id,))
    conn.commit()
    conn.close()

# Función para actualizar un contacto en la base de datos
def update_contact(contacto_id, nombre, telefono):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE contactos SET nombre = ?, telefono = ? WHERE id = ?", (nombre, telefono, contacto_id))
    conn.commit()
    conn.close()

# Función para cargar y mostrar los contactos de la base de datos
def load_and_display_entries(search_name=None):
    conn = connect_db()
    cursor = conn.cursor()
    
    if search_name:
        cursor.execute("SELECT * FROM contactos WHERE nombre LIKE ?", ('%' + search_name + '%',))
    else:
        cursor.execute("SELECT * FROM contactos")
    
    rows = cursor.fetchall()
    conn.close()
    
    entries_display.config(state=tk.NORMAL)
    entries_display.delete(1.0, tk.END)
    
    if not rows:
        entries_display.insert(tk.END, "No se encontraron contactos.")
    else:
        for row in rows:
            entries_display.insert(tk.END, f"ID: {row[0]}, Nombre: {row[1]}, Teléfono: {row[2]}\n")
    
    entries_display.config(state=tk.DISABLED)

def confirm_whatsapp_linked():
    messagebox.showinfo("Vinculación de WhatsApp", "Escanea el código QR en WhatsApp Web y haz clic en Aceptar para continuar.")

def open_message_window():
    top = Toplevel(root)
    top.title("Configurar Mensaje")
    top.configure(bg="#ffffff")

    tk.Label(top, text="Escribe el mensaje a enviar:", bg="#ffffff", fg=text_color).pack(padx=10, pady=10)

    message_text = tk.Text(top, height=10, width=50)
    message_text.pack(padx=10, pady=10)

    def save_message():
        global configured_message
        configured_message = message_text.get("1.0", "end-1c")
        messagebox.showinfo("Mensaje guardado", "Tu mensaje ha sido guardado.")
        top.destroy()

    tk.Button(top, text="Guardar Mensaje", bg=button_color, fg=text_color, command=save_message).pack(pady=10)

def add_contact_window():
    top = Toplevel(root)
    top.title("Agregar Contacto")
    top.configure(bg="#ffffff")

    tk.Label(top, text="Nombre:", bg="#ffffff", fg=text_color).pack(padx=10, pady=5)
    nombre_entry = tk.Entry(top)
    nombre_entry.pack(padx=10, pady=5)

    tk.Label(top, text="Teléfono:", bg="#ffffff", fg=text_color).pack(padx=10, pady=5)
    telefono_entry = tk.Entry(top)
    telefono_entry.pack(padx=10, pady=5)

    def save_contact():
        nombre = nombre_entry.get()
        telefono = telefono_entry.get()
        if nombre and telefono:
            add_contact(nombre, telefono)
            messagebox.showinfo("Contacto Agregado", "El contacto ha sido agregado.")
            load_and_display_entries()
            top.destroy()
        else:
            messagebox.showerror("Error", "Por favor, ingrese el nombre y el teléfono.")

    tk.Button(top, text="Agregar Contacto", bg=button_color, fg=text_color, command=save_contact).pack(pady=10)

def delete_contact_window():
    contacto_id = simpledialog.askinteger("Eliminar Contacto", "Ingrese el ID del contacto a eliminar:")
    if contacto_id:
        delete_contact(contacto_id)
        messagebox.showinfo("Contacto Eliminado", "El contacto ha sido eliminado.")
        load_and_display_entries()

def update_contact_window():
    contacto_id = simpledialog.askinteger("Actualizar Contacto", "Ingrese el ID del contacto a actualizar:")
    if contacto_id:
        top = Toplevel(root)
        top.title("Actualizar Contacto")
        top.configure(bg="#ffffff")

        tk.Label(top, text="Nuevo Nombre:", bg="#ffffff", fg=text_color).pack(padx=10, pady=5)
        nombre_entry = tk.Entry(top)
        nombre_entry.pack(padx=10, pady=5)

        tk.Label(top, text="Nuevo Teléfono:", bg="#ffffff", fg=text_color).pack(padx=10, pady=5)
        telefono_entry = tk.Entry(top)
        telefono_entry.pack(padx=10, pady=5)

        def save_update():
            nombre = nombre_entry.get()
            telefono = telefono_entry.get()
            if nombre and telefono:
                update_contact(contacto_id, nombre, telefono)
                messagebox.showinfo("Contacto Actualizado", "El contacto ha sido actualizado.")
                load_and_display_entries()
                top.destroy()
            else:
                messagebox.showerror("Error", "Por favor, ingrese el nombre y el teléfono.")

        tk.Button(top, text="Actualizar Contacto", bg=button_color, fg=text_color, command=save_update).pack(pady=10)

def send_message():
    if configured_message:
        result = send_messages(configured_message, confirm_whatsapp_linked)
        messagebox.showinfo("Resultado del Envío", result)
    else:
        messagebox.showerror("Error", "Por favor, configura un mensaje antes de enviar.")

# Función para buscar contactos por nombre
def search_contacts():
    search_name = search_entry.get()
    load_and_display_entries(search_name)

# Función para exportar la base de datos a un archivo de Excel
def export_to_excel():
    conn = connect_db()
    query = "SELECT * FROM contactos"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    try:
        df.to_excel('contactos_exportados.xlsx', index=False)
        messagebox.showinfo("Exportar a Excel", "Los contactos han sido exportados a 'contactos_exportados.xlsx'.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar a Excel: {e}")

# Función para importar contactos desde un archivo Excel
def import_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)

        if 'telefono' not in df.columns or 'nombre' not in df.columns:
            messagebox.showerror("Error", "El archivo Excel debe contener las columnas 'nombre' y 'telefono'.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        
        for index, row in df.iterrows():
            nombre = row['nombre']
            telefono = row['telefono']
            
            cursor.execute("SELECT id FROM contactos WHERE telefono = ?", (telefono,))
            if cursor.fetchone() is None:
                add_contact(nombre, telefono)
        
        conn.close()
        messagebox.showinfo("Importación Completa", "Los contactos han sido importados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo importar desde Excel: {e}")

# Función para mostrar el diálogo de importación de contactos
def import_contacts_window():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
    if file_path:
        import_from_excel(file_path)

# Configuración de la ventana principal
root = tk.Tk()
root.title("WspMsg")

# Colores
root.configure(bg="#128C7E")
button_color = "#c8e6c9"
text_color = "#333333"

# Cargar imágenes
folder_icon = Image.open("images/folder.png")
folder_icon = folder_icon.resize((30, 30), Image.Resampling.LANCZOS)
folder_icon = ImageTk.PhotoImage(folder_icon)

note_icon = Image.open("images/note.png")
note_icon = note_icon.resize((30, 30), Image.Resampling.LANCZOS)
note_icon = ImageTk.PhotoImage(note_icon)

whatsapp_icon = Image.open("images/wsp.png")
whatsapp_icon = whatsapp_icon.resize((30, 30), Image.Resampling.LANCZOS)
whatsapp_icon = ImageTk.PhotoImage(whatsapp_icon)

# Widgets
tk.Label(root, text="Buscar Contacto por Nombre:", bg="#128C7E", fg=text_color).pack(padx=10, pady=5)
search_entry = tk.Entry(root, width=50)
search_entry.pack(padx=10, pady=5)
tk.Button(root, text="Buscar", bg=button_color, fg=text_color, command=search_contacts).pack(padx=10, pady=5)

tk.Label(root, text="Contactos en la base de datos:", bg="#128C7E", fg=text_color).pack(padx=10, pady=5)
tk.Button(root, text="Agregar Contacto", bg=button_color, fg=text_color, command=add_contact_window).pack(padx=10, pady=5)
tk.Button(root, text="Eliminar Contacto", bg=button_color, fg=text_color, command=delete_contact_window).pack(padx=10, pady=5)
tk.Button(root, text="Actualizar Contacto", bg=button_color, fg=text_color, command=update_contact_window).pack(padx=10, pady=5)
tk.Button(root, text="Exportar a Excel", bg=button_color, fg=text_color, command=export_to_excel).pack(padx=10, pady=5)
tk.Button(root, text="Importar desde Excel", bg=button_color, fg=text_color, command=import_contacts_window).pack(padx=10, pady=5)

entries_display = tk.Text(root, height=10, width=60, bg="#ffffff", fg=text_color)
entries_display.pack(padx=10, pady=5)

tk.Label(root, text="Configurar el mensaje:", bg="#128C7E", fg=text_color).pack(padx=10, pady=5)
tk.Button(root, image=note_icon, command=open_message_window).pack(padx=10, pady=10)

tk.Label(root, text="Enviar Mensaje:", bg="#128C7E", fg=text_color).pack(padx=10, pady=5)
tk.Button(root, image=whatsapp_icon, command=send_message).pack(padx=10, pady=10)

# Cargar y mostrar los contactos al iniciar la aplicación
load_and_display_entries()

root.mainloop()
