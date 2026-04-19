import sys
from datetime import datetime
import time
import ui
from utils import limpiar_pantalla, imprimir_encabezado_h2, formatear_texto, borrar_lineas
from validation import validar_duplicado, validar_fecha_registro
from alerts import evaluar_alerta
import io_manager as io
from auth import registrar_usuario, login
from stats import mostrar_grafico_interactivo
from logger import configurar_logger, log_info, log_warning, log_error, log_critico

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



    contrasena = input("Contraseña (Mínimo 8 caracteres: letras (A-z), \nnúmeros (0-9) y caracteres especiales): ")


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
    
    limpiar_pantalla()
    imprimir_encabezado_h2("NUEVO REGISTRO ATMOSFÉRICO")
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
            print(f"  {formatear_texto('Alerta')}: {alerta}")
    
    opcion = ui.mostrar_confirmacion()
    while True:
        try: 
            if opcion == "1":
                # Validar registros duplicados
                datos = io.cargar_datos()
                es_unico = validar_duplicado(fecha, zona, datos)
                
                if not es_unico:
                    log_warning(f"Intento de registro duplicado bloqueado: Zona '{zona}', Fecha {fecha}")
                    print(f"\n  {formatear_texto('AVISO', "amarillo")}: Ya existe una medición para la zona '{zona}' en la fecha {fecha}.")
                    print("No se ha guardado el registro para evitar datos repetidos.")
                    break
                else:
                    # 4. Guardar registro (I/O)
                    registro.update(alertas)

                    print("\n...Guardando datos...")
                    time.sleep(0.5)

                    if io.guardar_registro(registro, datos):
                        print(f"\nRegistro guardado correctamente.")
                        time.sleep(1)
                        log_info(f"Registro persistido con éxito en data.json para la zona {zona}.")
                        break
                    else:
                        log_error("Error al intentar guardar el registro a través de io_manager.")
                        break
            elif opcion == "2":
                log_info("El usuario canceló guardar y reintenta el registro.")
                ejecutar_registro()
            elif opcion == "X":
                log_info("El usuario canceló guardar y volvió al menú principal.")
                return
        except KeyboardInterrupt:
            log_info("Operación cancelada por KeyboardInterrupt (Ctrl+C).")
            print(f"\n\n  {formatear_texto('Operación cancelada', 'amarillo')}")
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
            zona_busqueda = ui.solicitar_zona("Zona a consultar: ")

            log_info(f"Consulta realizada para la zona: {zona_busqueda}")
            
            # Filtramos y ordenamos los datos
            resultados = [r for r in datos if r["zona_registro"].lower() == zona_busqueda.lower()]
            resultados.sort(key=lambda r: datetime.strptime(r['fecha_registro'], "%Y-%m-%d"), reverse=True)

            if resultados:
                num_resultados = len(resultados)
                zona = formatear_texto(zona_busqueda.upper(), "blanco")
                num = formatear_texto(num_resultados, "blanco") 
                if num_resultados == 1:
                    print(f"\n Se ha encontrado {num} registro en la zona {zona}:")
                else:
                    print(f"\n Se han encontrado {num} registros en la zona {zona}:")
                
                log_info(f"Resultados encontrados para {zona_busqueda}: {num_resultados}")
                
                print("-" * 50)
                for r in resultados:
                    fecha = formatear_texto(r['fecha_registro'], color="blanco")
                    print(f" {fecha} | {r['temperatura']}°C | {r['humedad_nivel']}% |"
                          f" {r['viento_velocidad']} km/h")
                    if r.get("mensajes"):
                        print(f"\n   {formatear_texto('Alertas')}:")
                        for alerta in r["mensajes"]:
                            print(f"        - {alerta}")
                    print('.' * 50)
     
            else:
                zona_error = formatear_texto(zona_busqueda.upper())
                print(f"\nNo se encontraron registros para la zona {zona_error}")

            # Preguntar al usuario qué quiere hacer a continuación
            while True: 
                opcion = ui.mostrar_submenu_consultas()
            
                if opcion == "1":
                    break
                elif opcion == "X":
                    log_info("Usuario regresó al menú principal.")
                    return
                
                print(f"\n '{opcion if opcion else ' '}' no es una opción válida.")
                time.sleep(1)
                borrar_lineas(8)

        except KeyboardInterrupt:
            log_info("Consulta cancelada por el usuario.")
            print(f"\n\n  {formatear_texto('Operación cancelada', 'amarillo')}: "
                   "Volviendo al menú principal.")
            time.sleep(2)
            return 

