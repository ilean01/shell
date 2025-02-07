#!/usr/bin/python3

import shutil
import os
import json  # Para almacenar los datos en formato JSON
import socket
import shlex
usuario_horarios_log = "usuario_horarios_log"
USER_DATA = "/usr/local/bin/user_data.txt"
os.environ["PATH"] = "/bin:/usr/bin:/usr/local/bin:" + os.environ.get("PATH", "")
usuarios = {}
sistema_error_log = "/var/log/shell/sistema_error.log"

def registrar_error(mensaje):
    if not os.path.exists("/var/log/shell"):
        os.makedirs("/var/log/shell", exist_ok=True)
    if not os.path.isfile(sistema_error_log):
        open(sistema_error_log, "w").close()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(sistema_error_log, "a") as log:
             log.write(f"{timestamp} - ERROR: {mensaje}\n")
    except Exception as e:
        print(f"Error al escribir en el log: {e}")

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
    """
    try:
        # Comando para agregar el usuario
        comando_crear = f"sudo useradd {nombre_usuario} -m"
        resultado = subprocess.run(comando_crear, shell=True, check=True, capture_output=True, text=True)
        print(f"Usuario '{nombre_usuario}' creado en el sistema operativo.")

        # Si se proporciona una contraseña, establecerla
        if contrasena:
            comando_contrasena = f"echo '{nombre_usuario}:{contrasena}' | sudo chpasswd"
            subprocess.run(comando_contrasena, shell=True, check=True, capture_output=True, text=True)
            print(f"Contraseña configurada para el usuario '{nombre_usuario}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error al crear el usuario '{nombre_usuario}': {e.stderr}")
        registrar_error(f"Error al crear el usuario '{nombre_usuario}': {e.stderr}")
    except Exception as e:
        print(f"Error inesperado al crear el usuario '{nombre_usuario}': {e}")
        registrar_error(f"Error inesperado al crear el usuario '{nombre_usuario}': {e}")






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


def agregar_usuario(nombre, horario, ips):
    try:
        # Crear el usuario en el sistema
        comando = f"useradd -m {nombre}"
        result = subprocess.run(comando, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error al crear el usuario '{nombre}'.")
            return

        # Establecer contraseña
        print(f"Estableciendo contraseña para '{nombre}'.")
        # Solicitar la contraseña de forma segura
        contrasena = getpass.getpass(f"Introduce la contraseña para el usuario {nombre}: ")

        # Comando para establecer la contraseña
        comando_passwd = f"echo {nombre}:{contrasena} | chpasswd"
        result = subprocess.run(comando_passwd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error al establecer la contraseña para '{nombre}'.")
            return

        # Guardar los datos del usuario en el archivo
        with open(USER_DATA, "a") as archivo:
            archivo.write(f"Usuario: {nombre}\n")
            archivo.write(f"Horario: {horario}\n")
            archivo.write(f"IPs permitidas: {ips}\n")
            archivo.write("-----------------------------------\n")

        print(f"Usuario '{nombre}' creado exitosamente con horario '{horario}' y acceso desde '{ips}'.")

    except Exception as e:
        print(f"Error: {e}")


def ejecutar_comando_sistema(comando):
    """
    Ejecuta cualquier comando del sistema, incluyendo comandos como ls, cd, vim, nano, etc.
    """
    global directorio_actual

    try:
        # Si el usuario usa "cd", cambiamos el directorio manualmente
        if comando.startswith("cd "):
            nuevo_directorio = comando.split(" ", 1)[1].strip()  # Extraer el directorio
            if os.path.isdir(nuevo_directorio):
                os.chdir(nuevo_directorio)  # Cambiar en Python
                directorio_actual = os.getcwd()  # Actualizar variable global
                print(f"Directorio cambiado a: {directorio_actual}")
            else:
                print(f"Error: El directorio '{nuevo_directorio}' no existe.")
            return  # Salir de la función para evitar ejecutar en subprocess

        # Ejecutar cualquier otro comando en un shell real
        subprocess.run(comando, shell=True, executable="/bin/bash")

    except FileNotFoundError:
        print(f"Error: Comando no encontrado -> {comando}")
        registrar_error(f"Error: Comando no encontrado -> {comando}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar '{comando}': {e}")
        registrar_error(f"Error ejecutando comando: {comando}")
    except Exception as e:
        print(f"Error inesperado: {e}")
        registrar_error(f"Error inesperado ejecutando comando: {comando}")

def validar_datos_usuario(datos):
    horario = datos.get("horario_trabajo", "").strip()
    lugares = datos.get("lugares_conexion", [])

    if not horario or not lugares:
        print("Advertencia: Datos incompletos para el usuario. Asumiendo valores por defecto.")
        return {
            "horario_trabajo": "00:00 - 23:59",
            "lugares_conexion": ["127.0.0.1"]
        }
    return datos



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
    usuarios = os.getenv("USER") or os.getenv("LOGNAME") or "desconocido"

    if not isinstance(usuarios, dict):

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
    copiar <origen> <nombre> <destino>          - Copia un archivo.
    mover <origen> <nombre> <destino>           - Mueve un archivo.
    renombrar <origen> <nombre> <nuevo_nombre>  - Renombra un archivo.
    listar <carpeta>                            - Ver archivos y directorios.
    creardir <carpeta>                          - Crea un nuevo directorio.
    ir <nuevo_directorio>                       - Cambia al directorio deseado.
    permisos <archivo> <permisos>               - Cambia los permisos de archivo.
    propietario <archivo/ruta> <UID> <GID>      - Cambia el propietario.
    password <usuario> <nueva_contrasena>       - Cambia la contraseña.
    agregar_usuario <nombre> <horario> <ips>    - Opciones de usuario
    demonios                                    - Manejo de demonios
    transferencias <origen> <destino>           - Hacer ransferencias FTP o SCP
    <comando del sistema>                       - Ejecuta cualquier comando.
    help                                        - Ayuda.
    salir                                       - Sale de la shell.

    Directorio actual: {directorio_actual}
        """)

