# Sistema-de-Gestion-para-una-tienda-de-juegos-Oline-

# GameStoreLite - Sistema de Gestión para una Tienda de Videojuegos

Este proyecto es un sistema básico de gestión para una tienda de videojuegos, desarrollado en Python con la biblioteca tkinter para la interfaz de usuario y mysql.connector para la conexión a una base de datos MySQL.

El sistema permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en las siguientes entidades:

**Desarrolladores:** Gestión de información sobre los estudios desarrolladores de videojuegos.  
**Géneros:** Organización de videojuegos por géneros (acción, aventura, RPG, etc.).  
**Plataformas:** Control de consolas y plataformas disponibles (PlayStation, Xbox, Nintendo, PC).  
**Videojuegos:** Registro y control del inventario de videojuegos.  
**Clientes:** Almacenamiento de los datos de los clientes de la tienda.  
**Ventas:** Registro de transacciones de venta, con lógica de negocio para la gestión de stock.

## Contenido del Repositorio

**DB gamestore.sql:** Archivo SQL con el esquema de la base de datos (CREATE TABLE).  
**Store Pro gamestore.sql:** Archivo SQL con los procedimientos almacenados (CREATE PROCEDURE) utilizados para realizar las operaciones de la aplicación.  
**GameStoreLite.py:** El script principal de Python que ejecuta la interfaz gráfica y se conecta a la base de datos para interactuar con ella.

## Requisitos

Para poder ejecutar este proyecto, necesitas tener instalados los siguientes componentes:

**Python 3.x:** El lenguaje de programación.  
**MySQL Server:** El sistema de gestión de bases de datos. Se debe INICIAR XAMPP PARA ESTABLECER CONEXIÓN.  
**Bibliotecas de Python:**
- **tkinter:** Generalmente viene incluido en la instalación de Python.
- **mysql-connector-python:** Para conectar Python con MySQL. Puedes instalarlo usando pip:
  ```
  pip install mysql-connector-python
  ```

## Configuración y Uso

### Configuración de la Base de Datos:

1. Asegúrate de que tu servidor MySQL esté en ejecución.
2. Importa el archivo `DB gamestore.sql` en tu servidor MySQL para crear la base de datos y las tablas necesarias.
3. Importa el archivo `Store Pro gamestore.sql` para crear todos los procedimientos almacenados.
4. Verifica que los datos de conexión en el archivo `GameStoreLite.py` coincidan con la configuración de tu base de datos local (host, user, password, database).

### Ejecutar la Aplicación:

1. Abre una terminal o línea de comandos.
2. Navega al directorio donde se encuentra el archivo `GameStoreLite.py`.
3. Ejecuta el script de Python:
   ```
   python "GameStoreLite.py"
   ```
4. Ahora puedes empezar a usar la aplicación para gestionar desarrolladores, géneros, plataformas, videojuegos, clientes y ventas de tu tienda de videojuegos.

## Procedimientos Almacenados Destacados

El sistema utiliza procedimientos almacenados para garantizar la integridad y el control de las operaciones, especialmente en el módulo de ventas. El procedimiento `RegistrarVenta` incluye la siguiente lógica de negocio:

- Calcula el total de la venta automáticamente.
- Verifica el stock del videojuego antes de registrar la venta.
- Si hay suficiente stock, registra la venta y disminuye la cantidad del videojuego en el inventario.
- Si el stock es insuficiente, muestra un mensaje de error.

## Licencia de Uso

Este proyecto se distribuye bajo licencia MIT, permitiendo su uso tanto personal como comercial. Se autoriza la modificación y distribución del código, sin garantías incluidas. Se requiere atribución al autor original en redistribuciones.
---

**Nota:** Este sistema fue desarrollado con fines educativos y puede ser adaptado según las necesidades específicas de cada tienda de videojuegos.
