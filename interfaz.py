import tkinter as tk  # importa el módulo o símbolo necesario
from tkinter import messagebox, scrolledtext, ttk  # importa la clase o excepción necesaria
import re  # importa el módulo o símbolo necesario

from cliente import Cliente  # importa la clase o excepción necesaria
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada  # importa la clase o excepción necesaria
from reserva import Reserva  # importa la clase o excepción necesaria
from excepciones import ClienteError, ReservaError, ServicioError  # importa la clase o excepción necesaria
from logger_config import logger  # importa la clase o excepción necesaria

# Listas globales
clientes = []  # asigna un valor a una variable o atributo
reservas = []  # asigna un valor a una variable o atributo
comentarios = []  # asigna un valor a una variable o atributo
# Servicio activo
servicio_actual = ReservaSala("Sala VIP", 50000, 1)  # asigna un valor a una variable o atributo

# Colores
COLOR_FONDO = "#151a2e"  # asigna un valor a una variable o atributo
COLOR_HEADER = "#1b2440"  # asigna un valor a una variable o atributo
COLOR_SECUNDARIO = "#2b3a67"  # asigna un valor a una variable o atributo
COLOR_ACENTO = "#8be9fd"  # asigna un valor a una variable o atributo
COLOR_BOTON = "#4b6cb7"  # asigna un valor a una variable o atributo
COLOR_BOTON_HOVER = "#5c7cfa"  # asigna un valor a una variable o atributo
COLOR_EXITO = "#7bd88f"  # asigna un valor a una variable o atributo
COLOR_ERROR = "#ff6b81"  # asigna un valor a una variable o atributo
COLOR_TEXTO = "#f4f7ff"  # asigna un valor a una variable o atributo
COLOR_CARD = "#222b45"  # asigna un valor a una variable o atributo
COLOR_INPUT = "#364269"  # asigna un valor a una variable o atributo
COLOR_BORDER = "#3d4c72"  # asigna un valor a una variable o atributo

# Hover botones
def on_enter(e):  # ejecuta la instrucción correspondiente
    e.widget['background'] = COLOR_BOTON_HOVER  # asigna un valor a una variable o atributo

def on_leave(e):  # ejecuta la instrucción correspondiente
    e.widget['background'] = COLOR_BOTON  # asigna un valor a una variable o atributo

#Apartado para registrar clientes, con validaciones de campos.
def registrar_cliente():  # define el método para registrar clientes
    """Registra un cliente con cédula, nombre y correo."""
    cedula = entrada_cedula.get().strip()  # asigna un valor a una variable o atributo
    nombre = entrada_nombre.get().strip()  # asigna un valor a una variable o atributo
    correo = entrada_correo.get().strip()  # asigna un valor a una variable o atributo

    if not cedula or not nombre or not correo:  # verifica que todos los campos estén completos
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")  # muestra un cuadro de diálogo al usuario
        return  # ejecuta la instrucción correspondiente

    if not cedula.isdigit():  # verifica que la cédula solo tenga números
        messagebox.showerror("Error", "La cédula solo debe contener números")  # muestra un cuadro de diálogo al usuario
        return  # ejecuta la instrucción correspondiente

    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚ ]+$", nombre):  # verifica que el dato cumpla con el patrón definido
        messagebox.showerror("Error", "El nombre solo debe contener letras y espacios")  # muestra un cuadro de diálogo al usuario
        return  # ejecuta la instrucción correspondiente

    for cliente in clientes:  # itera sobre elementos de una colección
        if cliente.get_cedula() == cedula:  # evalúa una condición para decidir el flujo
            messagebox.showerror("Error", f"La cédula {cedula} ya está registrada")  # muestra un cuadro de diálogo al usuario
            return  # ejecuta la instrucción correspondiente

    try:  # inicia un bloque try para manejo de excepciones
        cliente = Cliente(nombre, correo, cedula)  # asigna un valor a una variable o atributo
        clientes.append(cliente)  # agrega un elemento a la lista
        logger.info(f"Cliente registrado: {cliente.mostrar_info()}")  # registra un evento informativo en el log
        messagebox.showinfo("Éxito", f"Cliente {nombre} registrado correctamente")  # muestra un cuadro de diálogo al usuario

        entrada_cedula.delete(0, tk.END)  # ejecuta la instrucción correspondiente
        entrada_nombre.delete(0, tk.END)  # ejecuta la instrucción correspondiente
        entrada_correo.delete(0, tk.END)  # ejecuta la instrucción correspondiente
        actualizar_tabla_clientes()  # ejecuta la instrucción correspondiente
    except ClienteError as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        messagebox.showerror("Error de validación", str(e))  # muestra un cuadro de diálogo al usuario



#Apartado para actualizar la tabla de clientes cada vez que se registre un nuevo cliente o se realice una búsqueda.
def actualizar_tabla_clientes():  # define el método para actualizar la tabla de clientes
    """Actualiza la tabla de clientes con estilo similar a Excel."""
    for item in tabla_clientes.get_children():  # itera sobre elementos de una colección
        tabla_clientes.delete(item)  # ejecuta la instrucción correspondiente

    for cliente in clientes:  # itera sobre elementos de una colección
        tabla_clientes.insert("", "end", values=(  # inserta una fila en la tabla
            cliente.get_id(),  # ejecuta la instrucción correspondiente
            cliente.get_cedula(),  # ejecuta la instrucción correspondiente
            cliente.get_nombre(),  # ejecuta la instrucción correspondiente
            cliente.get_correo()  # ejecuta la instrucción correspondiente
        ))  # ejecuta la instrucción correspondiente

    actualizar_dropdown_clientes()  # ejecuta la instrucción correspondiente


#Apartado para actualizar el menú desplegable de clientes.
def actualizar_dropdown_clientes():  # ejecuta la instrucción correspondiente

    valores = [  # asigna un valor a una variable o atributo
        f"{c.get_cedula()} - {c.get_nombre()}"  # ejecuta la instrucción correspondiente
        for c in clientes  # itera sobre elementos de una colección
    ]  # ejecuta la instrucción correspondiente

    combo_clientes['values'] = valores  # asigna un valor a una variable o atributo

    combo_clientes_comentario['values'] = valores  # asigna un valor a una variable o atributo

    if valores:  # evalúa una condición para decidir el flujo

        combo_clientes.current(0)  # ejecuta la instrucción correspondiente

        combo_clientes_comentario.current(0)  # ejecuta la instrucción correspondiente



