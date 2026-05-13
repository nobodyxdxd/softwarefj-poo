import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import re

from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import ClienteError, ReservaError, ServicioError
from logger_config import logger

# Listas globales
clientes = []
reservas = []
comentarios = []
# Servicio activo
servicio_actual = ReservaSala("Sala VIP", 50000, 1)

# Colores
COLOR_FONDO = "#151a2e"
COLOR_HEADER = "#1b2440"
COLOR_SECUNDARIO = "#2b3a67"
COLOR_ACENTO = "#8be9fd"
COLOR_BOTON = "#4b6cb7"
COLOR_BOTON_HOVER = "#5c7cfa"
COLOR_EXITO = "#7bd88f"
COLOR_ERROR = "#ff6b81"
COLOR_TEXTO = "#f4f7ff"
COLOR_CARD = "#222b45"
COLOR_INPUT = "#364269"
COLOR_BORDER = "#3d4c72"

# Hover botones
def on_enter(e):
    e.widget['background'] = COLOR_BOTON_HOVER

def on_leave(e):
    e.widget['background'] = COLOR_BOTON

#Apartado para registrar clientes, con validaciones de campos.
def registrar_cliente():
    """Registra un cliente con cédula, nombre y correo."""
    cedula = entrada_cedula.get().strip()
    nombre = entrada_nombre.get().strip()
    correo = entrada_correo.get().strip()

    if not cedula or not nombre or not correo:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return

    if not cedula.isdigit():
        messagebox.showerror("Error", "La cédula solo debe contener números")
        return

    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚ ]+$", nombre):
        messagebox.showerror("Error", "El nombre solo debe contener letras y espacios")
        return

    for cliente in clientes:
        if cliente.get_cedula() == cedula:
            messagebox.showerror("Error", f"La cédula {cedula} ya está registrada")
            return

    try:
        cliente = Cliente(nombre, correo, cedula)
        clientes.append(cliente)
        logger.info(f"Cliente registrado: {cliente.mostrar_info()}")
        messagebox.showinfo("Éxito", f"Cliente {nombre} registrado correctamente")

        entrada_cedula.delete(0, tk.END)
        entrada_nombre.delete(0, tk.END)
        entrada_correo.delete(0, tk.END)
        actualizar_tabla_clientes()
    except ClienteError as e:
        logger.error(e)
        messagebox.showerror("Error de validación", str(e))



#Apartado para actualizar la tabla de clientes cada vez que se registre un nuevo cliente o se realice una búsqueda.
def actualizar_tabla_clientes():
    """Actualiza la tabla de clientes con estilo similar a Excel."""
    for item in tabla_clientes.get_children():
        tabla_clientes.delete(item)

    for cliente in clientes:
        tabla_clientes.insert("", "end", values=(
            cliente.get_id(),
            cliente.get_cedula(),
            cliente.get_nombre(),
            cliente.get_correo()
        ))

    actualizar_dropdown_clientes()


#Apartado para actualizar el menú desplegable de clientes.
def actualizar_dropdown_clientes():

    valores = [
        f"{c.get_nombre()}"
        for c in clientes
    ]

    combo_clientes['values'] = valores

    combo_clientes_comentario['values'] = valores

    if valores:

        combo_clientes.current(0)

        combo_clientes_comentario.current(0)



#Apartado para buscar un cliente por cédula, mostrando su información y reservas asociadas.
def buscar_cliente_por_cedula(): 
    """Busca un cliente por cédula."""
    cedula_busqueda = entrada_busqueda_cedula.get().strip()

    if not cedula_busqueda:
        messagebox.showwarning("Advertencia", "Ingresa una cédula para buscar")
        return

    cliente_encontrado = None
    for cliente in clientes:
        if cliente.get_cedula() == cedula_busqueda:
            cliente_encontrado = cliente
            break

    if not cliente_encontrado:
        messagebox.showinfo("Búsqueda", f"No se encontró cliente con cédula {cedula_busqueda}")
        return

    reservas_cliente = [r for r in reservas if r.cliente.get_cedula() == cedula_busqueda]

    info_resultado = f"Cliente encontrado:\n{cliente_encontrado.mostrar_info()}\n\n"
    info_resultado += f"Reservas ({len(reservas_cliente)}):\n"

    if reservas_cliente:
        for i, reserva in enumerate(reservas_cliente, 1):
            info_resultado += f"{i}. {reserva.mostrar_reserva()}\n"
    else:
        info_resultado += "Sin reservas registradas"

    messagebox.showinfo("Resultado de búsqueda", info_resultado)



