# Software FJ

Sistema orientado a objetos para la gestión de clientes, servicios y reservas.

## Arquitectura
- Clase abstracta `Entidad` como base general de entidades del sistema.
- Clase `Cliente` con encapsulación y validación rigurosa.
- Clase abstracta `Servicio` y tres servicios especializados:
  - `ReservaSala`
  - `AlquilerEquipo`
  - `AsesoriaEspecializada`
- Clase `Reserva` con confirmación, cancelación, validación y procesamiento.
- Excepciones personalizadas para datos inválidos y operaciones no permitidas.
- Registro de eventos y errores en el archivo `sistema.log`.

## Archivos principales
- `entidad.py`: clase abstracta base para entidades.
- `cliente.py`: clase `Cliente` con validación y encapsulación.
- `servicio.py`: abstracción de servicios y servicios concretos.
- `reserva.py`: lógica de reservas con manejo de estados.
- `excepciones.py`: excepciones personalizadas.
- `logger_config.py`: configuración de logging del sistema.
- `interfaz.py`: interfaz gráfica de usuario para la gestión.
- `main.py`: demostración de operaciones válidas e inválidas.

## Ejecución
Ejecutar la demostración de consola:

```bash
python main.py
```

Ejecutar la interfaz gráfica:

```bash
python interfaz.py
```

## Funcionalidades
- Registro y validación de clientes.
- Creación y validación de servicios.
- Reserva de servicios con confirmación y cancelación.
- Manejo de múltiples escenarios con excepciones controladas.
- Continuidad del programa ante errores.
- Registro de eventos y errores en el archivo `sistema.log`.
