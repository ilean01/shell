# shell
Manual de Uso y Guía de Instalación de la Shell Personalizada
1. Introducción
Este documento describe la instalación, configuración y uso de una shell personalizada escrita en Python. La shell permite la gestión de archivos, usuarios, permisos, demonios y transferencias de archivos  SCP.
2. Instalación
La instalación requiere los siguientes pasos
2.1. Requisitos
• Python 3 instalado en el sistema (/usr/bin/python3)
• Privilegios de superusuario para algunas funciones
• Acceso a comandos básicos de Linux

2.2. Instalación Paso a Paso
1. Descargar el script de la shell y guardarlo en un directorio accesible.
2. Darle permisos de ejecución con:
   ```bash
   chmod +x shell.py
   ```
3. Para ejecutarlo manualmente, usar:
   ```bash
   sudo python3 shell.py
   ```
4. Para hacer que la shell se inicie automáticamente al iniciar sesión, agregar lo siguiente al archivo `.bashrc` o `.bash_profile`:
   ```bash
   exec /ruta/a/shell.py
   ```
3. Comandos Disponibles
• help: Muestra la lista de comandos disponibles.
• salir: Finaliza la sesión de la shell.
• copiar <origen> <nombre> <destino>: Copia un archivo a otro directorio.
• mover <origen> <nombre> <destino>: Mueve un archivo de un directorio a otro.
• renombrar <origen> <nombre> <nuevo_nombre>: Renombra un archivo.
• listar <carpeta>: Muestra los archivos y carpetas en un directorio.
• creardir <carpeta>: Crea un nuevo directorio.
• ir <nuevo_directorio>: Cambia el directorio actual.
• permisos <archivo> <permisos>: Cambia los permisos de un archivo o directorio.
• propietario <archivo/ruta> <UID> <GID>: Cambia el propietario de un archivo o directorio.
• contrasena <usuario> <nueva_contrasena>: Cambia la contraseña de un usuario.
• agregar_usuario <nombre> <horario> <ips>
• demonios: Accede al menú de gestión de demonios.
• transferencias: Permite realizar transferencias SCP.
• <comando del sistema>: Ejecuta cualquier comando estándar de Linux.
4. Gestión de Usuarios
La shell permite registrar y cambiar contraseñas del usuario si este tiene permisos de root.
5. Gestión de Demonios
Permite administrar procesos en segundo plano.
5.1. Registrar un Demonio
1. Ejecutar `demonios`
2. Seleccionar `1. Registrar un nuevo demonio`
3. Ingresar el nombre y su direccion.

5.2. Iniciar/Detener Demonio
Para iniciar:
1. Ejecutar `demonios`
2. Seleccionar `1. Iniciar un demonio`
3. Especificar el nombre del demonio.

Para detener:
1. Ejecutar `demonios`
2. Seleccionar `0. Detener un demonio`
3. Introduzca el nombre del demonio


6. Transferencias de Archivos
Permite transferencias seguras mediante SCP.
Transferencia SCP
1. Ejecutar `transferencias`
2. Ecriba `2. Transferencia <Archivo> <Ruta>`

7. Registro de Errores y Eventos
Todos los errores y eventos son registrados en los siguientes archivos:
• `/var/log/shell/sistema_error.log`: Errores del sistema.
• `usuario_horarios_log`: Eventos de sesión.
• `Shell_transferencias.log`: Transferencias de archivos.

8. Ejecución de Comandos del Sistema
Además de los comandos personalizados, esta shell permite ejecutar cualquier comando estándar de Linux.
Ejemplos:
• `vim archivo.txt`
• `ls -la`
• `chmod 777 script.sh`

9. Cierre de Sesión
Para salir de la shell, usa el comando `salir` o presiona `Ctrl+C`.
