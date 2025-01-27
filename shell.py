import shutil
import os
import stat
import subprocess
import json  # Para almacenar los datos en formato JSON
import datetime
import socket
sistema_error_log = "/var/log/shell/sistema_error.log"

def registrar_error(mensaje):
    if not os.path.exists("/var/log/shell"):
        os.makedirs("/var/log/shell", exist_ok=True)
    if not os.path.isfile(sistema_error_log):
        open(sistema_error_log, "w").close()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(sistema_error_log, "a") as log:
        log.write(f"{timestamp} - ERROR: {mensaje}\n")

def obtener_ip_local():
    """
    Obtiene la dirección IP local del equipo que ejecuta la shell.

    Intentamos obtener el nombre del host y, a partir de él, resolvemos
    la dirección IP asociada. En caso de que falle, se devuelve "desconocida".

    Retorna:
        - Una cadena con la IP local del equipo.
    """
    try:
        # Obtener el nombre del host actual.
        hostname = socket.gethostname()
        # Resolver la IP a partir del nombre del host.
        ip_local = socket.gethostbyname(hostname)
        return ip_local
    except Exception as e:
        # En caso de error, registramos el fallo y devolvemos "desconocida".
        print(f"Error al obtener la IP local: {e}")
        registrar_error("Error al obtener la IP local: " + str(e))
        return "desconocida"

# Variable global para almacenar el directorio actual
directorio_actual = os.getcwd()
def copiar_archivo(origen_carpeta, archivo_nombre, destino_carpeta):
    """
    Copia un archivo de una carpeta origen a una carpeta destino.

    Parámetros:
        - origen_carpeta: Ruta de la carpeta origen donde se encuentra el archivo.
        - archivo_nombre: Nombre del archivo a copiar.
        - destino_carpeta: Ruta de la carpeta destino donde se copiará el archivo.
    """
    try:
        # Construimos las rutas completas para origen y destino.
        origen = os.path.join(origen_carpeta, archivo_nombre)
        destino = os.path.join(destino_carpeta, archivo_nombre)
        
        # Verificamos que el archivo existe en la carpeta origen.
        if not os.path.isfile(origen):
            print(f"El archivo '{archivo_nombre}' no existe en la carpeta de origen '{origen_carpeta}'.")
            return
        
        # Si la carpeta destino no existe, la creamos.
        if not os.path.exists(destino_carpeta):
            os.makedirs(destino_carpeta)
        
        # Realizamos la copia del archivo.
        shutil.copy(origen, destino)
        print(f"Archivo '{archivo_nombre}' copiado de '{origen_carpeta}' a '{destino_carpeta}' exitosamente.")
    
    except Exception as e:
        # En caso de error, lo registramos.
        print(f"Error al copiar el archivo: {e}")
        registrar_error()
            
def verificar_archivos_necesarios():
    if not os.path.exists("usuarios.json"):
        print("Creando archivo usuarios.json...")
        with open("usuarios.json", "w") as archivo:
            json.dump({}, archivo)

verificar_archivos_necesarios()
def mover_archivo(origen_carpeta, archivo_nombre, destino_carpeta):
    """
    Mueve un archivo de una carpeta origen a una carpeta destino.

    Parámetros:
        - origen_carpeta: Ruta de la carpeta origen.
        - archivo_nombre: Nombre del archivo a mover.
        - destino_carpeta: Ruta de la carpeta destino.
    """
    try:
        # Construimos las rutas completas para origen y destino.
        origen = os.path.join(origen_carpeta, archivo_nombre)
        destino = os.path.join(destino_carpeta, archivo_nombre)
        
        # Verificamos que el archivo existe en la carpeta origen.
        if not os.path.isfile(origen):
            print(f"El archivo '{archivo_nombre}' no existe en la carpeta de origen '{origen_carpeta}'.")
            return
        
        # Si la carpeta destino no existe, la creamos.
        if not os.path.exists(destino_carpeta):
            os.makedirs(destino_carpeta)
        
        # Movemos el archivo a la carpeta destino.
        shutil.move(origen, destino)
        print(f"Archivo '{archivo_nombre}' movido de '{origen_carpeta}' a '{destino_carpeta}' exitosamente.")
    
    except Exception as e:
        # En caso de error, lo registramos.
        print(f"Error al mover el archivo: {e}")
        registrar_error()