import datetime

def registrar_historial(comando):
    log_path = "/home/historial.log"  # Ruta fija para el archivo de log

    try:
        # Obtener la marca de tiempo actual
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Abrir el archivo en modo "append" (agregar al final)
        with open(log_path, "a") as archivo:
            archivo.write(f"{timestamp}: {comando}\n")  # Escribir la fecha y comando

    except Exception as e:
        print(f"Error al abrir {log_path}: {e}")


import subprocess

def obtener_timestamp():
    # Obtener la fecha y hora actual en formato YYYY-MM-DD HH:MM:SS
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def obtener_timestamp():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def transferencia_archivo(origen=None, destino=None, metodo=None):
    log_path = "/home/Shell_transferencias.log"

    # Verificar que los parámetros no sean None o vacíos
    if not origen or not destino or not metodo:
        print("Error: Parámetros inválidos. Debes proporcionar origen, destino y método.")
        return

    try:
        with open(log_path, "a") as archivo:
            timestamp = obtener_timestamp()

            if metodo == "scp":
                archivo.write(f"{timestamp}: Transferencia de {origen} a {destino} usando SCP\n")

                comando = f"scp {origen} {destino}"
                print(f"Ejecutando: {comando}")

                result = subprocess.run(comando, shell=True, capture_output=True, text=True)

                if result.returncode != 0:
                    archivo.write(f"{timestamp}: Error durante la transferencia: {result.stderr}\n")
                    print(f"Error en la transferencia: {result.stderr}")
                else:
                    archivo.write(f"{timestamp}: Transferencia exitosa\n")
                    print("Transferencia completada con éxito.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de origen '{origen}'.")
    except PermissionError:
        print(f"Error: Permiso denegado al acceder a '{origen}' o '{destino}'.")
    except Exception as e:
        print(f"Error inesperado: {e}")




import os
import sys
import signal

