def leer_datos(nombrearchivo):
    from collections import defaultdict #clase especial de diccionario
    #sirve para definir  valor por defecto tendrá cada nueva clave automáticamente.

    datos = defaultdict(lambda: {"tmax": [], "tmin": []})
    
    fechas = []  # almacena las fechas en orden

    #abrir el archivo
    with open(nombrearchivo, 'r', encoding='latin1') as archivo:
        lineas = archivo.readlines()[3:]  # saltea las primeras 3 lineas del txt porque no tienen datos

        fecha_actual = None
        estaciones_en_fecha = set()

        for linea in lineas:
            if not linea.strip():
                continue

            # Toma de caracteres para las variables correspondientes
            fecha = linea[0:8].strip() 
            tmax_str = linea[8:14].strip() 
            tmin_str = linea[14:20].strip() 
            estacion = linea[20:].strip() 

            # las estaciones que faltan las lleno con none
            if fecha != fecha_actual:
                if fecha_actual is not None:
                    for est in datos:
                        if est not in estaciones_en_fecha:
                            datos[est]["tmax"].append(None)
                            datos[est]["tmin"].append(None)
                fecha_actual = fecha
                fechas.append(fecha)
                estaciones_en_fecha = set()

            # Parseo valores 
            tmax = float(tmax_str) if tmax_str and tmax_str.strip() else None
            tmin = float(tmin_str) if tmin_str and tmin_str.strip() else None

            datos[estacion]["tmax"].append(tmax)
            datos[estacion]["tmin"].append(tmin)
            estaciones_en_fecha.add(estacion)

        # último día: relleno los que faltaron
        for est in datos:
            if est not in estaciones_en_fecha:
                datos[est]["tmax"].append(None)
                datos[est]["tmin"].append(None)

    return datos, fechas

def generar_reporte(datos, nombre_reporte="reporte.txt"):
   
    with open(nombre_reporte, "w", encoding="latin1") as salida:
        
        salida.write("Reporte anual de estaciones: \n\n")

        # 1. Tmax y Tmin anual por estación
        for estacion, temps in datos.items():
            # Filtrar valores None
            tmax_validos = [t for t in temps["tmax"] if t is not None]
            tmin_validos = [t for t in temps["tmin"] if t is not None]
            
            maximo = max(tmax_validos) if tmax_validos else "N/A"
            minimo = min(tmin_validos) if tmin_validos else "N/A"
            salida.write(f"{estacion}: Tmax anual = {maximo}, Tmin anual = {minimo}\n")

        # 2. Buscar mayor y menor amplitud térmica diaria
        mayor_amp = (-1, None, None)  # (amplitud, estacion, dia)
        menor_amp = (float('inf'), None, None)

        # Encontrar el número máximo de días
        dias = max(len(temps["tmax"]) for temps in datos.values())

        for dia in range(dias):
            for estacion, temps in datos.items():
                if dia >= len(temps["tmax"]):
                    continue
                    
                tmax = temps["tmax"][dia]
                tmin = temps["tmin"][dia]
                
                if tmax is None or tmin is None:
                    continue
                    
                amplitud = tmax - tmin
                if amplitud > mayor_amp[0]:
                    mayor_amp = (amplitud, estacion, dia + 1)
                if amplitud < menor_amp[0]:
                    menor_amp = (amplitud, estacion, dia + 1)

        salida.write("\nAmplitud termica: \n")
        salida.write(f"Mayor amplitud: {mayor_amp[0]} en {mayor_amp[1]} el dia {mayor_amp[2]}\n")
        salida.write(f"Menor amplitud: {menor_amp[0]} en {menor_amp[1]} el dia {menor_amp[2]}\n")

        # 3. En un mismo dia la máxima y la mínima diferencia entre estaciones 
        max_diff = (-1, None, None, None, None, None)  # (valor, est1, t1, est2, t2, dia)
        min_diff = (float('inf'), None, None, None, None, None)

        for dia in range(dias):
            # Obtener todas las temperaturas válidas para este día
            temperaturas_dia = {}
            for estacion, temps in datos.items():
                if dia < len(temps["tmax"]) and temps["tmax"][dia] is not None:
                    temperaturas_dia[estacion] = temps["tmax"][dia]
            
            # Comparo todas las estaciones entre ellas
            estaciones = list(temperaturas_dia.keys())
            for i in range(len(estaciones)):
                for j in range(i + 1, len(estaciones)):
                    est1 = estaciones[i]
                    est2 = estaciones[j]
                    t1 = temperaturas_dia[est1]
                    t2 = temperaturas_dia[est2]
                    
                    diff = abs(t1 - t2)
                    if diff > max_diff[0]:
                        max_diff = (diff, est1, t1, est2, t2, dia + 1)
                    if diff < min_diff[0]:
                        min_diff = (diff, est1, t1, est2, t2, dia + 1)

        salida.write("\nDiferencias entre estaciones: \n")
        salida.write(f"Maxima diferencia: {max_diff[0]} entre {max_diff[1]}({max_diff[2]}) y {max_diff[3]}({max_diff[4]}) en el dia: {max_diff[5]} del año\n")
        salida.write(f"Minima diferencia: {min_diff[0]} entre {min_diff[1]}({min_diff[2]}) y {min_diff[3]}({min_diff[4]}) en el dia: {min_diff[5]}del año\n")


def main():
    archivo_datos = "registro_temperatura365d_smn.txt"
    datos, fechas = leer_datos(archivo_datos)
    generar_reporte(datos)


if __name__ == "__main__":
    main()