def renombrar_archivo(origen_carpeta, archivo_nombre, nuevo_nombre):
    """
    Renombra un archivo dentro de una misma carpeta.

    Parámetros:
        - origen_carpeta: Ruta de la carpeta donde está el archivo.
        - archivo_nombre: Nombre actual del archivo.
        - nuevo_nombre: Nuevo nombre que se le asignará al archivo.
    """
    try:
        # Construimos las rutas completas para el archivo y su nuevo nombre.
        origen = os.path.join(origen_carpeta, archivo_nombre)
        destino = os.path.join(origen_carpeta, nuevo_nombre)
        
        # Verificamos que el archivo existe.
        if not os.path.isfile(origen):
            print(f"El archivo '{archivo_nombre}' no existe en la carpeta '{origen_carpeta}'.")
            return
        
        # Renombramos el archivo.
        os.rename(origen, destino)
        print(f"Archivo '{archivo_nombre}' renombrado a '{nuevo_nombre}' exitosamente en '{origen_carpeta}'.")
    
    except Exception as e:
        # En caso de error, lo registramos.
        print(f"Error al renombrar el archivo: {e}")
        registrar_error()

def listar_contenido(carpeta):
    """
    Lista los archivos y carpetas dentro de un directorio.

    Parámetros:
        - carpeta: Ruta de la carpeta que se desea listar.
    """
    try:
        # Verificamos que la carpeta existe.
        if not os.path.exists(carpeta):
            print(f"La carpeta '{carpeta}' no existe.")
            return
        
        # Obtenemos el contenido de la carpeta.
        contenido = os.listdir(carpeta)
        
        # Si la carpeta está vacía, lo indicamos.
        if not contenido:
            print(f"La carpeta '{carpeta}' está vacía.")
            return
        
        # Listamos cada elemento en la carpeta.
        print(f"Contenido de la carpeta '{carpeta}':")
        for item in contenido:
            ruta_item = os.path.join(carpeta, item)
            if os.path.isdir(ruta_item):
                print(f"  [D] {item}/")  # Directorio.
            else:
                print(f"  [F] {item}")  # Archivo.
    
    except Exception as e:
        # En caso de error, lo registramos.
        print(f"Error al listar el contenido de la carpeta: {e}")
        registrar_error()

import subprocess

def crear_usuario_sistema(nombre_usuario, contrasena=None):
    """
    Crea un usuario en el sistema operativo.
    
    :param nombre_usuario: Nombre del usuario que se va a crear.
    :param contrasena: Contraseña del usuario (opcional).
    """
    try:
        # Comando para agregar el usuario
        comando_crear = f"useradd {nombre_usuario}"
        resultado = subprocess.run(comando_crear, shell=True, check=True, capture_output=True, text=True)
        print(f"Usuario '{nombre_usuario}' creado en el sistema operativo.")

        # Si se proporciona una contraseña, establecerla
        if contrasena:
            comando_contrasena = f"echo '{nombre_usuario}:{contrasena}' | chpasswd"
            subprocess.run(comando_contrasena, shell=True, check=True, capture_output=True, text=True)
            print(f"Contraseña configurada para el usuario '{nombre_usuario}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error al crear el usuario '{nombre_usuario}': {e.stderr}")
        registrar_error(f"Error al crear el usuario '{nombre_usuario}': {e.stderr}")
    except Exception as e:
        print(f"Error inesperado al crear el usuario '{nombre_usuario}': {e}")
        registrar_error(f"Error inesperado al crear el usuario '{nombre_usuario}': {e}")

    if verificar_usuario_existe(nombre_usuario):
    print(f"El usuario '{nombre_usuario}' ya existe en el sistema operativo.")
    return




def crear_directorio(ruta_carpeta):
    """
    Crea un nuevo directorio en la ruta especificada.

    Parámetros:
        - ruta_carpeta: Ruta completa donde se creará el directorio.
    """
    try:
        # Verificamos si la carpeta ya existe.
        if os.path.exists(ruta_carpeta):
            print(f"La carpeta '{ruta_carpeta}' ya existe.")
        else:
            # Creamos la carpeta.
            os.makedirs(ruta_carpeta)
            print(f"Carpeta '{ruta_carpeta}' creada exitosamente.")
    
    except Exception as e:
        # En caso de error, lo registramos.
        print(f"Error al crear la carpeta: {e}")
        registrar_error()


def cambiar_directorio(nuevo_directorio):
    """
    Cambia el directorio actual de trabajo al especificado tanto en la shell como en el sistema operativo.

    :param nuevo_directorio: Ruta del directorio al que se desea cambiar.
    """
    global directorio_actual
    try:
        # Verificar si el directorio existe
        if os.path.isdir(nuevo_directorio):
            # Cambiar el directorio en el sistema operativo
            os.chdir(nuevo_directorio)
            # Actualizar la variable global del directorio actual
            directorio_actual = os.getcwd()
            print(f"Directorio cambiado a: {directorio_actual}")
        else:
            print(f"El directorio '{nuevo_directorio}' no existe.")
    except Exception as e:
        # Manejar cualquier error durante el cambio de directorio
        print(f"Error al cambiar de directorio: {e}")
        registrar_error(f"Error al cambiar de directorio: {e}")