def levantar_demonio(nombre_demonio, ruta_binario):
    print(f"Intentando iniciar el demonio '{nombre_demonio}'")

    pid = os.fork()
    if pid == 0:
        # Proceso hijo: se convierte en demonio
        try:
            # Crear una nueva sesión para el demonio
            os.setsid()
        except Exception as e:
            print(f"Error al crear sesión de demonio: {e}")
            sys.exit(1)

        # Redirigir entradas/salidas a /dev/null
        sys.stdin = open(os.devnull, 'r')
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

        # Ejecutar el binario del demonio
        try:
            os.execv(ruta_binario, [ruta_binario])
        except Exception as e:
            print(f"Error al ejecutar el demonio: {e}")
            sys.exit(1)
    elif pid > 0:
        # Proceso padre guarda el PID del demonio
        pid_path = f"/var/run/{nombre_demonio}.pid"
        try:
            with open(pid_path, "w") as pid_file:
                pid_file.write(f"{pid}\n")
            print(f"Demonio '{nombre_demonio}' iniciado con PID {pid}")
        except Exception as e:
            print(f"Error al guardar el archivo PID: {e}")
    else:
        print("Error al crear proceso para el demonio")




def apagar_demonio(nombre_demonio):
    print(f"Intentando detener el demonio '{nombre_demonio}'")

    pid_path = f"/var/run/{nombre_demonio}.pid"
    try:
        with open(pid_path, "r") as pid_file:
            pid = int(pid_file.read().strip())
    except Exception as e:
        print(f"Error al leer el archivo PID: {e}")
        return

    try:
        # Enviar la señal SIGTERM al demonio
        os.kill(pid, signal.SIGTERM)
        print(f"Demonio '{nombre_demonio}' detenido con éxito")
        os.remove(pid_path)  # Eliminar el archivo PID
    except Exception as e:
        print(f"Error al detener el demonio: {e}")



def gestionar_demonio():
    # Preguntar al usuario si desea levantar o apagar el demonio
    accion = input("Pon 1 para levantar demonio o 0 para apagar: ")

    # Verificar que la acción es válida
    if accion not in ['0', '1']:
        print("Acción no válida. Debes ingresar 1 para levantar o 0 para apagar.")
        return

    nombre_demonio = input("Pon el nombre del demonio: ")

    if accion == '1':  # Levantar demonio
        ruta_binario = input("Pon la ruta del binario: ")
        print(f"Intentando iniciar el demonio '{nombre_demonio}' con binario en '{ruta_binario}'")
        levantar_demonio(nombre_demonio, ruta_binario)
    elif accion == '0':  # Apagar demonio
        print(f"Intentando detener el demonio '{nombre_demonio}'")
        apagar_demonio(nombre_demonio)

