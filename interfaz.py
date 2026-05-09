import tkinter as tk
from tkinter import messagebox, scrolledtext

from cliente import Cliente
from servicio import ReservaSala
from reserva import Reserva
from excepciones import ClienteError, ReservaError

# Lista global de clientes y reservas registrados en la aplicación
clientes = []
reservas = []

# Servicio principal fijo que se ofrece en la aplicación
servicio_principal = ReservaSala(
    "Sala VIP",
    50000,
    1
)


def registrar_cliente():
    """Registra un cliente utilizando los datos ingresados en la interfaz."""
    nombre = entrada_nombre.get().strip()
    correo = entrada_correo.get().strip()

    # Validación básica: no deben quedar campos vacíos
    if nombre == "" or correo == "":
        messagebox.showwarning(
            "Advertencia",
            "Todos los campos son obligatorios"
        )
        return

    # Validar el cliente y capturar errores de validación
    try:
        cliente = Cliente(nombre, correo)
    except ClienteError as e:
        messagebox.showerror(
            "Error de validación",
            str(e)
        )
        return

    clientes.append(cliente)

    messagebox.showinfo(
        "✓ Éxito",
        f"Cliente {nombre} registrado correctamente"
    )

    # Limpiar campos y actualizar el panel de clientes
    entrada_nombre.delete(0, tk.END)
    entrada_correo.delete(0, tk.END)
    actualizar_info_clientes()


def hacer_reserva():
    """Crea y confirma una reserva para el último cliente registrado."""
    if len(clientes) == 0:
        messagebox.showerror(
            "Error",
            "No hay clientes registrados\n\nPrimero debes registrar un cliente"
        )
        return

    cliente = clientes[-1]
    reserva = Reserva(cliente, servicio_principal)

    try:
        reserva.confirmar()
        reservas.append(reserva)

        mensaje_reserva = (
            f"✓ Reserva Confirmada\n\n"
            f"Cliente: {cliente.get_nombre()}\n"
            f"Servicio: {servicio_principal.nombre}\n"
            f"Estado: {reserva.estado}\n"
            f"Costo: ${servicio_principal.calcular_costo():,.0f}"
        )

        messagebox.showinfo(
            "Reserva Exitosa",
            mensaje_reserva
        )
        actualizar_info_reservas()

    except ReservaError as e:
        messagebox.showerror(
            "Error en la Reserva",
            str(e)
        )


def actualizar_info_clientes():
    """Actualiza el panel de texto que muestra los clientes registrados."""
    info_clientes.config(state=tk.NORMAL)
    info_clientes.delete(1.0, tk.END)

    if clientes:
        info_clientes.insert(tk.END, "📋 CLIENTES REGISTRADOS\n")
        info_clientes.insert(tk.END, "=" * 35 + "\n\n")
        for i, cliente in enumerate(clientes, 1):
            info_clientes.insert(tk.END, f"{i}. {cliente.mostrar_info()}\n")
    else:
        info_clientes.insert(tk.END, "No hay clientes registrados")

    info_clientes.config(state=tk.DISABLED)


def actualizar_info_reservas():
    """Actualiza el panel de texto que muestra las reservas confirmadas."""
    info_reservas.config(state=tk.NORMAL)
    info_reservas.delete(1.0, tk.END)

    if reservas:
        info_reservas.insert(tk.END, "🎫 RESERVAS CONFIRMADAS\n")
        info_reservas.insert(tk.END, "=" * 35 + "\n\n")
        for i, reserva in enumerate(reservas, 1):
            info_reservas.insert(tk.END, f"{i}. {reserva.mostrar_reserva()}\n")
    else:
        info_reservas.insert(tk.END, "No hay reservas confirmadas")

    info_reservas.config(state=tk.DISABLED)


# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Reservas VIP")
ventana.geometry("700x700")
ventana.configure(bg="#f0f0f0")

# Colores personalizados para mantener consistencia visual
COLOR_HEADER = "#1e3c72"
COLOR_SECUNDARIO = "#2a5298"
COLOR_ACENTO = "#00d4ff"
COLOR_TEXTO = "#ffffff"
COLOR_BOTON = "#00a8e8"
COLOR_BOTON_HOVER = "#0088b8"

# Frame superior con título principal
frame_header = tk.Frame(ventana, bg=COLOR_HEADER)
frame_header.pack(fill=tk.X, padx=0, pady=0)

titulo = tk.Label(
    frame_header,
    text="🏢 SISTEMA DE RESERVAS VIP",
    font=("Arial", 20, "bold"),
    bg=COLOR_HEADER,
    fg=COLOR_TEXTO
)
titulo.pack(pady=20)

# Frame contenedor principal para secciones
frame_main = tk.Frame(ventana, bg="#f0f0f0")
frame_main.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