#Apartado para realizar una reserva, con validaciones de selección de cliente y servicio activo.
def hacer_reserva(): 
    """Crea y confirma una reserva."""
    seleccion = combo_clientes.get()

    if not seleccion:
        messagebox.showerror("Error", "Debes seleccionar un cliente")
        return

    if len(clientes) == 0:
        messagebox.showerror("Error", "No hay clientes registrados")
        return

    cliente_seleccionado = None
    for cliente in clientes:
        if f"{cliente.get_cedula()} - {cliente.get_nombre()}" == seleccion:
            cliente_seleccionado = cliente
            break

    if not cliente_seleccionado:
        messagebox.showerror("Error", "Cliente no encontrado")
        return

    try:
        reserva = Reserva(cliente_seleccionado, servicio_actual)
        reserva.confirmar()
        reservas.append(reserva)

        costo = reserva.obtener_costo_total()
        mensaje = f"✓ Reserva Confirmada\n\n" \
                  f"Cliente: {cliente_seleccionado.get_nombre()}\n" \
                  f"Cédula: {cliente_seleccionado.get_cedula()}\n" \
                  f"Servicio: {servicio_actual.nombre}\n" \
                  f"Costo: ${costo:,.0f}"

        messagebox.showinfo("Reserva Exitosa", mensaje)
        actualizar_tabla_reservas()
        logger.info(f"Reserva realizada: {reserva.mostrar_reserva()}")
    except (ReservaError, ClienteError, ServicioError) as e:
        logger.error(e)
        messagebox.showerror("Error en la Reserva", str(e))



#Apartado para actualizar la tabla de reservas, mostrando información detallada de cada reserva y su estado actual.
def actualizar_tabla_reservas(): #
    """Actualiza la tabla de reservas."""
    for item in tabla_reservas.get_children():
        tabla_reservas.delete(item)

    for i, reserva in enumerate(reservas, 1):
        tabla_reservas.insert("", "end", values=(
            i,
            reserva.cliente.get_cedula(),
            reserva.cliente.get_nombre(),
            reserva.servicio.nombre,
            getattr(reserva.servicio, "horas", None) or getattr(reserva.servicio, "dias", None),
            f"${reserva.obtener_costo_total():,.0f}",
            reserva.estado
        ))



#Apartado para eliminar una reserva seleccionada de la tabla, con validación de selección.
def eliminar_reserva_seleccionada(): 
    """Elimina la reserva seleccionada de la tabla."""
    seleccion = tabla_reservas.selection()

    if not seleccion:
        messagebox.showwarning("Advertencia", "Selecciona una reserva para eliminar")
        return

    indice = tabla_reservas.index(seleccion[0])

    if indice < len(reservas):
        reserva = reservas.pop(indice)
        logger.info(f"Reserva eliminada: {reserva.mostrar_reserva()}")
        messagebox.showinfo("Éxito", "Reserva eliminada correctamente")
        actualizar_tabla_reservas()



