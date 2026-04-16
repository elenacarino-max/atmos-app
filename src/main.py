import sys
import time
import ui
from utils import limpiar_pantalla, imprimir_encabezado_h2
from validation import validar_zona_registro, validar_duplicado, validar_fecha_registro
from alerts import evaluar_alerta
import io_manager as io
from logger import configurar_logger, log_info, log_warning, log_error, log_critico
from auth import registrar_usuario, login

def mostrar_menu_inicio():
    """
    Menú inicial antes de entrar en la aplicación.
    """
    print("\n===== ATMOS-APP =====")
    print("1. Registrarse")
    print("2. Iniciar sesión")
    print("3. Salir")


def hacer_registro_usuario():
    """
    Pide los datos para registrar un usuario nuevo.
    """
    print("\n--- REGISTRO DE USUARIO ---")
    usuario = input("Usuario: ")
    email = input("Email: ")
    contrasena = input("Contraseña(8–15, incluye may., min., nº y símbolo): ")

    correcto, mensaje = registrar_usuario(usuario, email, contrasena)
    print(mensaje)


def hacer_login_usuario():
    """
    Pide email y contraseña y comprueba si el login es correcto.
    Devuelve True o False.
    """
    print("\n--- INICIO DE SESIÓN ---")
    email = input("Email: ")
    contrasena = input("Contraseña: ")

    correcto, mensaje = login(email, contrasena)
    print(mensaje)
    return correcto


def menu_acceso():
    """
    Bucle del menú de acceso.
    Solo deja entrar en la app si el login es correcto.
    """
    while True:
        limpiar_pantalla()
        mostrar_menu_inicio()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            hacer_registro_usuario()
            input("\nPulsa Enter para continuar...")

        elif opcion == "2":
            acceso = hacer_login_usuario()
            if acceso:
                return True
            input("\nPulsa Enter para continuar...")

        elif opcion == "3":
            print("Saliendo del programa...")
            return False

        else:
            print("Opción no válida.")
            input("\nPulsa Enter para continuar...")

def ejecutar_registro() -> None:
    """
    Orquesta el flujo completo de creación de una nueva medición meteorológica.
    
    El proceso incluye:
    1. Captura de datos vía UI.
    2. Evaluación de alertas basadas en niveles críticos.
    3. Verificación de registros duplicados (misma fecha y zona).
    4. Persistencia de datos en el almacenamiento.
    
    Returns:
        None
    """
    log_info("Iniciando proceso de captura de nueva medición.")
    registro = ui.solicitar_medicion()

    if registro is None:
        log_info("El usuario canceló la captura de datos.")
        return 
    
    fecha = registro["fecha_registro"] 
    zona = registro["zona_registro"]

    ui.mostrar_resumen_registro(registro)

    # Evaluación de alertas
    alertas = evaluar_alerta(registro)
    if alertas["mensajes"]:
        log_warning(f"Alertas meteorológicas detectadas para {zona}: {alertas['mensajes']}")
        for alerta in alertas["mensajes"]:
            print(f"⚠️  ALERTA: {alerta}")
    
    opcion = ui.mostrar_confirmacion()
    while True:
        try: 
            if opcion == "1":
                # Validar registros duplicados
                datos = io.cargar_datos()
                es_unico = validar_duplicado(fecha, zona, datos)
                
                if not es_unico:
                    log_warning(f"Intento de registro duplicado bloqueado: Zona '{zona}', Fecha {fecha}")
                    print(f"\n⚠️  AVISO: Ya existe una medición para la zona '{zona}' en la fecha {fecha}.")
                    print("No se ha guardado el registro para evitar datos repetidos.")
                    break
                else:
                    # 4. Guardar registro (I/O)
                    registro.update(alertas)

                    print("\n💾 Guardando datos...")
                    time.sleep(0.5)

                    if io.guardar_registro(registro, datos):
                        print(f"\n✅ Registro guardado correctamente.")
                        log_info(f"Registro persistido con éxito en data.json para la zona {zona}.")
                        break
                    else:
                        log_error("Error al intentar guardar el registro a través de io_manager.")
                        break
            elif opcion == "2":
                log_info("El usuario eligió reintentar el registro.")
                limpiar_pantalla()
                imprimir_encabezado_h2("NUEVO REGISTRO ATMOSFÉRICO")
                ejecutar_registro()
                break
            elif opcion == "X":
                log_info("El usuario canceló el guardado y volvió al menú.")
                iniciar_aplicacion()
        except KeyboardInterrupt:
            log_info("Operación cancelada por KeyboardInterrupt (Ctrl+C).")
            return