# Sección de registro de clientes
frame_registro = tk.LabelFrame(
    frame_main,
    text="📝 Registrar Cliente",
    font=("Arial", 12, "bold"),
    bg="#ffffff",
    fg=COLOR_HEADER,
    padx=15,
    pady=15
)
frame_registro.pack(fill=tk.X, pady=10)

# Campo de entrada para el nombre del cliente
label_nombre = tk.Label(
    frame_registro,
    text="Nombre completo:",
    font=("Arial", 10, "bold"),
    bg="#ffffff",
    fg=COLOR_HEADER
)
label_nombre.pack(anchor=tk.W)

entrada_nombre = tk.Entry(
    frame_registro,
    font=("Arial", 10),
    width=40,
    relief=tk.FLAT,
    bd=2
)
entrada_nombre.pack(fill=tk.X, pady=(5, 10))
entrada_nombre.config(highlightbackground=COLOR_ACENTO, highlightthickness=1)

# Campo de entrada para el correo electrónico del cliente
label_correo = tk.Label(
    frame_registro,
    text="Correo electrónico:",
    font=("Arial", 10, "bold"),
    bg="#ffffff",
    fg=COLOR_HEADER
)
label_correo.pack(anchor=tk.W)

entrada_correo = tk.Entry(
    frame_registro,
    font=("Arial", 10),
    width=40,
    relief=tk.FLAT,
    bd=2
)
entrada_correo.pack(fill=tk.X, pady=(5, 15))
entrada_correo.config(highlightbackground=COLOR_ACENTO, highlightthickness=1)

# Botón de acción para registrar cliente
boton_cliente = tk.Button(
    frame_registro,
    text="✓ REGISTRAR CLIENTE",
    command=registrar_cliente,
    font=("Arial", 11, "bold"),
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    relief=tk.FLAT,
    padx=20,
    pady=10,
    cursor="hand2",
    activebackground=COLOR_BOTON_HOVER,
    activeforeground=COLOR_TEXTO
)
boton_cliente.pack(fill=tk.X)

# Panel que muestra los clientes registrados hasta el momento
frame_info_clientes = tk.LabelFrame(
    frame_main,
    text="👥 Clientes Registrados",
    font=("Arial", 11, "bold"),
    bg="#ffffff",
    fg=COLOR_HEADER,
    padx=10,
    pady=10
)
frame_info_clientes.pack(fill=tk.BOTH, expand=True, pady=10)

info_clientes = scrolledtext.ScrolledText(
    frame_info_clientes,
    font=("Arial", 9),
    height=4,
    width=50,
    bg="#f9f9f9",
    fg=COLOR_HEADER,
    relief=tk.FLAT,
    bd=1
)
info_clientes.pack(fill=tk.BOTH, expand=True)
info_clientes.config(state=tk.DISABLED)

# Botón principal para confirmar la reserva del último cliente registrado
boton_reserva = tk.Button(
    frame_main,
    text="🎫 REALIZAR RESERVA",
    command=hacer_reserva,
    font=("Arial", 12, "bold"),
    bg=COLOR_SECUNDARIO,
    fg=COLOR_TEXTO,
    relief=tk.FLAT,
    padx=20,
    pady=12,
    cursor="hand2",
    activebackground="#1a2c52",
    activeforeground=COLOR_TEXTO
)
boton_reserva.pack(fill=tk.X, pady=10)

# Panel que muestra las reservas confirmadas hasta ahora
frame_info_reservas = tk.LabelFrame(
    frame_main,
    text="🎫 Reservas Confirmadas",
    font=("Arial", 11, "bold"),
    bg="#ffffff",
    fg=COLOR_HEADER,
    padx=10,
    pady=10
)
frame_info_reservas.pack(fill=tk.BOTH, expand=True, pady=10)

info_reservas = scrolledtext.ScrolledText(
    frame_info_reservas,
    font=("Arial", 9),
    height=4,
    width=50,
    bg="#f9f9f9",
    fg=COLOR_HEADER,
    relief=tk.FLAT,
    bd=1
)
info_reservas.pack(fill=tk.BOTH, expand=True)
info_reservas.config(state=tk.DISABLED)

# Panel inferior con detalles del servicio disponible
frame_servicio = tk.Frame(frame_main, bg="#e8f4f8", relief=tk.FLAT, bd=1, padx=10, pady=10)
frame_servicio.pack(fill=tk.X, pady=10)

info_servicio = tk.Label(
    frame_servicio,
    text=f"🏢 Servicio: {servicio_principal.nombre} | 💰 Precio: ${servicio_principal.precio_base:,.0f} por hora | ⏱️ Duración: {servicio_principal.horas} hora",
    font=("Arial", 9),
    bg="#e8f4f8",
    fg=COLOR_SECUNDARIO
)
info_servicio.pack()

# Inicia el bucle principal de la interfaz gráfica
ventana.mainloop()