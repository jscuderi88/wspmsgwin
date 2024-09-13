import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from file_manager import browse_file
from message_sender import send_messages
import pandas as pd
from PIL import Image, ImageTk

# Variable para almacenar el mensaje configurado
configured_message = ""
selected_file_path = ""  # Variable para almacenar la ruta del archivo seleccionado

def confirm_whatsapp_linked():
    messagebox.showinfo("Vinculación de WhatsApp", "Escanea el código QR en WhatsApp Web y haz clic en Aceptar para continuar.")

def open_message_window():
    # Ventana emergente para editar el mensaje
    top = Toplevel(root)
    top.title("Configurar Mensaje")
    top.configure(bg="#ffffff")
    
    tk.Label(top, text="Escribe el mensaje a enviar:", bg="#ffffff", fg=text_color).pack(padx=10, pady=10)
    
    message_text = tk.Text(top, height=10, width=50)
    message_text.pack(padx=10, pady=10)
    
    def save_message():
        # Guardar mensaje en la variable global y cerrar ventana emergente
        global configured_message
        configured_message = message_text.get("1.0", "end-1c")
        messagebox.showinfo("Mensaje guardado", "Tu mensaje ha sido guardado.")
        top.destroy()

    tk.Button(top, text="Guardar Mensaje", bg=button_color, fg=text_color, command=save_message).pack(pady=10)

# Función para seleccionar archivo y mostrar su ubicación
def browse_and_show_file():
    global selected_file_path
    file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file:
        selected_file_path = file
        file_path.set(file)  # Mostrar la ruta del archivo en la interfaz
        load_and_display_entries(file)  # Cargar y mostrar las entradas del archivo

# Función para cargar y mostrar las entradas del archivo Excel
def load_and_display_entries(file):
    try:
        # Leer archivo Excel usando pandas, sin incluir los encabezados
        df = pd.read_excel(file, header=None)
        
        # Limpiar la caja de texto antes de mostrar los datos
        entries_display.config(state=tk.NORMAL)  # Hacer que el widget sea editable para limpiar el contenido
        entries_display.delete(1.0, tk.END) 
        
        # Convertir DataFrame a cadena de texto con separación por tabulaciones
        data_str = df.to_string(index=False, header=False, col_space=10)
        entries_display.insert(tk.END, data_str)  # Mostrar solo los datos
        
        entries_display.config(state=tk.DISABLED)  # Hacer que el widget sea de solo lectura
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("WspMsg")

file_path = tk.StringVar()

# Colores
root.configure(bg="#128C7E")  # Verde agradable de fondo
button_color = "#c8e6c9"      # Verde suave para los botones
text_color = "#333333"        # Gris oscuro para el texto

# Cargar imágenes
folder_icon = Image.open("images/folder.png")  # Reemplaza con la ruta a tu imagen de carpeta
folder_icon = folder_icon.resize((30, 30), Image.Resampling.LANCZOS)  # Aumentar tamaño del ícono
folder_icon = ImageTk.PhotoImage(folder_icon)

note_icon = Image.open("images/note.png")  # Reemplaza con la ruta a tu imagen de hoja en blanco
note_icon = note_icon.resize((30, 30), Image.Resampling.LANCZOS)  # Aumentar tamaño del ícono
note_icon = ImageTk.PhotoImage(note_icon)

whatsapp_icon = Image.open("images/wsp.png")  # Reemplaza con la ruta a tu imagen de WhatsApp
whatsapp_icon = whatsapp_icon.resize((30, 30), Image.Resampling.LANCZOS)  # Aumentar tamaño del ícono
whatsapp_icon = ImageTk.PhotoImage(whatsapp_icon)

# Widgets
# Botón para seleccionar archivo
tk.Label(root, text="Selecciona la base de datos:", bg="#128C7E", fg=text_color).pack(padx=10, pady=5)
tk.Button(root, image=folder_icon, command=browse_and_show_file).pack(padx=10, pady=10)

# Mostrar la ruta del archivo seleccionado
tk.Label(root, text="Archivo seleccionado:", bg="#128C7E", fg=text_color).pack(padx=10, pady=5)
tk.Label(root, textvariable=file_path, bg="#ffffff", fg=text_color).pack(padx=10, pady=5)

# Caja de texto para mostrar las entradas del archivo Excel
tk.Label(root, text="Entradas cargadas:", bg="#128C7E", fg=text_color).pack(padx=10, pady=5)
entries_display = tk.Text(root, height=10, width=60, bg="#ffffff", fg=text_color)
entries_display.pack(padx=10, pady=5)

# Botón para configurar el mensaje
tk.Label(root, text="Configurar el mensaje:", bg="#128C7E", fg=text_color).pack(padx=10, pady=5)
tk.Button(root, image=note_icon, command=open_message_window).pack(padx=10, pady=10)

# Botón independiente para enviar el mensaje con ícono de WhatsApp
def send_message():
    if selected_file_path and configured_message:
        send_messages(selected_file_path, configured_message, confirm_whatsapp_linked)
        messagebox.showinfo("Mensaje Enviado", "El mensaje se ha enviado correctamente.")
    else:
        messagebox.showerror("Error", "Por favor, selecciona un archivo y configura un mensaje antes de enviar.")

tk.Label(root, text="Enviar Mensaje:", bg="#128C7E", fg=text_color).pack(padx=10, pady=5)
tk.Button(root, image=whatsapp_icon, command=send_message).pack(padx=10, pady=10)

root.mainloop()