def cambiar_permisos(ruta_archivo, permisos):
    """
    Cambia los permisos de un archivo o directorio según el valor especificado.

    Parámetros:
        - ruta_archivo: Ruta completa del archivo o directorio al que se desea cambiar permisos.
        - permisos: Permisos en formato octal, por ejemplo, 777 o 755.
    """
    try:
        # Convertimos los permisos de cadena a formato numérico octal.
        permisos_octal = int(permisos, 8)
        
        # Verificamos si la ruta es un archivo válido.
        if os.path.isfile(ruta_archivo):
            # Cambiamos los permisos del archivo.
            os.chmod(ruta_archivo, permisos_octal)
            print(f"Permisos de '{ruta_archivo}' cambiados a {permisos}.")
        elif os.path.isdir(ruta_archivo):
            # Si es un directorio, mostramos un mensaje indicando que no se puede aplicar directamente.
            print(f"'{ruta_archivo}' es un directorio. Usa permisos individualmente para los archivos dentro.")
        else:
            # Si la ruta no existe, mostramos un mensaje de error.
            print(f"El archivo o directorio '{ruta_archivo}' no existe.")
    
    except ValueError:
        # En caso de formato de permisos inválido, mostramos un error específico.
        print("Formato de permisos inválido. Asegúrate de usar un valor numérico como '777' o '755'.")
    except Exception as e:
        # Capturamos cualquier otro error y lo registramos.
        print(f"Error al cambiar permisos: {e}")
        registrar_error()

def cambiar_propietario(ruta, uid, gid):
    """
    Cambia el propietario (usuario y grupo) de un archivo o directorio.

    Parámetros:
        - ruta: Ruta completa del archivo o directorio cuyo propietario se desea cambiar.
        - uid: Nuevo ID de usuario (User ID).
        - gid: Nuevo ID de grupo (Group ID).
    """
    try:
        # Verificamos si el archivo o directorio existe.
        if not os.path.exists(ruta):
            print(f"El archivo o directorio '{ruta}' no existe.")
            return
        
        # Cambiamos el propietario del archivo o directorio.
        os.chown(ruta, uid, gid)
        print(f"Propietario de '{ruta}' cambiado a UID:{uid} y GID:{gid} exitosamente.")
    
    except PermissionError:
        # Si no se tienen los permisos necesarios, mostramos un mensaje claro.
        print("Permiso denegado. Necesitas privilegios de superusuario (sudo).")
        registrar_error()
    except Exception as e:
        # Capturamos cualquier otro error y lo registramos.
        print(f"Error al cambiar el propietario: {e}")
        registrar_error()

def propietario_comando(argumentos):
    """
    Procesa el comando 'propietario' para cambiar el propietario de un archivo o directorio.

    Este comando se invoca desde la shell personalizada.

    Parámetros:
        - argumentos: Lista de argumentos que incluye:
            - Ruta del archivo o directorio.
            - Nuevo UID (User ID).
            - Nuevo GID (Group ID).
    """
    # Verificamos que los argumentos sean los correctos.
    if len(argumentos) != 3:
        print("Uso: propietario <archivo/ruta> <UID> <GID>")
        return

    ruta = argumentos[0]
    try:
        # Convertimos UID y GID a enteros antes de pasarlos a la función.
        uid = int(argumentos[1])
        gid = int(argumentos[2])
        # Llamamos a la función para cambiar propietario.
        cambiar_propietario(ruta, uid, gid)
    except ValueError:
        # Mostramos un mensaje de error si los valores de UID o GID no son válidos.
        print("El UID y GID deben ser números enteros.")
        registrar_error()

        

def cambiar_password(usuario, nueva_password):
    """
    Cambia la contraseña de un usuario del sistema operativo.

    :param usuario: Nombre del usuario del sistema operativo.
    :param nueva_password: Nueva contraseña a asignar al usuario.
    """
    try:
        # Comando para cambiar la contraseña usando `passwd`
        comando = f"echo '{usuario}:{nueva_password}' | sudo chpasswd"
        subprocess.run(comando, shell=True, check=True)
        print(f"Contraseña de '{usuario}' cambiada exitosamente.")
    except subprocess.CalledProcessError:
        print("Error al cambiar la contraseña. Asegúrate de tener privilegios de superusuario.")
        registrar_error(f"Error al cambiar contraseña para usuario '{usuario}'.")
    except Exception as e:
        print(f"Error al cambiar la contraseña: {e}")
        registrar_error(f"Error inesperado al cambiar contraseña: {e}")
    