def consultar_por_zona() -> None:
    """
    Gestiona el submenú de consultas filtradas por zona geográfica.
    
    Carga los datos históricos y permite realizar búsquedas sucesivas. 
    Muestra los resultados formateados en consola y permite reintentar o volver.

    Returns:
        None
    """
    while True:
        try:
            limpiar_pantalla()
            imprimir_encabezado_h2("CONSULTA DE REGISTROS POR ZONA")
            
            datos = io.cargar_datos()
            zona_busqueda = ui.solicitar_zona("Zona/Distrito a consultar: ")

            log_info(f"Consulta realizada para la zona: {zona_busqueda}")
            
            # Filtramos los datos (convertimos a minúsculas para comparar sin errores)
            resultados = [r for r in datos if r["zona_registro"].lower() == zona_busqueda.lower()]

            if resultados:
                print(f"\n🔍 Se ha(n) encontrado {len(resultados)} registros en la zona {zona_busqueda.upper()}:")
                log_info(f"Resultados encontrados para {zona_busqueda}: {len(resultados)}")
                print("-" * 50)
                for r in resultados:
                    print(f"📅 {r['fecha_registro']} | 🌡️  {r['temperatura']}°C | 💧 {r['humedad_nivel']}% | 💨 {r['viento_velocidad']} km/h\n")
                    if r.get("mensajes"):
                        print(f"⚠️ Alertas:")
                        for alerta in r["mensajes"]:
                            print(f"      - {alerta}")
                    else:
                        print("Sin Alertas.\n")
            else:
                print(f"\nℹ️  No se encontraron registros para la zona {zona_busqueda.upper()}")

            # Preguntar al usuario qué desea hacer a continuación
            opcion = ui.mostrar_submenu_consultas()
            
            if opcion == "2":
                break # Sale del bucle de consulta y vuelve al menú principal
            elif opcion != "1":
                print(f"\n⚠️  {opcion} no es una opción válida.")
                input("\nPresione Enter para intentarlo de nuevo...")
        except KeyboardInterrupt:
            log_info("Consulta cancelada por el usuario.")
            print("\n\n⚠️  Operación cancelada por el usuario.")
            return 