def ver_historico():
    datos = io.cargar_datos()

    if not datos:
        print("\nNo existe datos registrados en el sistema")
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
                fecha = formatear_texto(r['fecha_registro'], color="blanco")
                print(f" {fecha} | {r['temperatura']}°C | {r['humedad_nivel']}% |"
                      f" {r['viento_velocidad']} km/h\n")
                if r.get("mensajes"):
                    print(f"   {formatear_texto('Alertas')}:")
                    for alerta in r["mensajes"]:
                        print(f"        - {alerta}")
                else:
                    print("Sin Alertas.\n")
                print('.' * 50)

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

def estadisticas_por_zona() -> None:
    """
    Muestra gráficos meteorológicos por zona.
    
    Procesa datos de temperatura, viento y humedad, genera gráficos
    y maneja entrada del usuario en bucle hasta volver al menú principal.

    Returns:
        None
    """
    datos = io.cargar_datos()
    
    if not datos:
        log_warning("Consulta de estadísticas fallida: Archivo de datos vacío o no encontrado.")
        print("\nNo hay datos registrados para analizar.")
        return
    
    while True:
        try:
            limpiar_pantalla()
            imprimir_encabezado_h2("GRÁFICOS")

            zona_buscada = ui.solicitar_zona("Zona a consultar: ")
            datos_zona = [d for d in datos if d['zona_registro'].lower() == zona_buscada]
            datos_zona.sort(key=lambda d: datetime.strptime(d['fecha_registro'], "%Y-%m-%d"))
            
            if datos_zona:
                log_info(f"Generando estadísticas para zona: {zona_buscada} ({len(datos_zona)} registros)")
                
                try:
                    fechas = [datetime.strptime(d['fecha_registro'], "%Y-%m-%d") for d in datos_zona]
                    datos_grafico = {
                                'temperatura': {
                                    'datos': [d['temperatura'] for d in datos_zona],
                                    'alertas': [d.get('alerta_temperatura', False) for d in datos_zona]
                                },
                                'humedad': {
                                    'datos': [d['humedad_nivel'] for d in datos_zona],
                                    'alertas': [d.get('alerta_humedad', False) for d in datos_zona]
                                },
                                'viento': {
                                    'datos': [d['viento_velocidad'] for d in datos_zona],
                                    'alertas': [d.get('alerta_viento', False) for d in datos_zona]
                                }
                    }

                    mostrar_grafico_interactivo(fechas, datos_grafico, zona_buscada.upper())
            
                except ValueError as ve:
                    log_error(f"Error de conversión de tipos en zona {zona_buscada}: {ve}")
                    print(f"{formatear_texto('Error')}: Datos corruptos detectados en "
                          "los registros de esta zona.")
            
            else:
                log_error(f"La zona '{zona_buscada}' no existe en la base de datos.")
                print(f"No existen registros de la zona '{zona_buscada}'.")
        
            # Preguntar al usuario qué quiere hacer a continuación
            while True: 
                opcion = ui.mostrar_submenu_consultas()
            
                if opcion == "1":
                    break
                elif opcion == "X":
                    log_info("Usuario regresó al menú principal.")
                    return
                
                print(f"\n  '{opcion if opcion else ' '}' no es una opción válida.")
                time.sleep(1)
                borrar_lineas(8)

        except KeyboardInterrupt:
            log_info("Consulta de estadísiticas cancelada por el usuario.")
            print(f"\n\n  {formatear_texto('Operación cancelada', 'amarillo')}: "
                   "Volviendo al menú principal.")
            time.sleep(2)
            return

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
            ejecutar_registro()
        
        elif opcion == "2":
            log_info("Navegando a: Consulta por zona")
            consultar_por_zona()
            
        elif opcion == "3":
            log_info("Navegando a: Histórico de registros")
            ver_historico()
        
        elif opcion == "4":
            log_info("Navegando a: Estadísticas")
            estadisticas_por_zona()
            
        elif opcion == "X":
            log_info("Cierre de aplicación solicitado por el usuario.")
            ui.transicion_despedida()
            sys.exit()

        else:
            log_warning(f"Opción de menú inválida: {opcion}")
            print(f"\n  '{opcion if opcion else ' '}' no es una opción válida.")
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
        print(f"\n {formatear_texto('Error crítico')} inesperado: {e}")