# Almacenamiento de usuarios en un archivo JSON
usuarios_file = "usuarios.json"

def cargar_usuarios():
    try:
        # Si no existe el archivo, inicializarlo
        if not os.path.exists("usuarios.json"):
            with open("usuarios.json", "w") as archivo:
                json.dump({}, archivo)
        
        # Intentar cargar el archivo JSON
        with open("usuarios.json", "r") as archivo:
            usuarios = json.load(archivo)
        
        # Verificar que el contenido sea un diccionario
        if not isinstance(usuarios, dict):
            raise ValueError("El archivo usuarios.json no es un diccionario válido.")
        
        return usuarios
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error al cargar usuarios: {e}")
        registrar_error(f"Error al cargar usuarios: {e}")

        # Reparar el archivo con un diccionario vacío
        usuarios = {}
        with open("usuarios.json", "w") as archivo:
            json.dump(usuarios, archivo)
        return usuarios

    except (json.JSONDecodeError, ValueError) as e:
        # Manejar errores de formato o contenido inválido
        print(f"Error al cargar usuarios: {e}")
        registrar_error(f"Error al cargar usuarios: {e}")

        # Reparar el archivo con un diccionario vacío
        usuarios = {}
        guardar_usuarios()  # Sobrescribir con un diccionario vacío
        return usuarios





def guardar_usuarios(usuarios):
    """Guarda los usuarios en un archivo JSON."""
    with open(usuarios_file, "w") as file:
        json.dump(usuarios, file, indent=4)

def agregar_usuario():
    """Registrar un nuevo usuario o actualizar uno existente."""
    nombre = input("Ingrese el nombre del usuario: ").strip()
    contrasena = input("Ingrese la contraseña para el usuario: ").strip()
    
    if nombre in usuarios:
        print(f"El usuario '{nombre}' ya existe en el archivo. ¿Desea actualizar sus datos? (s/n)")
        respuesta = input().strip().lower()
        if respuesta != 's':
            print("Operación cancelada.")
            return
    else:
        print(f"Registrando nuevo usuario: {nombre}.")

    # Solicitar datos adicionales
    horario_trabajo = input("Ingrese el horario de trabajo (ejemplo: 9:00 - 17:00): ").strip()
    lugares_conexion = input("Ingrese los lugares de conexión (IPs o localhost, separados por comas): ").split(',')

    # Crear el usuario en el sistema operativo
    crear_usuario_sistema(nombre, contrasena)

    # Guardar los datos del usuario en el archivo JSON
    usuarios[nombre] = {
        "horario_trabajo": horario_trabajo,
        "lugares_conexion": [ip.strip() for ip in lugares_conexion]
    }
    guardar_usuarios()
    print(f"Los datos de '{nombre}' han sido registrados exitosamente.")