def ver_historico():
    import io_manager as io
    datos = io.cargar_datos()

    if not datos:
        print("\n⚠️ No existe datos registrados en el sistema")
        return
    
    #Opcion filtrar por fechas
    while True:
        print("\n---FILTRAR FECHAS---")
        finicio = input("Fecha inicio (YYYY-MM-DD, Enter para ver todo): ").strip()
        ffin = input("Fecha fin (YYYY-MM-DD, Enter para todo): ").strip()

        #Validar filtro fechas
        if finicio == "" and ffin == "":
            finicio = "0000-01-01"
            ffin = "9999-12-31"
        else:
            if finicio != "" and not validar_fecha_registro(finicio):
                print("\nFecha de inicio no válida")
                print("Reintentando...")
                time.sleep(2)
                continue
                
            if ffin != "" and not validar_fecha_registro(ffin):
                print("\nFecha de fin no válida")
                print("Reintentando...")
                time.sleep(2)
                continue

            if finicio == "":
                finicio = "0000-01-01"

            if ffin == "":
                ffin = "9999-12-31"
        
            if finicio > ffin:
                print("\nFecha de inicio no puede ser mayor que fecha fin.")
                print("Reintentando...")
                time.sleep(2)
                continue

        datos_filtrados = [
        r for r in datos
        if finicio <= r["fecha_registro"] <= ffin
        ]

        if not datos_filtrados:
            print("\nNo hay registros en las fechas indicadas.\n")
        
            reintentar = False

            while True:
                print("\n---Opciones---")
                print("[1] Volver a introducir fechas")
                print("[X] Volver al menú principal")

                option = input("Seleccione opción: ").strip().upper()
                if option == "1":
                    reintentar = True
                    break
                elif option == "X":
                    return
                else:
                    print(" La opción seleccionada no es válida.")
            if reintentar:
                continue
        break

    datos_ordenados=sorted(datos_filtrados, key=lambda r:r["fecha_registro"])

    indice=0
    size=10
    paginas=(len(datos_ordenados)-1)//size+1
    cambio_pagina = True

    while True:

        if cambio_pagina:
            inicio = indice * size
            fin = inicio + size
            bloque = datos_ordenados[inicio:fin]

            print("\n HISTORICO (Pag: {}/{}):".format(indice+1, paginas))
            print("-"*50)

            for r in bloque:
                print(f"📅 {r['fecha_registro']} | 🌡️  {r['temperatura']}°C | 💧 {r['humedad_nivel']}% | 💨 {r['viento_velocidad']} km/h\n")
                if r.get("mensajes"):
                            print(f"⚠️ Alertas:")
                            for alerta in r["mensajes"]:
                                print(f"      - {alerta}")
                else:
                    print("Sin Alertas.\n")

        cambio_pagina = False

        print("\nOpciones:")
        print("[1] Siguiente página")
        print("[2] Página anterior")
        print("[X] Salir")

        opcion = input("Seleccione una opción: ").strip().upper()

        if opcion == "1":
            if indice < paginas - 1:
                indice += 1
                cambio_pagina = True
            else:
                print("\nEstás en la última página.")
        elif opcion == "2":
            if indice > 0:
                indice -= 1
                cambio_pagina = True
            else:
                print("\nEstás en la primera página.")
        elif opcion == "X":
            break
        else:
            print("\nOpción no válida.")

            
def iniciar_aplicacion() -> None:
    """
    Punto de entrada principal que mantiene el bucle de ejecución de la App.
    
    Gestiona la navegación entre el registro de datos, las consultas y la 
    salida controlada del sistema.

    Returns:
        None
    """
    while True:
        limpiar_pantalla()
        opcion = ui.mostrar_menu_principal()

        if opcion == "1":
            log_info("Navegando a: Registrar nueva medición")
            limpiar_pantalla()
            imprimir_encabezado_h2("NUEVO REGISTRO ATMOSFÉRICO")
            ejecutar_registro()
            input("\nPresione Enter para continuar...")
        
        elif opcion == "2":
            log_info("Navegando a: Consulta por zona")
            consultar_por_zona()
            input("\nPresione Enter para continuar...")
            
        elif opcion == "3":
            log_info("Navegando a: Histórico de registros")
            ver_historico()
            
        elif opcion == "X":
            log_info("Cierre de aplicación solicitado por el usuario.")
            ui.transicion_despedida()
            sys.exit()

        else:
            log_warning(f"Opción de menú inválida ingresada: {opcion}")
            print(f"\n⚠️  {opcion} no es una opción válida.")
            input("\nPresione Enter para intentarlo de nuevo...")

if __name__ == "__main__":
    # Configurar el logger al arrancar
    configurar_logger()
    log_info("--- SESIÓN INICIADA: Sistema Atmos arrancado correctamente ---")
    
    try:
        ui.transicion_bienvenida()
        acceso_concedido = menu_acceso()

        if acceso_concedido:
            iniciar_aplicacion()
        else:
            ui.transicion_despedida()
            sys.exit()
    except KeyboardInterrupt:
        log_info("Cierre forzado de la aplicación (Ctrl+C).")
        ui.transicion_despedida()
        sys.exit()
    except EOFError:
        pass
    except Exception as e:
        log_critico(f"ERROR CRÍTICO NO CONTROLADO: {str(e)}")
        print(f"\n❌ Error crítico inesperado: {e}")