#Apartado para editar el estado de una reserva seleccionada, mostrando un diálogo con opciones de estado.
def editar_reserva_seleccionada():
    """Abre un diálogo para editar el estado de una reserva."""
    seleccion = tabla_reservas.selection()

    if not seleccion:
        messagebox.showwarning("Advertencia", "Selecciona una reserva para editar")
        return

    indice = tabla_reservas.index(seleccion[0])

    if indice < len(reservas):
        reserva = reservas[indice]
        ventana_edicion = tk.Toplevel(ventana)
        ventana_edicion.title("Editar Estado de Reserva")
        ventana_edicion.geometry("400x200")
        ventana_edicion.configure(bg=COLOR_FONDO)

        tk.Label(ventana_edicion, text="Estado Actual:", font=("Arial", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5)
        tk.Label(ventana_edicion, text=reserva.estado, font=("Arial", 10), bg=COLOR_CARD, fg=COLOR_TEXTO, relief=tk.FLAT, pady=5).pack(fill=tk.X, padx=20)

        tk.Label(ventana_edicion, text="Nuevo Estado:", font=("Arial", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5)

        variable_estado = tk.StringVar(value=reserva.estado)
        combo_estado = ttk.Combobox(ventana_edicion, textvariable=variable_estado, values=["Pendiente", "Confirmada", "Cancelada"], state="readonly", width=30)
        combo_estado.pack(padx=20, pady=5)

        def guardar_edicion():
            nuevo_estado = variable_estado.get()
            try:
                reserva.editar_estado(nuevo_estado)
                messagebox.showinfo("Éxito", f"Reserva actualizada a estado: {nuevo_estado}")
                ventana_edicion.destroy()
                actualizar_tabla_reservas()
            except ReservaError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana_edicion, text="Guardar", command=guardar_edicion, bg=COLOR_EXITO, fg=COLOR_TEXTO, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=10).pack(pady=10)



#Apartado para actualizar el formulario de creación de servicios según el tipo de servicio seleccionado, mostrando u ocultando campos específicos.
def actualizar_formulario_servicio():
    """Actualiza el formulario según el tipo de servicio seleccionado."""
    tipo = servicio_tipo.get()
    if tipo == "Asesoría Especializada":
        label_especialista.pack(anchor=tk.W)
        entrada_especialista.pack(fill=tk.X, pady=(5, 10))
        label_duracion_servicio.config(text="Duración (horas):")
        entrada_nombre_servicio.delete(0, tk.END)
        entrada_nombre_servicio.insert(0, "Consultoría Python")
        entrada_duracion_servicio.delete(0, tk.END)
        entrada_duracion_servicio.insert(0, "2")
        entrada_especialista.delete(0, tk.END)
        entrada_especialista.insert(0, "Carlos")
    else:
        label_especialista.pack_forget()
        entrada_especialista.pack_forget()

        if tipo == "Reserva Sala":
            label_duracion_servicio.config(text="Duración (horas):")
            entrada_nombre_servicio.delete(0, tk.END)
            entrada_nombre_servicio.insert(0, "Sala VIP")
            entrada_duracion_servicio.delete(0, tk.END)
            entrada_duracion_servicio.insert(0, "1")
        else:
            label_duracion_servicio.config(text="Duración (días):")
            entrada_nombre_servicio.delete(0, tk.END)
            entrada_nombre_servicio.insert(0, "PC Gamer")
            entrada_duracion_servicio.delete(0, tk.END)
            entrada_duracion_servicio.insert(0, "3")



#Apartado para crear un servicio activo dinámico según el tipo seleccionado, con validaciones de campos y actualización de la información del servicio activo.
def crear_servicio():
    """Crea un servicio activo dinámico."""
    tipo = servicio_tipo.get()
    nombre = entrada_nombre_servicio.get().strip()
    precio_texto = entrada_precio_servicio.get().strip()
    duracion_texto = entrada_duracion_servicio.get().strip()
    especialista = entrada_especialista.get().strip()

    if not nombre or not precio_texto or not duracion_texto:
        messagebox.showerror("Error", "Todos los campos del servicio son obligatorios")
        return

    try:
        precio = float(precio_texto)
        duracion = int(duracion_texto)

        global servicio_actual

        if tipo == "Reserva Sala":
            servicio_actual = ReservaSala(nombre, precio, duracion)
        elif tipo == "Alquiler Equipo":
            servicio_actual = AlquilerEquipo(nombre, precio, duracion)
        else:
            if not especialista:
                raise ValueError("El especialista es obligatorio para la asesoría")
            servicio_actual = AsesoriaEspecializada(nombre, precio, duracion, especialista)

        actualizar_info_servicio()
        messagebox.showinfo("Servicio activo", f"Servicio actualizado: {servicio_actual.describir_servicio()}")
    except Exception as e:
        logger.error(e)
        messagebox.showerror("Error al crear servicio", str(e))


def actualizar_info_servicio():
    """Actualiza la información del servicio activo."""
    info_servicio.config(
        text=(
            f"🏢 Servicio: {servicio_actual.nombre} | "
            f"💰 Precio: ${servicio_actual.precio_base:,.0f} | "
            f"Detalle: {servicio_actual.describir_servicio()}"
        )
    )



#Apartado para agregar un comentario, asociado a un cliente seleccionado.
def agregar_comentario():

    cliente = combo_clientes_comentario.get()
    comentario = caja_comentario.get("1.0", tk.END).strip()

    if not cliente or not comentario:

        messagebox.showwarning(
            "Advertencia",
            "Debes seleccionar un cliente y escribir un comentario"
        )

        return

    comentarios.append({
        "cliente": cliente,
        "comentario": comentario
    })

    lista_comentarios.insert(
        tk.END,
        f"{cliente}: {comentario}"
    )

    caja_comentario.delete("1.0", tk.END)

    messagebox.showinfo(
        "Éxito",
        "Comentario agregado correctamente"
    )



    
# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Gestión de Reservas - Software FJ")
ventana.geometry("1200x800")
ventana.configure(bg=COLOR_FONDO)

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook",background=COLOR_FONDO,borderwidth=0)
style.configure("TNotebook.Tab",background=COLOR_SECUNDARIO,foreground=COLOR_TEXTO,padding=[15, 10],font=("Arial", 10, "bold"))
style.map("TNotebook.Tab",background=[("selected", COLOR_BOTON)],foreground=[("selected", COLOR_TEXTO)])
style.configure("Treeview",background=COLOR_CARD,foreground=COLOR_TEXTO,rowheight=28,fieldbackground=COLOR_CARD,bordercolor=COLOR_BORDER,font=("Arial", 10))
style.configure("Treeview.Heading",background=COLOR_HEADER,foreground=COLOR_ACENTO,font=("Arial", 10, "bold"))
style.map("Treeview",background=[("selected", COLOR_BOTON)])
style.configure("TCombobox",padding=5,font=("Arial", 10))

titulo = tk.Label(ventana,text="Sistema de Gestión de Reservas",font=("Arial", 20, "bold"),bg=COLOR_HEADER,fg=COLOR_ACENTO,pady=15)

titulo.pack(fill=tk.X)

# Notebook para pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# ============= PESTAÑA 1: REGISTRO DE CLIENTES =============
frame_clientes = ttk.Frame(notebook)
notebook.add(frame_clientes, text="📝 Registro de Clientes")

frame_entrada_clientes = tk.LabelFrame(frame_clientes, text="Registrar nuevo cliente", font=("Arial", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)
frame_entrada_clientes.pack(fill=tk.X, padx=10, pady=10)

tk.Label(frame_entrada_clientes, text="Cédula:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(10, 0))
entrada_cedula = tk.Entry(frame_entrada_clientes,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)
entrada_cedula.pack(fill=tk.X, padx=10, pady=(0, 10))

tk.Label(frame_entrada_clientes, text="Nombre completo:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(0, 0))
entrada_nombre = tk.Entry(frame_entrada_clientes,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)
entrada_nombre.pack(fill=tk.X, padx=10, pady=(0, 10))

tk.Label(frame_entrada_clientes, text="Correo electrónico:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(0, 0))
entrada_correo = tk.Entry(frame_entrada_clientes,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)
entrada_correo.pack(fill=tk.X, padx=10, pady=(0, 10))

boton_registrar = tk.Button(frame_entrada_clientes, text="✓ REGISTRAR CLIENTE", command=registrar_cliente, bg=COLOR_BOTON, fg=COLOR_TEXTO, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=10)
boton_registrar.pack(fill=tk.X, padx=10, pady=(0, 10))
boton_registrar.bind("<Enter>", on_enter)
boton_registrar.bind("<Leave>", on_leave)

frame_tabla_clientes = tk.LabelFrame(frame_clientes, text="Clientes registrados", font=("Arial", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)
frame_tabla_clientes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columnas_clientes = ("ID", "Cédula", "Nombre", "Correo")
tabla_clientes = ttk.Treeview(frame_tabla_clientes, columns=columnas_clientes, height=15)
tabla_clientes.column("#0", width=0, stretch=tk.NO)
tabla_clientes.column("ID", anchor=tk.CENTER, width=50)
tabla_clientes.column("Cédula", anchor=tk.CENTER, width=100)
tabla_clientes.column("Nombre", anchor=tk.W, width=200)
tabla_clientes.column("Correo", anchor=tk.W, width=250)

tabla_clientes.heading("#0", text="", anchor=tk.W)
tabla_clientes.heading("ID", text="ID", anchor=tk.CENTER)
tabla_clientes.heading("Cédula", text="Cédula", anchor=tk.CENTER)
tabla_clientes.heading("Nombre", text="Nombre", anchor=tk.W)
tabla_clientes.heading("Correo", text="Correo", anchor=tk.W)

tabla_clientes.pack(fill=tk.BOTH, expand=True)




# ============= PESTAÑA 2: GESTIÓN DE RESERVAS =============
frame_reservas = ttk.Frame(notebook)
notebook.add(frame_reservas, text="🎫 Gestión de Reservas")

frame_config_servicio = tk.LabelFrame(frame_reservas, text="Configurar servicio", font=("Arial", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)
frame_config_servicio.pack(fill=tk.X, padx=10, pady=10)

tk.Label(frame_config_servicio, text="Tipo de servicio:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(10, 0))
servicio_tipo = tk.StringVar(value="Reserva Sala")
combo_tipo = ttk.Combobox(frame_config_servicio, textvariable=servicio_tipo, values=["Reserva Sala", "Alquiler Equipo", "Asesoría Especializada"], state="readonly", width=30)
combo_tipo.pack(fill=tk.X, padx=10, pady=(0, 10))
combo_tipo.bind("<<ComboboxSelected>>", lambda _: actualizar_formulario_servicio())

tk.Label(frame_config_servicio, text="Nombre:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10)
entrada_nombre_servicio = tk.Entry(frame_config_servicio,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)
entrada_nombre_servicio.pack(fill=tk.X, padx=10, pady=(0, 10))
entrada_nombre_servicio.insert(0, "Sala VIP")

tk.Label(frame_config_servicio, text="Precio base ($):", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10)
entrada_precio_servicio = tk.Entry(frame_config_servicio,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)
entrada_precio_servicio.pack(fill=tk.X, padx=10, pady=(0, 10))
entrada_precio_servicio.insert(0, "50000")

label_duracion_servicio = tk.Label(frame_config_servicio, text="Duración (horas):", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)
label_duracion_servicio.pack(anchor=tk.W, padx=10)
entrada_duracion_servicio = tk.Entry(frame_config_servicio,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)
entrada_duracion_servicio.pack(fill=tk.X, padx=10, pady=(0, 10))
entrada_duracion_servicio.insert(0, "1")

label_especialista = tk.Label(frame_config_servicio, text="Especialista:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)
entrada_especialista = tk.Entry(frame_config_servicio,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)
entrada_especialista.insert(0, "Carlos")

boton_crear_servicio = tk.Button(frame_config_servicio, text="✅ Crear servicio activo", command=crear_servicio, bg=COLOR_EXITO, fg=COLOR_TEXTO, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=10)
boton_crear_servicio.pack(fill=tk.X, padx=10, pady=(0, 10))
boton_crear_servicio.bind("<Enter>", on_enter)
boton_crear_servicio.bind("<Leave>", on_leave)

frame_nueva_reserva = tk.LabelFrame(frame_reservas, text="Crear nueva reserva", font=("Arial", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)
frame_nueva_reserva.pack(fill=tk.X, padx=10, pady=10)

tk.Label(frame_nueva_reserva, text="Seleccionar cliente:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(10, 0))
combo_clientes = ttk.Combobox(frame_nueva_reserva, state="readonly", width=40)
combo_clientes.pack(fill=tk.X, padx=10, pady=(0, 10))

boton_reserva = tk.Button(frame_nueva_reserva, text="🎫 REALIZAR RESERVA", command=hacer_reserva, bg=COLOR_SECUNDARIO, fg=COLOR_TEXTO, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=10)
boton_reserva.pack(fill=tk.X, padx=10, pady=(0, 10))
boton_reserva.bind("<Enter>", on_enter)
boton_reserva.bind("<Leave>", on_leave)

frame_tabla_reservas = tk.LabelFrame(frame_reservas, text="Reservas confirmadas", font=("Arial", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)
frame_tabla_reservas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columnas_reservas = ("#", "Cédula", "Cliente", "Servicio", "Duración", "Costo Total", "Estado")
tabla_reservas = ttk.Treeview(frame_tabla_reservas, columns=columnas_reservas, height=12)
tabla_reservas.column("#0", width=0, stretch=tk.NO)
tabla_reservas.column("#", anchor=tk.CENTER, width=40)
tabla_reservas.column("Cédula", anchor=tk.CENTER, width=90)
tabla_reservas.column("Cliente", anchor=tk.W, width=120)
tabla_reservas.column("Servicio", anchor=tk.W, width=120)
tabla_reservas.column("Duración", anchor=tk.CENTER, width=80)
tabla_reservas.column("Costo Total", anchor=tk.CENTER, width=100)
tabla_reservas.column("Estado", anchor=tk.CENTER, width=90)

tabla_reservas.heading("#0", text="", anchor=tk.W)
tabla_reservas.heading("#", text="#", anchor=tk.CENTER)
tabla_reservas.heading("Cédula", text="Cédula", anchor=tk.CENTER)
tabla_reservas.heading("Cliente", text="Cliente", anchor=tk.W)
tabla_reservas.heading("Servicio", text="Servicio", anchor=tk.W)
tabla_reservas.heading("Duración", text="Duración", anchor=tk.CENTER)
tabla_reservas.heading("Costo Total", text="Costo Total", anchor=tk.CENTER)
tabla_reservas.heading("Estado", text="Estado", anchor=tk.CENTER)

tabla_reservas.pack(fill=tk.BOTH, expand=True)

frame_botones_reservas = tk.Frame(frame_reservas, bg=COLOR_FONDO)
frame_botones_reservas.pack(fill=tk.X, padx=10, pady=10)

boton_editar = tk.Button(frame_botones_reservas, text="✏️ Editar", command=editar_reserva_seleccionada, bg="#ffc107", fg="#000", font=("Arial", 10, "bold"), relief=tk.FLAT, padx=15, pady=8)
boton_editar.pack(side=tk.LEFT, padx=5)
boton_editar.bind("<Enter>", on_enter)
boton_editar.bind("<Leave>", on_leave)

boton_eliminar = tk.Button(frame_botones_reservas, text="🗑️ Eliminar", command=eliminar_reserva_seleccionada, bg=COLOR_ERROR, fg=COLOR_TEXTO, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=15, pady=8)
boton_eliminar.pack(side=tk.LEFT, padx=5)
boton_eliminar.bind("<Enter>", on_enter)
boton_eliminar.bind("<Leave>", on_leave)

# ============= PESTAÑA 3: BÚSQUEDA =============
frame_busqueda = ttk.Frame(notebook)
notebook.add(frame_busqueda, text="🔍 Búsqueda de Clientes")

frame_busqueda_clientes = tk.LabelFrame(frame_busqueda, text="Buscar cliente por cédula", font=("Arial", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)
frame_busqueda_clientes.pack(fill=tk.X, padx=10, pady=10)

tk.Label(frame_busqueda_clientes, text="Ingresa la cédula:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(10, 0))
entrada_busqueda_cedula = tk.Entry(frame_busqueda_clientes,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)
entrada_busqueda_cedula.pack(fill=tk.X, padx=10, pady=(0, 10))

boton_buscar = tk.Button(frame_busqueda_clientes, text="🔍 BUSCAR", command=buscar_cliente_por_cedula, bg=COLOR_BOTON, fg=COLOR_TEXTO, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=10)
boton_buscar.pack(fill=tk.X, padx=10, pady=(0, 10))
boton_buscar.bind("<Enter>", on_enter)
boton_buscar.bind("<Leave>", on_leave)




# ============= PESTAÑA 4: COMENTARIOS =============

frame_comentarios = tk.Frame(notebook, bg=COLOR_FONDO)

notebook.add(
    frame_comentarios,
    text="💬 Comentarios"
)

tk.Label(
    frame_comentarios,
    text="Seleccionar cliente:",
    font=("Arial", 10, "bold"),
    bg=COLOR_CARD,
    fg=COLOR_TEXTO
).pack(anchor=tk.W, padx=10, pady=(10, 0))

combo_clientes_comentario = ttk.Combobox(
    frame_comentarios,
    state="readonly",
    width=40
)

combo_clientes_comentario.pack(
    fill=tk.X,
    padx=10,
    pady=(0, 10)
)

tk.Label(
    frame_comentarios,
    text="Comentario:",
    font=("Arial", 10, "bold"),
    bg=COLOR_CARD,
    fg=COLOR_TEXTO
).pack(anchor=tk.W, padx=10)

caja_comentario = tk.Text(
    frame_comentarios,
    height=5,
    font=("Arial", 10),
    bg=COLOR_INPUT,
    fg=COLOR_TEXTO,
    insertbackground=COLOR_TEXTO,
    relief=tk.FLAT,
    bd=2
)

caja_comentario.pack(
    fill=tk.X,
    padx=10,
    pady=(0, 10)
)

boton_comentario = tk.Button(
    frame_comentarios,
    text="💬 Guardar comentario",
    command=agregar_comentario,
    bg=COLOR_BOTON,
    fg=COLOR_TEXTO,
    font=("Arial", 10, "bold"),
    relief=tk.FLAT,
    padx=20,
    pady=10
)

boton_comentario.pack(
    padx=10,
    pady=(0, 10)
)

boton_comentario.bind("<Enter>", on_enter)
boton_comentario.bind("<Leave>", on_leave)

lista_comentarios = tk.Listbox(
    frame_comentarios,
    font=("Arial", 10),
    height=10,
    bg=COLOR_INPUT,
    fg=COLOR_TEXTO,
    relief=tk.FLAT,
    bd=2
)

lista_comentarios.pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=10
)



# ============= INFORMACIÓN DEL SERVICIO ACTIVO =============
frame_servicio = tk.Frame(ventana,bg=COLOR_HEADER,relief=tk.FLAT,bd=1)
frame_servicio.pack(fill=tk.X, padx=5, pady=5)

info_servicio = tk.Label(frame_servicio,text="",font=("Arial", 9),bg=COLOR_HEADER,fg=COLOR_ACENTO)
info_servicio.pack(padx=10, pady=10)

actualizar_formulario_servicio()
actualizar_info_servicio()

# Inicia el bucle principal
ventana.mainloop()