def verificar_usuario_existe(nombre_usuario):
    """
    Verifica si un usuario ya existe en el sistema operativo.
    
    :param nombre_usuario: Nombre del usuario.
    :return: True si el usuario existe, False en caso contrario.
    """
    try:
        resultado = subprocess.run(f"id -u {nombre_usuario}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return resultado.returncode == 0  # Código de retorno 0 significa que el usuario existe
    except Exception as e:
        print(f"Error al verificar si el usuario existe: {e}")
        registrar_error(f"Error al verificar si el usuario '{nombre_usuario}' existe: {e}")
        return False


def mostrar_usuarios():
    """Muestra los datos de todos los usuarios."""
    usuarios = cargar_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    for nombre, datos in usuarios.items():
        print(f"\nUsuario: {nombre}")
        print(f"Correo: {datos['correo']}")
        print(f"Horario de Trabajo: {datos['horario_trabajo']}")
        print(f"Lugares de Conexión: {', '.join(datos['lugares_conexion'])}")

def actualizar_usuario():
    """Actualiza los datos de un usuario existente."""
    nombre = input("Ingrese el nombre del usuario a actualizar: ")
    usuarios = cargar_usuarios()

    if nombre not in usuarios:
        print(f"El usuario '{nombre}' no existe.")
        return

    print(f"Actualizando los datos del usuario '{nombre}':")
    correo = input(f"Nuevo correo (actual: {usuarios[nombre]['correo']}): ")
    horario_trabajo = input(f"Nuevo horario de trabajo (actual: {usuarios[nombre]['horario_trabajo']}): ")
    lugares_conexion = input(f"Nuevos lugares de conexión (actual: {', '.join(usuarios[nombre]['lugares_conexion'])}): ").split(',')

    usuarios[nombre] = {
        "nombre": nombre,
        "correo": correo,
        "horario_trabajo": horario_trabajo,
        "lugares_conexion": [ip.strip() for ip in lugares_conexion]
    }
    guardar_usuarios(usuarios)
    print(f"Datos del usuario '{nombre}' actualizados exitosamente.")


usuarios = {}

def cargar_usuarios():
    """Cargar los usuarios desde un archivo JSON."""
    global usuarios
    try:
        if not os.path.exists("usuarios.json"):
            # Crear un archivo JSON vacío si no existe
            with open("usuarios.json", "w") as archivo:
                json.dump({}, archivo)  # Guardar un diccionario vacío
        with open("usuarios.json", "r") as archivo:
            usuarios = json.load(archivo)
    except Exception as e:
        usuarios = {}
        registrar_error(f"Error al cargar usuarios: {e}")   

def guardar_usuarios():
    """Guardar los usuarios en un archivo JSON."""
    with open("usuarios.json", "w") as archivo:
        json.dump(usuarios, archivo, indent=4)

def agregar_usuario():
    """Registrar un nuevo usuario o actualizar uno existente."""
    nombre = input("Ingrese el nombre del usuario: ")
    if nombre in usuarios:
        print(f"El usuario '{nombre}' ya existe. ¿Desea actualizar sus datos? (s/n)")
        respuesta = input().strip().lower()
        if respuesta != 's':
            print("Operación cancelada.")
            return
    else:
        print(f"Registrando nuevo usuario: {nombre}.")
    
    # Solicitar datos del usuario
    horario_trabajo = input("Ingrese el horario de trabajo (ejemplo: 9:00 - 17:00): ")
    lugares_conexion = input("Ingrese los lugares de conexión (IPs o localhost, separados por comas): ").split(',')
    
    # Guardar los datos del usuario
    usuarios[nombre] = {
        "horario_trabajo": horario_trabajo,
        "lugares_conexion": [ip.strip() for ip in lugares_conexion]
    }
    
    # Guardar en el archivo
    guardar_usuarios()
    print(f"Los datos de '{nombre}' han sido actualizados exitosamente.")

def mostrar_menu_usuario():
    """Mostrar un menú con las opciones disponibles para el comando 'usuario'."""
    while True:
        print("\n--- Menú de opciones ---")
        print("1. Registrar nuevo usuario / Actualizar usuario")
        print("2. Ver todos los usuarios registrados")
        print("3. Salir")
        opcion = input("Elija una opción: ").strip()
        
        if opcion == "1":
            agregar_usuario()
        elif opcion == "2":
            ver_usuarios()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def ver_usuarios():
    """Mostrar los datos de todos los usuarios registrados."""
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    print("\n--- Usuarios registrados ---")
    for nombre, datos in usuarios.items():
        print(f"Nombre: {nombre}")
        print(f"  Horario de trabajo: {datos['horario_trabajo']}")
        print(f"  Lugares de conexión: {', '.join(datos['lugares_conexion'])}")
        print()

def usuario():
    """Función principal para ejecutar el comando 'usuario' y mostrar el menú."""
    print("\nComando 'usuario' activado.")
    mostrar_menu_usuario()

# Cargar usuarios desde el archivo al inicio del programa
cargar_usuarios()

demonios_file = "demonios.json"

def cargar_demonios():
    """Carga la lista de demonios desde un archivo JSON."""
    if os.path.exists(demonios_file):
        with open(demonios_file, "r") as file:
            return json.load(file)
    return {}

def guardar_demonios(demonios):
    """Guarda la lista de demonios en un archivo JSON."""
    with open(demonios_file, "w") as file:
        json.dump(demonios, file, indent=4)

def registrar_demonio(nombre, comando):
    """Registra un nuevo demonio con su comando de inicio."""
    demonios = cargar_demonios()
    if nombre in demonios:
        print(f"El demonio '{nombre}' ya está registrado.")
    else:
        demonios[nombre] = {"comando": comando, "estado": "detenido"}
        guardar_demonios(demonios)
        print(f"Demonio '{nombre}' registrado exitosamente.")

def iniciar_demonio(nombre):
    """Inicia un demonio registrado."""
    demonios = cargar_demonios()
    if nombre not in demonios:
        print(f"El demonio '{nombre}' no está registrado.")
        return

    if demonios[nombre]["estado"] == "ejecutando":
        print(f"El demonio '{nombre}' ya está en ejecución.")
        return

    try:
        comando = demonios[nombre]["comando"]
        proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        demonios[nombre]["pid"] = proceso.pid
        demonios[nombre]["estado"] = "ejecutando"
        guardar_demonios(demonios)
        print(f"Demonio '{nombre}' iniciado con éxito.")
    except Exception as e:
        print(f"Error al iniciar el demonio '{nombre}': {e}")
        registrar_error()

def detener_demonio(nombre):
    """Detiene un demonio registrado."""
    demonios = cargar_demonios()
    if nombre not in demonios:
        print(f"El demonio '{nombre}' no está registrado.")
        return

    if demonios[nombre]["estado"] != "ejecutando":
        print(f"El demonio '{nombre}' no está en ejecución.")
        return

    try:
        pid = demonios[nombre]["pid"]
        os.kill(pid, 9)
        demonios[nombre]["estado"] = "detenido"
        demonios[nombre]["pid"] = None
        guardar_demonios(demonios)
        print(f"Demonio '{nombre}' detenido con éxito.")
    except Exception as e:
        print(f"Error al detener el demonio '{nombre}': {e}")
        registrar_error()

def estado_demonio(nombre):
    """Muestra el estado de un demonio registrado."""
    demonios = cargar_demonios()
    if nombre not in demonios:
        print(f"El demonio '{nombre}' no está registrado.")
        return

    estado = demonios[nombre]["estado"]
    print(f"El estado del demonio '{nombre}' es: {estado}.")

def menu_demonios():
    """Muestra el menú de gestión de demonios."""
    while True:
        print("\n--- Menú de Gestión de Demonios ---")
        print("1. Registrar un nuevo demonio")
        print("2. Iniciar un demonio")
        print("3. Detener un demonio")
        print("4. Ver estado de un demonio")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre del demonio: ").strip()
            comando = input("Comando para iniciar el demonio: ").strip()
            registrar_demonio(nombre, comando)
        elif opcion == "2":
            nombre = input("Nombre del demonio a iniciar: ").strip()
            iniciar_demonio(nombre)
        elif opcion == "3":
            nombre = input("Nombre del demonio a detener: ").strip()
            detener_demonio(nombre)
        elif opcion == "4":
            nombre = input("Nombre del demonio: ").strip()
            estado_demonio(nombre)
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

sistema_error_log = "/var/log/shell/sistema_error.log"



def ejecutar_comando_sistema(comando):
    """
    Ejecuta comandos del sistema que no sean los mencionados en los comandos específicos de la shell.
    
    :param comando: Comando del sistema ingresado por el usuario.
    """
    try:
        # Ejecutar el comando directamente en el terminal interactivo
        subprocess.run(comando, shell=True)
    except Exception as e:
        print(f"Error al ejecutar el comando: {e}")
        registrar_error(f"Error ejecutando comando: {comando}")




usuario_horarios_log = "usuario_horarios_log"

def validar_horario(ahora, horario_permitido):
    try:
        inicio = datetime.datetime.strptime(horario_permitido['inicio'], "%H:%M").time()
        fin = datetime.datetime.strptime(horario_permitido['fin'], "%H:%M").time()

        # Si el rango cruza la medianoche, manejarlo específicamente
        if inicio > fin:
            return ahora >= inicio or ahora <= fin
        else:
            return inicio <= ahora <= fin
    except ValueError as e:
        registrar_error(f"Formato de hora inválido en horario_permitido: {e}")
        return False


def registrar_evento_sesion(usuario, ip, tipo_evento):
    usuarios = cargar_usuarios()
    if not isinstance(usuarios, dict):
        print("Error: El archivo de usuarios no contiene un formato válido.")
        registrar_error("Archivo usuarios.json no es un diccionario válido.")
        return False

    if usuario not in usuarios:
        print(f"Error: El usuario '{usuario}' no está registrado.")
        registrar_error(f"Intento de sesión con usuario no registrado: {usuario}")
        return False

    ahora = datetime.datetime.now()
    horario_actual = ahora.time()
    usuario_info = usuarios.get(usuario, {})

    try:
        horario_permitido = {
            "inicio": usuario_info["horario_trabajo"].split("-")[0].strip(),
            "fin": usuario_info["horario_trabajo"].split("-")[1].strip(),
        }
    except KeyError as e:
        registrar_error(f"Falta clave en datos de usuario {usuario}: {e}")
        return False

    ips_permitidas = usuario_info.get("lugares_conexion", [])
    dentro_de_horario = validar_horario(horario_actual, horario_permitido)
    ip_permitida = ip in ips_permitidas

    mensaje = f"{ahora.strftime('%Y-%m-%d %H:%M:%S')} - Usuario: {usuario} - Evento: {tipo_evento} - IP: {ip}"
    if not dentro_de_horario:
        mensaje += " (FUERA DE HORARIO)"
    if not ip_permitida:
        mensaje += " (IP NO PERMITIDA)"

    with open(usuario_horarios_log, "a") as log:
        log.write(mensaje + "\n")
    print("Evento de sesión registrado.")
    return True


def mostrar_help():
    print(f"""
    Comandos disponibles:
    copiar <carpeta_origen> <nombre_archivo> <carpeta_destino>  - Copia un archivo de una carpeta a otra.
    mover <carpeta_origen> <nombre_archivo> <carpeta_destino>   - Mueve un archivo de una carpeta a otra.
    renombrar <carpeta_origen> <nombre_archivo> <nuevo_nombre>  - Renombra un archivo en la misma carpeta.
    listar <carpeta>                                           - Lista los archivos y directorios en una carpeta.
    creardir <carpeta>                                         - Crea un nuevo directorio.
    ir <nuevo_directorio>                                      - Cambia al directorio especificado.
    permisos <archivo> <permisos>                              - Cambia los permisos de un archivo (ejemplo: 777, 755).
    propietario <archivo/ruta> <UID> <GID>                     - Cambia el propietario de un archivo o directorio.
    password <usuario> <nueva_contrasena>                    - Cambia la contraseña de un usuario.
    usuario                                                    - Opciones de usuario
    demonios                                                   - Manejo de demonios
    transferencias                                             - Realizar transferencias FTP o SCP
    <comando del sistema>                                      - Ejecuta cualquier comando del sistema no mencionado aquí.
    help                                                       - Muestra esta lista de comandos disponibles.
    salir                                                      - Sale de la shell.

    Directorio actual: {directorio_actual}
        """)
transferencias_log = "Shell_transferencias.log"

def registrar_transferencia(usuario, comando, resultado):
    """
    Registra una transferencia en el log de transferencias.

    :param usuario: Nombre del usuario que realiza la transferencia.
    :param comando: El comando usado para la transferencia.
    :param resultado: Resultado de la transferencia (éxito o error).
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = f"{timestamp} - Usuario: {usuario} - Comando: {comando} - Resultado: {resultado}\n"
    
    with open(transferencias_log, "a") as log:
        log.write(mensaje)

def transferencia_ftp(usuario, servidor, usuario_ftp, clave, archivo_origen, archivo_destino):
    """
    Realiza una transferencia de archivos mediante FTP y la registra en el log.

    :param usuario: Usuario que realiza la transferencia.
    :param servidor: Dirección del servidor FTP.
    :param usuario_ftp: Usuario para autenticación FTP.
    :param clave: Clave del usuario FTP.
    :param archivo_origen: Archivo local a transferir.
    :param archivo_destino: Ruta en el servidor destino.
    """
    try:
        import ftplib
        with ftplib.FTP(servidor, usuario_ftp, clave) as ftp:
            with open(archivo_origen, "rb") as file:
                ftp.storbinary(f"STOR {archivo_destino}", file)
        registrar_transferencia(usuario, f"FTP {archivo_origen} -> {archivo_destino}", "Éxito")
        print(f"Transferencia FTP exitosa de '{archivo_origen}' a '{archivo_destino}'.")
    except Exception as e:
        registrar_transferencia(usuario, f"FTP {archivo_origen} -> {archivo_destino}", f"Error: {e}")
        print(f"Error en transferencia FTP: {e}")
        
        registrar_error()

def transferencia_scp(usuario, archivo_origen, destino):
    """
    Realiza una transferencia de archivos mediante SCP y la registra en el log.

    :param usuario: Usuario que realiza la transferencia.
    :param archivo_origen: Archivo local a transferir.
    :param destino: Ruta destino en formato usuario@host:/ruta.
    """
    try:
        comando = f"scp {archivo_origen} {destino}"
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)

        if resultado.returncode == 0:
            registrar_transferencia(usuario, comando, "Éxito")
            print(f"Transferencia SCP exitosa de '{archivo_origen}' a '{destino}'.")
        else:
            registrar_transferencia(usuario, comando, f"Error: {resultado.stderr}")
            print(f"Error en transferencia SCP: {resultado.stderr}")
    except Exception as e:
        registrar_transferencia(usuario, f"SCP {archivo_origen} -> {destino}", f"Error: {e}")
        print(f"Error en transferencia SCP: {e}")
        

        registrar_error()
def menu_transferencias(usuario):
    """
    Menú para gestionar transferencias FTP o SCP.

    :param usuario: Nombre del usuario que accede al menú.
    """
    while True:
        print("\n--- Menú de Transferencias ---")
        print("1. Transferencia FTP")
        print("2. Transferencia SCP")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            servidor = input("Ingrese el servidor FTP: ").strip()
            usuario_ftp = input("Ingrese el usuario FTP: ").strip()
            clave = input("Ingrese la clave FTP: ").strip()
            archivo_origen = input("Ingrese la ruta del archivo a transferir: ").strip()
            archivo_destino = input("Ingrese la ruta destino en el servidor: ").strip()
            transferencia_ftp(usuario, servidor, usuario_ftp, clave, archivo_origen, archivo_destino)
        elif opcion == "2":
            archivo_origen = input("Ingrese la ruta del archivo a transferir: ").strip()
            destino = input("Ingrese el destino (usuario@host:/ruta): ").strip()
            transferencia_scp(usuario, archivo_origen, destino)
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente nuevamente.")

def shell():
    print("Bienvenido a la shell de archivos. Usa 'help' para ver los comandos disponibles.")
    
    # Solicitar información del usuario
    nombre_usuario = input("Ingrese su nombre de usuario: ").strip()  # Evitar conflicto con 'usuario'
    ip = obtener_ip_local()
    print(f"Conectado desde la IP: {ip}")

    # Registrar inicio de sesión
    if not registrar_evento_sesion(nombre_usuario, ip, "inicio"):
        print("El usuario no está registrado correctamente. Continuará en la shell con acceso limitado.")

    try:
        while True:
            comando = input("Shell> ").strip()  # Leer comando del usuario
            
            if not comando:
                continue  # Si el comando está vacío, vuelve a pedir entrada
            
            partes = comando.split()
            cmd = partes[0].lower()  # Comando principal
            args = partes[1:]  # Argumentos del comando
            
            # Manejo de comandos
            if cmd == "salir":
                print("Saliendo de la shell. ¡Hasta luego!")
                registrar_evento_sesion(nombre_usuario, ip, "salida")
                break
            elif cmd == "help":
                mostrar_help()
            elif cmd == "usuario":
                mostrar_menu_usuario()  # Usar el nombre correcto de la función
            elif cmd == "demonios":
                menu_demonios()  # Ejecutar el menú de demonios
            elif cmd == "transferencias":
                menu_transferencias(nombre_usuario)  # Ejecutar el menú de transferencias
            elif cmd == "copiar" and len(args) == 3:
                copiar_archivo(args[0], args[1], args[2])  # Copiar archivo
            elif cmd == "mover" and len(args) == 3:
                mover_archivo(args[0], args[1], args[2])  # Mover archivo
            elif cmd == "renombrar" and len(args) == 3:
                renombrar_archivo(args[0], args[1], args[2])  # Renombrar archivo
            elif cmd == "listar" and len(args) == 1:
                listar_contenido(args[0])  # Listar contenido de un directorio
            elif cmd == "creardir" and len(args) == 1:
                crear_directorio(args[0])  # Crear un nuevo directorio
            elif cmd == "ir" and len(args) == 1:
                cambiar_directorio(args[0])  # Cambiar el directorio actual
            elif cmd == "permisos" and len(args) == 2:
                cambiar_permisos(args[0], args[1])  # Cambiar permisos de archivo/directorio
            elif cmd == "propietario" and len(args) == 3:
                propietario_comando(args)  # Cambiar propietario de un archivo/directorio
            elif cmd == "password" and len(args) == 2:
                cambiar_password(args[0], args[1])  # Cambia la contraseña del usuario
            elif cmd == "agregar_usuario":
                agregar_usuario()  # Agregar un nuevo usuario
            elif cmd == "mostrar_usuarios":
                mostrar_usuarios()  # Mostrar usuarios registrados
            elif cmd == "actualizar_usuario":
                actualizar_usuario()  # Actualizar un usuario existente
            else:
                 # Si no coincide con comandos personalizados, intentamos ejecutar como comando del sistema
                try:
                    ejecutar_comando_sistema(comando)
                except Exception as e:
                    print(f"Error al ejecutar el comando del sistema: {e}")
                    registrar_error(f"Error ejecutando comando: {comando}")

    except KeyboardInterrupt:
        # Manejar interrupción de teclado (Ctrl+C)
        print("\nSesión terminada por el usuario.")
        registrar_evento_sesion(nombre_usuario, ip, "salida")
        registrar_error("Sesión terminada por el usuario")

if __name__ == "__main__":
    shell()