#Apartado para buscar un cliente por cédula, mostrando su información y reservas asociadas.
def buscar_cliente_por_cedula():  # define el método para buscar clientes por cédula
    """Busca un cliente por cédula."""
    cedula_busqueda = entrada_busqueda_cedula.get().strip()  # asigna un valor a una variable o atributo

    if not cedula_busqueda:  # evalúa una condición para decidir el flujo
        messagebox.showwarning("Advertencia", "Ingresa una cédula para buscar")  # muestra un cuadro de diálogo al usuario
        return  # ejecuta la instrucción correspondiente

    cliente_encontrado = None  # asigna un valor a una variable o atributo
    for cliente in clientes:  # itera sobre elementos de una colección
        if cliente.get_cedula() == cedula_busqueda:  # evalúa una condición para decidir el flujo
            cliente_encontrado = cliente  # asigna un valor a una variable o atributo
            break  # ejecuta la instrucción correspondiente

    if not cliente_encontrado:  # verifica si no se encontró el cliente
        messagebox.showinfo("Búsqueda", f"No se encontró cliente con cédula {cedula_busqueda}")  # muestra un cuadro de diálogo al usuario
        return  # ejecuta la instrucción correspondiente

    reservas_cliente = [r for r in reservas if r.cliente.get_cedula() == cedula_busqueda]  # ejecuta la instrucción correspondiente

    info_resultado = f"Cliente encontrado:\n{cliente_encontrado.mostrar_info()}\n\n"  # asigna un valor a una variable o atributo
    info_resultado += f"Reservas ({len(reservas_cliente)}):\n"  # asigna un valor a una variable o atributo

    if reservas_cliente:  # evalúa una condición para decidir el flujo
        for i, reserva in enumerate(reservas_cliente, 1):  # itera sobre elementos de una colección
            info_resultado += f"{i}. {reserva.mostrar_reserva()}\n"  # asigna un valor a una variable o atributo
    else:  # se ejecuta cuando no ocurre una excepción
        info_resultado += "Sin reservas registradas"  # asigna un valor a una variable o atributo

    messagebox.showinfo("Resultado de búsqueda", info_resultado)  # muestra un cuadro de diálogo al usuario



#Apartado para realizar una reserva, con validaciones de selección de cliente y servicio activo.
def hacer_reserva():  # define el método para crear reservas
    """Crea y confirma una reserva."""
    seleccion = combo_clientes.get()  # asigna un valor a una variable o atributo

    if not seleccion:  # evalúa una condición para decidir el flujo
        messagebox.showerror("Error", "Debes seleccionar un cliente")  # muestra un cuadro de diálogo al usuario
        return  # ejecuta la instrucción correspondiente

    if len(clientes) == 0:  # evalúa una condición para decidir el flujo
        messagebox.showerror("Error", "No hay clientes registrados")  # muestra un cuadro de diálogo al usuario
        return  # ejecuta la instrucción correspondiente

    cliente_seleccionado = None  # asigna un valor a una variable o atributo
    for cliente in clientes:  # itera sobre elementos de una colección
        if f"{cliente.get_cedula()} - {cliente.get_nombre()}" == seleccion:  # evalúa una condición para decidir el flujo
            cliente_seleccionado = cliente  # asigna un valor a una variable o atributo
            break  # ejecuta la instrucción correspondiente

    if not cliente_seleccionado:  # evalúa una condición para decidir el flujo
        messagebox.showerror("Error", "Cliente no encontrado")  # muestra un cuadro de diálogo al usuario
        return  # ejecuta la instrucción correspondiente

    try:  # inicia un bloque try para manejo de excepciones
        reserva = Reserva(cliente_seleccionado, servicio_actual)  # asigna un valor a una variable o atributo
        reserva.confirmar()  # ejecuta la instrucción correspondiente
        reservas.append(reserva)  # agrega un elemento a la lista

        costo = reserva.obtener_costo_total()  # asigna un valor a una variable o atributo
        mensaje = f"✓ Reserva Confirmada\n\n" \
                  f"Cliente: {cliente_seleccionado.get_nombre()}\n" \
                  f"Cédula: {cliente_seleccionado.get_cedula()}\n" \
                  f"Servicio: {servicio_actual.nombre}\n" \
                  f"Costo: ${costo:,.0f}"  # ejecuta la instrucción correspondiente

        messagebox.showinfo("Reserva Exitosa", mensaje)  # muestra un cuadro de diálogo al usuario
        actualizar_tabla_reservas()  # ejecuta la instrucción correspondiente
        logger.info(f"Reserva realizada: {reserva.mostrar_reserva()}")  # registra un evento informativo en el log
    except (ReservaError, ClienteError, ServicioError) as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        messagebox.showerror("Error en la Reserva", str(e))  # muestra un cuadro de diálogo al usuario



#Apartado para actualizar la tabla de reservas, mostrando información detallada de cada reserva y su estado actual.
def actualizar_tabla_reservas(): #  # ejecuta la instrucción correspondiente
    """Actualiza la tabla de reservas."""
    for item in tabla_reservas.get_children():  # itera sobre elementos de una colección
        tabla_reservas.delete(item)  # ejecuta la instrucción correspondiente

    for i, reserva in enumerate(reservas, 1):  # itera sobre elementos de una colección
        tabla_reservas.insert("", "end", values=(  # inserta una fila en la tabla
            i,  # ejecuta la instrucción correspondiente
            reserva.cliente.get_cedula(),  # ejecuta la instrucción correspondiente
            reserva.cliente.get_nombre(),  # ejecuta la instrucción correspondiente
            reserva.servicio.nombre,  # ejecuta la instrucción correspondiente
            getattr(reserva.servicio, "horas", None) or getattr(reserva.servicio, "dias", None),  # ejecuta la instrucción correspondiente
            f"${reserva.obtener_costo_total():,.0f}",  # ejecuta la instrucción correspondiente
            reserva.estado  # ejecuta la instrucción correspondiente
        ))  # ejecuta la instrucción correspondiente



