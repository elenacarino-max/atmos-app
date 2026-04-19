# src/launcher.py

from auth import registrar_usuario, login
from ui import capturar_datos_estacion
from io_manager import cargar_datos, guardar_registro


def mostrar_menu_acceso():
    """
    Muestra el menú inicial de autenticación.
    """
    print("\n===== ATMOS-APP =====")
    print("1. Registrarse")
    print("2. Iniciar sesión")
    print("3. Salir")


def hacer_registro():
    """
    Pide usuario, email y contraseña, y registra al usuario.
    """
    print("\n--- REGISTRO ---")
    usuario = input("Usuario: ")
    email = input("Email: ")
    contrasena = input("Contraseña: ")

    correcto, mensaje = registrar_usuario(usuario, email, contrasena)
    print(mensaje)


def hacer_login():
    """
    Pide email y contraseña, e intenta iniciar sesión.
    """
    print("\n--- LOGIN ---")
    email = input("Email: ")
    contrasena = input("Contraseña: ")

    correcto, mensaje = login(email, contrasena)
    print(mensaje)
    return correcto


def ejecutar_programa_principal():
    """
    Llama a la parte principal de Atmos-App:
    captura datos y los guarda en data/data.json.
    """
    print("\n Acceso concedido. Entrando en Atmos-App...")

    # 1. Capturamos un nuevo registro desde ui.py
    nuevo_registro = capturar_datos_estacion()

    # Si por cualquier motivo no devuelve datos válidos, paramos
    if not nuevo_registro:
        print(" No se pudo crear el registro.")
        return

    # 2. Cargamos el histórico actual
    datos = cargar_datos()

    # 3. Guardamos el nuevo registro
    guardado = guardar_registro(nuevo_registro, datos)

    if guardado:
        print("\n Registro guardado correctamente en data/data.json")
    else:
        print("\n Error al guardar el registro.")


def main():
    """
    Bucle principal del launcher.
    """
    while True:
        mostrar_menu_acceso()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            hacer_registro()

        elif opcion == "2":
            acceso = hacer_login()

            if acceso:
                ejecutar_programa_principal()

        elif opcion == "3":
            print("Saliendo del programa...")
            break

        else:
            print(" Opción no válida.")


if __name__ == "__main__":
    main()