import getpass
def agregar_usuario(nombre, horario, ips):
    try:
        # Crear el usuario en el sistema
        comando = f"useradd -m {nombre}"
        result = subprocess.run(comando, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error al crear el usuario '{nombre}'.")
            return

        # Establecer contraseña
        print(f"Estableciendo contraseña para '{nombre}'.")
        # Solicitar la contraseña de forma segura
        contrasena = getpass.getpass(f"Introduce la contraseña para el usuario {nombre}: ")

        # Comando para establecer la contraseña
        comando_passwd = f"echo {nombre}:{contrasena} | chpasswd"
        result = subprocess.run(comando_passwd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error al establecer la contraseña para '{nombre}'.")
            return

        # Guardar los datos del usuario en el archivo
        with open(USER_DATA, "a") as archivo:
            archivo.write(f"Usuario: {nombre}\n")
            archivo.write(f"Horario: {horario}\n")
            archivo.write(f"IPs permitidas: {ips}\n")
            archivo.write("-----------------------------------\n")

        print(f"Usuario '{nombre}' creado exitosamente con horario '{horario}' y acceso desde '{ips}'.")

    except Exception as e:
        print(f"Error: {e}")

def cambiar_contrasena():
    usuario = os.getenv("USER")  # Obtener el nombre del usuario actual
    if not usuario:
        print("No se pudo determinar el usuario actual.")
        return

    print(f"Cambiando contraseña para el usuario '{usuario}'.")

    # Crear el comando para llamar a 'passwd' con el usuario actual
    comando = f"passwd {usuario}"  # Se genera el comando "passwd juan" por ejemplo

    # Ejecutar el comando
    try:
        resultado = subprocess.run(comando, shell=True, check=True)
        print("Contraseña cambiada exitosamente.")
    except subprocess.CalledProcessError:
        print("Error al cambiar la contraseña.")


def shell():


    print("Bienvenido a la shell de archivos. Usa 'help' para ver los comandos disponibles.")

    # Solicitar información del usuario
    nombre_usuario = os.getenv("USER") or os.getenv("LOGNAME") or "desconocido"
    ip = obtener_ip_local()
    print(f"Conectado desde la IP: {ip}")

    # Registrar inicio de sesión
    if not registrar_evento_sesion(nombre_usuario, ip, "inicio"):
        print(" ")

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
                subprocess.run(["/bin/bash"])  # Abre Bash automáticamente
                break
            elif cmd == "help":
                registrar_historial("help")
                mostrar_help()
             #
            elif cmd == "demonios":
                registrar_historial("demonios")
                gestionar_demonio()  # Llamada a la función que gestiona demonios
            elif cmd == "transferencias":
                if len(args) < 3:
                   print("Error: Debes ingresar origen, destino y método.")
                   continue  # Volver a pedir un comando

                origen = args[0]
                destino = args[1]

                registrar_historial("transferencias")
                transferencia_archivo(args[0], args[1])  # Ejecutar el menú de transferencias
            elif cmd == "copiar" and len(args) == 3:
                registrar_historial(f"copiar {args}")
                copiar_archivo(args[0], args[1], args[2])  # Copiar archivo
            elif cmd == "mover" and len(args) == 3:
                registrar_historial(f"mover {args}")
                mover_archivo(args[0], args[1], args[2])  # Mover archivo
            elif cmd == "renombrar" and len(args) == 3:
                registrar_historial(f"renombrar {args}")
                renombrar_archivo(args[0], args[1], args[2])  # Renombrar archivo
            elif cmd == "listar" and len(args) == 1:
                registrar_historial(f"listar {args}")
                listar_contenido(args[0])  # Listar contenido de un directorio
            elif cmd == "creardir" and len(args) == 1:
                registrar_historial(f"creardir {args}")
                crear_directorio(args[0])  # Crear un nuevo directorio
            elif cmd == "ir" and len(args) == 1:
                registrar_historial(f"ir {args}")
                cambiar_directorio(args[0])  # Cambiar el directorio actual
            elif cmd == "permisos" and len(args) == 2:
                registrar_historial(f"permisos {args}")
                cambiar_permisos(args[0], args[1])  # Cambiar permisos de archivo/directorio
            elif cmd == "propietario" and len(args) == 3:
                registrar_historial(f"propietario {args}")
                propietario_comando(args)  # Cambiar propietario de un archivo/directorio
            elif cmd == "contrasena":
                registrar_historial(f"password ")
                cambiar_contrasena()
            elif cmd == "agregar_usuario":
                registrar_historial("agregar_usuario")
                # Verificar que se pasen los argumentos necesarios
                if len(args) < 3:
                    print("Error: Se requieren tres parámetros: nombre de usuario, horario y direcciones IP permitidas.")
                    continue
                else:
                   nombre = args[0]
                   horario = args[1]
                   ips = args[2]
                   agregar_usuario(nombre, horario, ips)
            else:
                try:
                    ejecutar_comando_sistema(comando)
                    registrar_historial(f"sistema {comando}")
                except Exception as e:
                    print(f"Error al ejecutar el comando del sistema: {e}")
                    registrar_error(f"Error ejecutando comando: {comando}")

    except KeyboardInterrupt:
        # Manejar interrupción de teclado (Ctrl+C)
        print("\nSesión terminada por el usuario.")
        registrar_evento_sesion(nombre_usuario, ip, "salida")
        registrar_error("Sesión terminada por el usuario")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Este script requiere permisos de superusuario. Ejecútelo con sudo.")
        exit(1)

    usuarios = {}  # Variable global para almacenar los usuarios
    # Cargar los usuarios desde el archivo al iniciar el programa
    shell()