#Apartado para eliminar una reserva seleccionada de la tabla, con validación de selección.
def eliminar_reserva_seleccionada():  # define el método para eliminar reservas seleccionadas
    """Elimina la reserva seleccionada de la tabla."""
    seleccion = tabla_reservas.selection()  # asigna un valor a una variable o atributo

    if not seleccion:  # evalúa una condición para decidir el flujo
        messagebox.showwarning("Advertencia", "Selecciona una reserva para eliminar")  # muestra un cuadro de diálogo al usuario
        return  # ejecuta la instrucción correspondiente

    indice = tabla_reservas.index(seleccion[0])  # asigna un valor a una variable o atributo

    if indice < len(reservas):  # evalúa una condición para decidir el flujo
        reserva = reservas.pop(indice)  # asigna un valor a una variable o atributo
        logger.info(f"Reserva eliminada: {reserva.mostrar_reserva()}")  # registra un evento informativo en el log
        messagebox.showinfo("Éxito", "Reserva eliminada correctamente")  # muestra un cuadro de diálogo al usuario
        actualizar_tabla_reservas()  # ejecuta la instrucción correspondiente



#Apartado para editar el estado de una reserva seleccionada, mostrando un diálogo con opciones de estado.
def editar_reserva_seleccionada():  # define el método para editar reservas seleccionadas
    """Abre un diálogo para editar el estado de una reserva."""
    seleccion = tabla_reservas.selection()  # asigna un valor a una variable o atributo

    if not seleccion:  # evalúa una condición para decidir el flujo
        messagebox.showwarning("Advertencia", "Selecciona una reserva para editar")  # muestra un cuadro de diálogo al usuario
        return  # ejecuta la instrucción correspondiente

    indice = tabla_reservas.index(seleccion[0])  # asigna un valor a una variable o atributo

    if indice < len(reservas):  # evalúa una condición para decidir el flujo
        reserva = reservas[indice]  # asigna un valor a una variable o atributo
        ventana_edicion = tk.Toplevel(ventana)  # asigna un valor a una variable o atributo
        ventana_edicion.title("Editar Estado de Reserva")  # ejecuta la instrucción correspondiente
        ventana_edicion.geometry("400x200")  # ejecuta la instrucción correspondiente
        ventana_edicion.configure(bg=COLOR_FONDO)  # asigna un valor a una variable o atributo

        tk.Label(ventana_edicion, text="Estado Actual:", font=("Arial", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5)  # crea una etiqueta de texto en la interfaz
        tk.Label(ventana_edicion, text=reserva.estado, font=("Arial", 10), bg=COLOR_CARD, fg=COLOR_TEXTO, relief=tk.FLAT, pady=5).pack(fill=tk.X, padx=20)  # crea una etiqueta de texto en la interfaz

        tk.Label(ventana_edicion, text="Nuevo Estado:", font=("Arial", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5)  # crea una etiqueta de texto en la interfaz

        variable_estado = tk.StringVar(value=reserva.estado)  # ejecuta la instrucción correspondiente
        combo_estado = ttk.Combobox(ventana_edicion, textvariable=variable_estado, values=["Pendiente", "Confirmada", "Cancelada"], state="readonly", width=30)  # crea una lista desplegable
        combo_estado.pack(padx=20, pady=5)  # posiciona el widget en la interfaz

        def guardar_edicion():  # ejecuta la instrucción correspondiente
            nuevo_estado = variable_estado.get()  # asigna un valor a una variable o atributo
            try:  # inicia un bloque try para manejo de excepciones
                reserva.editar_estado(nuevo_estado)  # ejecuta la instrucción correspondiente
                messagebox.showinfo("Éxito", f"Reserva actualizada a estado: {nuevo_estado}")  # muestra un cuadro de diálogo al usuario
                ventana_edicion.destroy()  # ejecuta la instrucción correspondiente
                actualizar_tabla_reservas()  # ejecuta la instrucción correspondiente
            except ReservaError as e:  # captura la excepción lanzada en el bloque try
                messagebox.showerror("Error", str(e))  # muestra un cuadro de diálogo al usuario

        tk.Button(ventana_edicion, text="Guardar", command=guardar_edicion, bg=COLOR_EXITO, fg=COLOR_TEXTO, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=10).pack(pady=10)  # crea un botón interactivo



#Apartado para actualizar el formulario de creación de servicios según el tipo de servicio seleccionado, mostrando u ocultando campos específicos.
def actualizar_formulario_servicio():  # define el método para actualizar el formulario de servicio
    """Actualiza el formulario según el tipo de servicio seleccionado."""
    tipo = servicio_tipo.get()  # asigna un valor a una variable o atributo
    if tipo == "Asesoría Especializada":  # evalúa una condición para decidir el flujo
        label_especialista.pack(anchor=tk.W)  # posiciona el widget en la interfaz
        entrada_especialista.pack(fill=tk.X, pady=(5, 10))  # posiciona el widget en la interfaz
        label_duracion_servicio.config(text="Duración (horas):")  # asigna un valor a una variable o atributo
        entrada_nombre_servicio.delete(0, tk.END)  # ejecuta la instrucción correspondiente
        entrada_nombre_servicio.insert(0, "Consultoría Python")  # ejecuta la instrucción correspondiente
        entrada_duracion_servicio.delete(0, tk.END)  # ejecuta la instrucción correspondiente
        entrada_duracion_servicio.insert(0, "2")  # ejecuta la instrucción correspondiente
        entrada_especialista.delete(0, tk.END)  # ejecuta la instrucción correspondiente
        entrada_especialista.insert(0, "Carlos")  # ejecuta la instrucción correspondiente
    else:  # se ejecuta cuando no ocurre una excepción
        label_especialista.pack_forget()  # ejecuta la instrucción correspondiente
        entrada_especialista.pack_forget()  # ejecuta la instrucción correspondiente

        if tipo == "Reserva Sala":  # evalúa una condición para decidir el flujo
            label_duracion_servicio.config(text="Duración (horas):")  # asigna un valor a una variable o atributo
            entrada_nombre_servicio.delete(0, tk.END)  # ejecuta la instrucción correspondiente
            entrada_nombre_servicio.insert(0, "Sala VIP")  # ejecuta la instrucción correspondiente
            entrada_duracion_servicio.delete(0, tk.END)  # ejecuta la instrucción correspondiente
            entrada_duracion_servicio.insert(0, "1")  # ejecuta la instrucción correspondiente
        else:  # se ejecuta cuando no ocurre una excepción
            label_duracion_servicio.config(text="Duración (días):")  # asigna un valor a una variable o atributo
            entrada_nombre_servicio.delete(0, tk.END)  # ejecuta la instrucción correspondiente
            entrada_nombre_servicio.insert(0, "PC Gamer")  # ejecuta la instrucción correspondiente
            entrada_duracion_servicio.delete(0, tk.END)  # ejecuta la instrucción correspondiente
            entrada_duracion_servicio.insert(0, "3")  # ejecuta la instrucción correspondiente



#Apartado para crear un servicio activo dinámico según el tipo seleccionado, con validaciones de campos y actualización de la información del servicio activo.
def crear_servicio():  # define el método para crear un servicio activo
    """Crea un servicio activo dinámico."""
    tipo = servicio_tipo.get()  # asigna un valor a una variable o atributo
    nombre = entrada_nombre_servicio.get().strip()  # asigna un valor a una variable o atributo
    precio_texto = entrada_precio_servicio.get().strip()  # asigna un valor a una variable o atributo
    duracion_texto = entrada_duracion_servicio.get().strip()  # asigna un valor a una variable o atributo
    especialista = entrada_especialista.get().strip()  # asigna un valor a una variable o atributo

    if not nombre or not precio_texto or not duracion_texto:  # evalúa una condición para decidir el flujo
        messagebox.showerror("Error", "Todos los campos del servicio son obligatorios")  # muestra un cuadro de diálogo al usuario
        return  # ejecuta la instrucción correspondiente

    try:  # inicia un bloque try para manejo de excepciones
        precio = float(precio_texto)  # asigna un valor a una variable o atributo
        duracion = int(duracion_texto)  # asigna un valor a una variable o atributo

        global servicio_actual  # ejecuta la instrucción correspondiente

        if tipo == "Reserva Sala":  # evalúa una condición para decidir el flujo
            servicio_actual = ReservaSala(nombre, precio, duracion)  # asigna un valor a una variable o atributo
        elif tipo == "Alquiler Equipo":  # evalúa una condición alternativa
            servicio_actual = AlquilerEquipo(nombre, precio, duracion)  # asigna un valor a una variable o atributo
        else:  # se ejecuta cuando no ocurre una excepción
            if not especialista:  # evalúa una condición para decidir el flujo
                raise ValueError("El especialista es obligatorio para la asesoría")  # lanza una excepción cuando ocurre un error
            servicio_actual = AsesoriaEspecializada(nombre, precio, duracion, especialista)  # asigna un valor a una variable o atributo

        actualizar_info_servicio()  # ejecuta la instrucción correspondiente
        messagebox.showinfo("Servicio activo", f"Servicio actualizado: {servicio_actual.describir_servicio()}")  # muestra un cuadro de diálogo al usuario
    except Exception as e:  # captura la excepción lanzada en el bloque try
        logger.error(e)  # registra un error en el log
        messagebox.showerror("Error al crear servicio", str(e))  # muestra un cuadro de diálogo al usuario


def actualizar_info_servicio():  # define el método para actualizar la información del servicio activo
    """Actualiza la información del servicio activo."""
    info_servicio.config(  # ejecuta la instrucción correspondiente
        text=(  # asigna un valor a una variable o atributo
            f"🏢 Servicio: {servicio_actual.nombre} | "  # ejecuta la instrucción correspondiente
            f"💰 Precio: ${servicio_actual.precio_base:,.0f} | "  # ejecuta la instrucción correspondiente
            f"Detalle: {servicio_actual.describir_servicio()}"  # ejecuta la instrucción correspondiente
        )  # ejecuta la instrucción correspondiente
    )  # ejecuta la instrucción correspondiente



#Apartado para agregar un comentario, asociado a un cliente seleccionado.
def agregar_comentario():  # define el método para agregar comentarios asociados al cliente

    cliente = combo_clientes_comentario.get()  # asigna un valor a una variable o atributo
    comentario = caja_comentario.get("1.0", tk.END).strip()  # asigna un valor a una variable o atributo

    if not cliente or not comentario:  # evalúa una condición para decidir el flujo

        messagebox.showwarning(  # muestra un cuadro de diálogo al usuario
            "Advertencia",  # ejecuta la instrucción correspondiente
            "Debes seleccionar un cliente y escribir un comentario"  # ejecuta la instrucción correspondiente
        )  # ejecuta la instrucción correspondiente

        return  # ejecuta la instrucción correspondiente

    comentarios.append({  # agrega un elemento a la lista
        "cliente": cliente,  # ejecuta la instrucción correspondiente
        "comentario": comentario  # ejecuta la instrucción correspondiente
    })  # ejecuta la instrucción correspondiente

    lista_comentarios.insert(  # ejecuta la instrucción correspondiente
        tk.END,  # ejecuta la instrucción correspondiente
        f"{cliente}: {comentario}"  # ejecuta la instrucción correspondiente
    )  # ejecuta la instrucción correspondiente

    caja_comentario.delete("1.0", tk.END)  # ejecuta la instrucción correspondiente

    messagebox.showinfo(  # muestra un cuadro de diálogo al usuario
        "Éxito",  # ejecuta la instrucción correspondiente
        "Comentario agregado correctamente"  # ejecuta la instrucción correspondiente
    )  # ejecuta la instrucción correspondiente



    
# Configuración de la ventana principal
ventana = tk.Tk()  # asigna un valor a una variable o atributo
ventana.title("Sistema de Gestión de Reservas - Software FJ")  # ejecuta la instrucción correspondiente
ventana.geometry("1200x800")  # ejecuta la instrucción correspondiente
ventana.configure(bg=COLOR_FONDO)  # asigna un valor a una variable o atributo

style = ttk.Style()  # asigna un valor a una variable o atributo
style.theme_use("clam")  # ejecuta la instrucción correspondiente
style.configure("TNotebook",background=COLOR_FONDO,borderwidth=0)  # ejecuta la instrucción correspondiente
style.configure("TNotebook.Tab",background=COLOR_SECUNDARIO,foreground=COLOR_TEXTO,padding=[15, 10],font=("Arial", 10, "bold"))  # ejecuta la instrucción correspondiente
style.map("TNotebook.Tab",background=[("selected", COLOR_BOTON)],foreground=[("selected", COLOR_TEXTO)])  # ejecuta la instrucción correspondiente
style.configure("Treeview",background=COLOR_CARD,foreground=COLOR_TEXTO,rowheight=28,fieldbackground=COLOR_CARD,bordercolor=COLOR_BORDER,font=("Arial", 10))  # ejecuta la instrucción correspondiente
style.configure("Treeview.Heading",background=COLOR_HEADER,foreground=COLOR_ACENTO,font=("Arial", 10, "bold"))  # ejecuta la instrucción correspondiente
style.map("Treeview",background=[("selected", COLOR_BOTON)])  # asigna un valor a una variable o atributo
style.configure("TCombobox",padding=5,font=("Arial", 10))  # ejecuta la instrucción correspondiente

# Contenedor desplazable para todo el contenido de la ventana
canvas_principal = tk.Canvas(ventana, bg=COLOR_FONDO, highlightthickness=0)  # crea un canvas para contener el contenido desplazable
scrollbar_principal = ttk.Scrollbar(ventana, orient="vertical", command=canvas_principal.yview)  # crea el scrollbar vertical principal
detail_frame = tk.Frame(canvas_principal, bg=COLOR_FONDO)  # contenedor interno para el contenido
canvas_window = canvas_principal.create_window((0, 0), window=detail_frame, anchor="nw")  # inserta el contenedor en el canvas

canvas_principal.configure(yscrollcommand=scrollbar_principal.set)  # conecta la barra de desplazamiento con el canvas

def actualizar_scrollregion(event):  # actualiza la región desplazable cuando cambia el tamaño
    canvas_principal.configure(scrollregion=canvas_principal.bbox("all"))

canvas_principal.bind("<Configure>", lambda event: canvas_principal.itemconfig(canvas_window, width=event.width))  # ajusta el ancho del contenido al ancho del canvas
detail_frame.bind("<Configure>", actualizar_scrollregion)  # actualiza el área desplazable según el contenido

canvas_principal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)  # posiciona el canvas principal
scrollbar_principal.pack(side=tk.RIGHT, fill=tk.Y)  # posiciona el scrollbar principal a la derecha

# Título y notebook ya usan el contenedor desplazable
titulo = tk.Label(detail_frame,text="Sistema de Gestión de Reservas",font=("Arial", 20, "bold"),bg=COLOR_HEADER,fg=COLOR_ACENTO,pady=15)  # crea una etiqueta de texto en la interfaz

titulo.pack(fill=tk.X)  # posiciona el widget en la interfaz

# Notebook para pestañas
notebook = ttk.Notebook(detail_frame)  # asigna un valor a una variable o atributo
notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # posiciona el widget en la interfaz

# ============= PESTAÑA 1: REGISTRO DE CLIENTES =============
frame_clientes = ttk.Frame(notebook)  # asigna un valor a una variable o atributo
notebook.add(frame_clientes, text="📝 Registro de Clientes")  # asigna un valor a una variable o atributo

frame_entrada_clientes = tk.LabelFrame(frame_clientes, text="Registrar nuevo cliente", font=("Arial", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)  # ejecuta la instrucción correspondiente
frame_entrada_clientes.pack(fill=tk.X, padx=10, pady=10)  # posiciona el widget en la interfaz

tk.Label(frame_entrada_clientes, text="Cédula:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(10, 0))  # crea una etiqueta de texto en la interfaz
entrada_cedula = tk.Entry(frame_entrada_clientes,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)  # crea un campo de entrada de texto
entrada_cedula.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz

tk.Label(frame_entrada_clientes, text="Nombre completo:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(0, 0))  # crea una etiqueta de texto en la interfaz
entrada_nombre = tk.Entry(frame_entrada_clientes,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)  # crea un campo de entrada de texto
entrada_nombre.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz

tk.Label(frame_entrada_clientes, text="Correo electrónico:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(0, 0))  # crea una etiqueta de texto en la interfaz
entrada_correo = tk.Entry(frame_entrada_clientes,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)  # crea un campo de entrada de texto
entrada_correo.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz

boton_registrar = tk.Button(frame_entrada_clientes, text="✓ REGISTRAR CLIENTE", command=registrar_cliente, bg=COLOR_BOTON, fg=COLOR_TEXTO, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=10)  # crea un botón interactivo
boton_registrar.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz
boton_registrar.bind("<Enter>", on_enter)  # ejecuta la instrucción correspondiente
boton_registrar.bind("<Leave>", on_leave)  # ejecuta la instrucción correspondiente

frame_tabla_clientes = tk.LabelFrame(frame_clientes, text="Clientes registrados", font=("Arial", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)  # ejecuta la instrucción correspondiente
frame_tabla_clientes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # posiciona el widget en la interfaz

columnas_clientes = ("ID", "Cédula", "Nombre", "Correo")  # asigna un valor a una variable o atributo
tabla_clientes = ttk.Treeview(frame_tabla_clientes, columns=columnas_clientes, height=15)  # ejecuta la instrucción correspondiente
tabla_clientes.column("#0", width=0, stretch=tk.NO)  # ejecuta la instrucción correspondiente
tabla_clientes.column("ID", anchor=tk.CENTER, width=50)  # ejecuta la instrucción correspondiente
tabla_clientes.column("Cédula", anchor=tk.CENTER, width=100)  # ejecuta la instrucción correspondiente
tabla_clientes.column("Nombre", anchor=tk.W, width=200)  # ejecuta la instrucción correspondiente
tabla_clientes.column("Correo", anchor=tk.W, width=250)  # ejecuta la instrucción correspondiente

tabla_clientes.heading("#0", text="", anchor=tk.W)  # ejecuta la instrucción correspondiente
tabla_clientes.heading("ID", text="ID", anchor=tk.CENTER)  # ejecuta la instrucción correspondiente
tabla_clientes.heading("Cédula", text="Cédula", anchor=tk.CENTER)  # ejecuta la instrucción correspondiente
tabla_clientes.heading("Nombre", text="Nombre", anchor=tk.W)  # ejecuta la instrucción correspondiente
tabla_clientes.heading("Correo", text="Correo", anchor=tk.W)  # ejecuta la instrucción correspondiente

scrollbar_clientes = ttk.Scrollbar(frame_tabla_clientes, orient="vertical", command=tabla_clientes.yview)  # crea un scrollbar vertical para la tabla de clientes
tabla_clientes.configure(yscrollcommand=scrollbar_clientes.set)  # conecta la tabla con la barra de desplazamiento

tabla_clientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # posiciona la tabla en el lado izquierdo y expande
tabla_clientes.pack_propagate(False)
scrollbar_clientes.pack(side=tk.RIGHT, fill=tk.Y)  # posiciona la barra de desplazamiento a la derecha




# ============= PESTAÑA 2: GESTIÓN DE RESERVAS =============
frame_reservas = ttk.Frame(notebook)  # asigna un valor a una variable o atributo
notebook.add(frame_reservas, text="🎫 Gestión de Reservas")  # asigna un valor a una variable o atributo

frame_config_servicio = tk.LabelFrame(frame_reservas, text="Configurar servicio", font=("Arial", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)  # ejecuta la instrucción correspondiente
frame_config_servicio.pack(fill=tk.X, padx=10, pady=10)  # posiciona el widget en la interfaz

tk.Label(frame_config_servicio, text="Tipo de servicio:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(10, 0))  # crea una etiqueta de texto en la interfaz
servicio_tipo = tk.StringVar(value="Reserva Sala")  # ejecuta la instrucción correspondiente
combo_tipo = ttk.Combobox(frame_config_servicio, textvariable=servicio_tipo, values=["Reserva Sala", "Alquiler Equipo", "Asesoría Especializada"], state="readonly", width=30)  # crea una lista desplegable
combo_tipo.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz
combo_tipo.bind("<<ComboboxSelected>>", lambda _: actualizar_formulario_servicio())  # ejecuta la instrucción correspondiente

tk.Label(frame_config_servicio, text="Nombre:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10)  # crea una etiqueta de texto en la interfaz
entrada_nombre_servicio = tk.Entry(frame_config_servicio,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)  # crea un campo de entrada de texto
entrada_nombre_servicio.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz
entrada_nombre_servicio.insert(0, "Sala VIP")  # ejecuta la instrucción correspondiente

tk.Label(frame_config_servicio, text="Precio base ($):", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10)  # crea una etiqueta de texto en la interfaz
entrada_precio_servicio = tk.Entry(frame_config_servicio,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)  # crea un campo de entrada de texto
entrada_precio_servicio.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz
entrada_precio_servicio.insert(0, "50000")  # ejecuta la instrucción correspondiente

label_duracion_servicio = tk.Label(frame_config_servicio, text="Duración (horas):", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)  # crea una etiqueta de texto en la interfaz
label_duracion_servicio.pack(anchor=tk.W, padx=10)  # posiciona el widget en la interfaz
entrada_duracion_servicio = tk.Entry(frame_config_servicio,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)  # crea un campo de entrada de texto
entrada_duracion_servicio.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz
entrada_duracion_servicio.insert(0, "1")  # ejecuta la instrucción correspondiente

label_especialista = tk.Label(frame_config_servicio, text="Especialista:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)  # crea una etiqueta de texto en la interfaz
entrada_especialista = tk.Entry(frame_config_servicio,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)  # crea un campo de entrada de texto
entrada_especialista.insert(0, "Carlos")  # ejecuta la instrucción correspondiente

boton_crear_servicio = tk.Button(frame_config_servicio, text="✅ Crear servicio activo", command=crear_servicio, bg=COLOR_EXITO, fg=COLOR_TEXTO, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=10)  # crea un botón interactivo
boton_crear_servicio.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz
boton_crear_servicio.bind("<Enter>", on_enter)  # ejecuta la instrucción correspondiente
boton_crear_servicio.bind("<Leave>", on_leave)  # ejecuta la instrucción correspondiente

frame_nueva_reserva = tk.LabelFrame(frame_reservas, text="Crear nueva reserva", font=("Arial", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)  # ejecuta la instrucción correspondiente
frame_nueva_reserva.pack(fill=tk.X, padx=10, pady=10)  # posiciona el widget en la interfaz

tk.Label(frame_nueva_reserva, text="Seleccionar cliente:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(10, 0))  # crea una etiqueta de texto en la interfaz
combo_clientes = ttk.Combobox(frame_nueva_reserva, state="readonly", width=40)  # crea una lista desplegable
combo_clientes.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz

boton_reserva = tk.Button(frame_nueva_reserva, text="🎫 REALIZAR RESERVA", command=hacer_reserva, bg=COLOR_SECUNDARIO, fg=COLOR_TEXTO, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=10)  # crea un botón interactivo
boton_reserva.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz
boton_reserva.bind("<Enter>", on_enter)  # ejecuta la instrucción correspondiente
boton_reserva.bind("<Leave>", on_leave)  # ejecuta la instrucción correspondiente

frame_tabla_reservas = tk.LabelFrame(frame_reservas, text="Reservas confirmadas", font=("Arial", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)  # ejecuta la instrucción correspondiente
frame_tabla_reservas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # posiciona el widget en la interfaz

columnas_reservas = ("#", "Cédula", "Cliente", "Servicio", "Duración", "Costo Total", "Estado")  # asigna un valor a una variable o atributo
tabla_reservas = ttk.Treeview(frame_tabla_reservas, columns=columnas_reservas, height=12)  # ejecuta la instrucción correspondiente
tabla_reservas.column("#0", width=0, stretch=tk.NO)  # ejecuta la instrucción correspondiente
tabla_reservas.column("#", anchor=tk.CENTER, width=40)  # ejecuta la instrucción correspondiente
tabla_reservas.column("Cédula", anchor=tk.CENTER, width=90)  # ejecuta la instrucción correspondiente
tabla_reservas.column("Cliente", anchor=tk.W, width=120)  # ejecuta la instrucción correspondiente
tabla_reservas.column("Servicio", anchor=tk.W, width=120)  # ejecuta la instrucción correspondiente
tabla_reservas.column("Duración", anchor=tk.CENTER, width=80)  # ejecuta la instrucción correspondiente
tabla_reservas.column("Costo Total", anchor=tk.CENTER, width=100)  # ejecuta la instrucción correspondiente
tabla_reservas.column("Estado", anchor=tk.CENTER, width=90)  # ejecuta la instrucción correspondiente

tabla_reservas.heading("#0", text="", anchor=tk.W)  # ejecuta la instrucción correspondiente
tabla_reservas.heading("#", text="#", anchor=tk.CENTER)  # ejecuta la instrucción correspondiente
tabla_reservas.heading("Cédula", text="Cédula", anchor=tk.CENTER)  # ejecuta la instrucción correspondiente
tabla_reservas.heading("Cliente", text="Cliente", anchor=tk.W)  # ejecuta la instrucción correspondiente
tabla_reservas.heading("Servicio", text="Servicio", anchor=tk.W)  # ejecuta la instrucción correspondiente
tabla_reservas.heading("Duración", text="Duración", anchor=tk.CENTER)  # ejecuta la instrucción correspondiente
tabla_reservas.heading("Costo Total", text="Costo Total", anchor=tk.CENTER)  # ejecuta la instrucción correspondiente
tabla_reservas.heading("Estado", text="Estado", anchor=tk.CENTER)  # ejecuta la instrucción correspondiente

scrollbar_reservas = ttk.Scrollbar(frame_tabla_reservas, orient="vertical", command=tabla_reservas.yview)  # crea un scrollbar vertical para la tabla de reservas
tabla_reservas.configure(yscrollcommand=scrollbar_reservas.set)  # conecta la tabla con la barra de desplazamiento

tabla_reservas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # posiciona la tabla en el lado izquierdo y expande
tabla_reservas.pack_propagate(False)
scrollbar_reservas.pack(side=tk.RIGHT, fill=tk.Y)  # posiciona la barra de desplazamiento a la derecha

frame_botones_reservas = tk.Frame(frame_reservas, bg=COLOR_FONDO)  # ejecuta la instrucción correspondiente
frame_botones_reservas.pack(fill=tk.X, padx=10, pady=10)  # posiciona el widget en la interfaz

boton_editar = tk.Button(frame_botones_reservas, text="✏️ Editar", command=editar_reserva_seleccionada, bg="#ffc107", fg="#000", font=("Arial", 10, "bold"), relief=tk.FLAT, padx=15, pady=8)  # crea un botón interactivo
boton_editar.pack(side=tk.LEFT, padx=5)  # posiciona el widget en la interfaz
boton_editar.bind("<Enter>", on_enter)  # ejecuta la instrucción correspondiente
boton_editar.bind("<Leave>", on_leave)  # ejecuta la instrucción correspondiente

boton_eliminar = tk.Button(frame_botones_reservas, text="🗑️ Eliminar", command=eliminar_reserva_seleccionada, bg=COLOR_ERROR, fg=COLOR_TEXTO, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=15, pady=8)  # crea un botón interactivo
boton_eliminar.pack(side=tk.LEFT, padx=5)  # posiciona el widget en la interfaz
boton_eliminar.bind("<Enter>", on_enter)  # ejecuta la instrucción correspondiente
boton_eliminar.bind("<Leave>", on_leave)  # ejecuta la instrucción correspondiente

# ============= PESTAÑA 3: BÚSQUEDA =============
frame_busqueda = ttk.Frame(notebook)  # asigna un valor a una variable o atributo
notebook.add(frame_busqueda, text="🔍 Búsqueda de Clientes")  # asigna un valor a una variable o atributo

frame_busqueda_clientes = tk.LabelFrame(frame_busqueda, text="Buscar cliente por cédula", font=("Arial", 12, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO)  # ejecuta la instrucción correspondiente
frame_busqueda_clientes.pack(fill=tk.X, padx=10, pady=10)  # posiciona el widget en la interfaz

tk.Label(frame_busqueda_clientes, text="Ingresa la cédula:", font=("Arial", 10, "bold"), bg=COLOR_CARD, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(10, 0))  # crea una etiqueta de texto en la interfaz
entrada_busqueda_cedula = tk.Entry(frame_busqueda_clientes,font=("Arial", 10),width=40,relief=tk.FLAT,bd=2,bg=COLOR_INPUT,fg=COLOR_TEXTO,insertbackground=COLOR_TEXTO)  # crea un campo de entrada de texto
entrada_busqueda_cedula.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz

boton_buscar = tk.Button(frame_busqueda_clientes, text="🔍 BUSCAR", command=buscar_cliente_por_cedula, bg=COLOR_BOTON, fg=COLOR_TEXTO, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=20, pady=10)  # crea un botón interactivo
boton_buscar.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el widget en la interfaz
boton_buscar.bind("<Enter>", on_enter)  # ejecuta la instrucción correspondiente
boton_buscar.bind("<Leave>", on_leave)  # ejecuta la instrucción correspondiente




# ============= PESTAÑA 4: COMENTARIOS =============

frame_comentarios = tk.Frame(notebook, bg=COLOR_FONDO)  # ejecuta la instrucción correspondiente

notebook.add(  # ejecuta la instrucción correspondiente
    frame_comentarios,  # ejecuta la instrucción correspondiente
    text="💬 Comentarios"  # asigna un valor a una variable o atributo
)  # ejecuta la instrucción correspondiente

tk.Label(  # crea una etiqueta de texto en la interfaz
    frame_comentarios,  # ejecuta la instrucción correspondiente
    text="Seleccionar cliente:",  # asigna un valor a una variable o atributo
    font=("Arial", 10, "bold"),  # asigna un valor a una variable o atributo
    bg=COLOR_CARD,  # asigna un valor a una variable o atributo
    fg=COLOR_TEXTO  # asigna un valor a una variable o atributo
).pack(anchor=tk.W, padx=10, pady=(10, 0))  # posiciona el widget en la interfaz

combo_clientes_comentario = ttk.Combobox(  # crea una lista desplegable
    frame_comentarios,  # ejecuta la instrucción correspondiente
    state="readonly",  # asigna un valor a una variable o atributo
    width=40  # asigna un valor a una variable o atributo
)  # ejecuta la instrucción correspondiente

combo_clientes_comentario.pack(  # posiciona el widget en la interfaz
    fill=tk.X,  # asigna un valor a una variable o atributo
    padx=10,  # asigna un valor a una variable o atributo
    pady=(0, 10)  # asigna un valor a una variable o atributo
)  # ejecuta la instrucción correspondiente

tk.Label(  # crea una etiqueta de texto en la interfaz
    frame_comentarios,  # ejecuta la instrucción correspondiente
    text="Comentario:",  # asigna un valor a una variable o atributo
    font=("Arial", 10, "bold"),  # asigna un valor a una variable o atributo
    bg=COLOR_CARD,  # asigna un valor a una variable o atributo
    fg=COLOR_TEXTO  # asigna un valor a una variable o atributo
).pack(anchor=tk.W, padx=10)  # posiciona el widget en la interfaz

frame_caja_comentario = tk.Frame(frame_comentarios, bg=COLOR_CARD)  # crea un contenedor para el texto y su scrollbar
frame_caja_comentario.pack(fill=tk.X, padx=10, pady=(0, 10))  # posiciona el contenedor en la interfaz

caja_comentario = tk.Text(  # asigna un valor a una variable o atributo
    frame_caja_comentario,  # ejecuta la instrucción correspondiente
    height=5,  # asigna un valor a una variable o atributo
    font=("Arial", 10),  # asigna un valor a una variable o atributo
    bg=COLOR_INPUT,  # asigna un valor a una variable o atributo
    fg=COLOR_TEXTO,  # asigna un valor a una variable o atributo
    insertbackground=COLOR_TEXTO,  # asigna un valor a una variable o atributo
    relief=tk.FLAT,  # asigna un valor a una variable o atributo
    bd=2,  # asigna un valor a una variable o atributo
    wrap=tk.WORD  # evita el corte abrupto de palabras
)  # ejecuta la instrucción correspondiente

scrollbar_comentario = ttk.Scrollbar(frame_caja_comentario, orient="vertical", command=caja_comentario.yview)  # crea un scrollbar vertical para la caja de texto
caja_comentario.configure(yscrollcommand=scrollbar_comentario.set)  # conecta la caja de texto con la barra de desplazamiento

caja_comentario.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # posiciona el cuadro de texto dentro del contenedor
scrollbar_comentario.pack(side=tk.RIGHT, fill=tk.Y)  # posiciona la barra de desplazamiento a la derecha

boton_comentario = tk.Button(  # crea un botón interactivo
    frame_comentarios,  # ejecuta la instrucción correspondiente
    text="💬 Guardar comentario",  # asigna un valor a una variable o atributo
    command=agregar_comentario,  # asigna un valor a una variable o atributo
    bg=COLOR_BOTON,  # asigna un valor a una variable o atributo
    fg=COLOR_TEXTO,  # asigna un valor a una variable o atributo
    font=("Arial", 10, "bold"),  # asigna un valor a una variable o atributo
    relief=tk.FLAT,  # asigna un valor a una variable o atributo
    padx=20,  # asigna un valor a una variable o atributo
    pady=10  # asigna un valor a una variable o atributo
)  # ejecuta la instrucción correspondiente

boton_comentario.pack(  # posiciona el widget en la interfaz
    padx=10,  # asigna un valor a una variable o atributo
    pady=(0, 10)  # asigna un valor a una variable o atributo
)  # ejecuta la instrucción correspondiente

boton_comentario.bind("<Enter>", on_enter)  # ejecuta la instrucción correspondiente
boton_comentario.bind("<Leave>", on_leave)  # ejecuta la instrucción correspondiente

frame_lista_comentarios = tk.Frame(frame_comentarios, bg=COLOR_CARD)  # crea un contenedor para la lista de comentarios y su scrollbar
frame_lista_comentarios.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # posiciona el contenedor en la interfaz

lista_comentarios = tk.Listbox(  # asigna un valor a una variable o atributo
    frame_lista_comentarios,  # ejecuta la instrucción correspondiente
    font=("Arial", 10),  # asigna un valor a una variable o atributo
    height=10,  # asigna un valor a una variable o atributo
    bg=COLOR_INPUT,  # asigna un valor a una variable o atributo
    fg=COLOR_TEXTO,  # asigna un valor a una variable o atributo
    relief=tk.FLAT,  # asigna un valor a una variable o atributo
    bd=2  # asigna un valor a una variable o atributo
)  # ejecuta la instrucción correspondiente

scrollbar_lista_comentarios = ttk.Scrollbar(frame_lista_comentarios, orient="vertical", command=lista_comentarios.yview)  # crea el scrollbar vertical de la lista de comentarios
lista_comentarios.configure(yscrollcommand=scrollbar_lista_comentarios.set)  # conecta la lista de comentarios con la barra de desplazamiento

lista_comentarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # posiciona la lista dentro del contenedor
scrollbar_lista_comentarios.pack(side=tk.RIGHT, fill=tk.Y)  # posiciona la barra de desplazamiento a la derecha



# ============= INFORMACIÓN DEL SERVICIO ACTIVO =============
frame_servicio = tk.Frame(ventana,bg=COLOR_HEADER,relief=tk.FLAT,bd=1)  # ejecuta la instrucción correspondiente
frame_servicio.pack(fill=tk.X, padx=5, pady=5)  # posiciona el widget en la interfaz

info_servicio = tk.Label(frame_servicio,text="",font=("Arial", 9),bg=COLOR_HEADER,fg=COLOR_ACENTO)  # crea una etiqueta de texto en la interfaz
info_servicio.pack(padx=10, pady=10)  # posiciona el widget en la interfaz

actualizar_formulario_servicio()  # ejecuta la instrucción correspondiente
actualizar_info_servicio()  # ejecuta la instrucción correspondiente

# Inicia el bucle principal
ventana.mainloop()  # ejecuta la instrucción correspondiente
