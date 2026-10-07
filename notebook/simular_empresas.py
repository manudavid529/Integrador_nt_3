'''
Organizacion que registra o propone retos. Crea el script `src/simular_empresas.py`. Con la libreria **Faker** genera 300 filas falsas de la tabla `empresas`, con las MISMAS columnas que usa Backend II. Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.

'''

# Todas las constantes en mayusculas, las variables en minusculas y los comentarios en español.

import random
import uuid
import pandas as pd
from faker import Faker

#1. Configurar el faker a la region que necesito.
fake = Faker("es_CO")

#2. Sembrar semilla para tener coherencia en los datos generados.
#simulados
Faker.seed(42)
random.seed(42)

#3. Identifico los datos que debo simular.
# id (texto (UUID)) 
# nombre (texto)
# nit (texto)
# sector (texto) elementos a seleccionar de una lista de sectores
# contacto (texto) 
# correo (texto)
# telefono (texto) 
# activa (booleano)

#4. Identificos los datos o el dato que sea un selector de una lista de opciones.
SECTORES = ["TECNOLOGIA", "SALUD", "FINANZAS", "EDUCACION", "LOGISTICA"]
TIPOS_EMPRESAS = ["SAS", "LTDA", "SA"]

#5. Defino mi DATASET de 300 filas simuladas.
FILAS = 300

#6. Construyo una funcion que genere los n datos pedidos (LIMPIOS).
def generar_datos_empresas(numero_datos = FILAS):
    empresas = []
    for _ in range(numero_datos):
        empresas.append({
            "id": str(fake.uuid4()),
            "nombre": f"{fake.company()} {random.choice(TIPOS_EMPRESAS)}",
            "nit": str(fake.unique.random_number(digits = 10, fix_len = True)),
            "sector": random.choice(SECTORES),
            "contacto": fake.name(),
            "correo": fake.email(),
            "telefono": fake.phone_number(),
            "activa": random.choice([True, False])
        })
    return empresas

tabla_empresas = pd.DataFrame(generar_datos_empresas())

# Ensuciar los datos

#1. Crear una funcion para definir porcentajes de error

def generar_muestra (datos, porcentaje):
    return datos.sample(frac = porcentaje, random_state = random.randint(0, 999)).index

#2. Crear una funcion para escribir mal un texto

def escribir_mal(texto):
    variantes = [texto.lower(), f" {texto.title()} ", texto.capitalize(), ]
    return random.choice(variantes)

#3. Crear una funcion para convetir booleanos en textos

def convertir_booleano_texto(valor):
    if valor:
        return random.choice(["SI", "1"])
    return random.choice(["NO", "0"])

#4. Funcion para ensuciar los datos

def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # Nombre: 10% con espacios sobrantes al inicio y al final; 15% en MAYUSCULAS. OK
    # NIT: la mitad con puntos y guiones (900.123.456-7) y la otra mitad sin nada (9001234567). OK
    # Sector: variantes del mismo sector: 'Logistica', 'LOGISTICA', ' logistica. OK
    # Contacto: 8% en None (nulos). OK
    # Correo: 6% sin la arroba (correo invalido). ok
    # Telefono: tres formatos mezclados: '3001234567', '300 123 4567', '+57 300-123-4567'. OK
    # Activa: a veces como texto: 'SI', 'NO', '1', '0'. OK
    # 5% de las filas repetidas tal cual (duplicados exactos). OK
    # 3% de los `nit` repetidos entre empresas distintas (el NIT deberia ser unico). OK


    # Nombre: 10% con espacios sobrantes al inicio y al final; 15% en MAYUSCULAS.
    
    filas_elegidas = generar_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "nombre"] = " " + datos_df.loc[filas_elegidas, "nombre"] + " " 
    
    filas_elegidas = generar_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.loc[filas_elegidas, "nombre"].str.upper()

    # NIT: la mitad con puntos y guiones (900.123.456-7) y la otra mitad sin nada (9001234567).

    def formatear_nit(nit):
        return f"{nit[:3]}.{nit[3:6]}.{nit[6:9]}-{nit[9]}"

    filas_elegidas = generar_muestra(datos_df, 0.50)
    datos_df.loc[filas_elegidas, "nit"] = ( datos_df.loc[filas_elegidas, "nit"].map(formatear_nit))

    # filas_elegidas = generar_muestra(datos_df, 0.50)
    # datos_df.loc[filas_elegidas, "nit"] = (datos_df.loc[filas_elegidas, "nit"].str.replace(r"(\d{3})(\d{3})(\d{3})(\d)", r"\1.\2.\3-\4", regex=True))

    # Sector: variantes del mismo sector: 'Logistica', 'LOGISTICA', ' logistica.

    filas_elegidas = generar_muestra(datos_df, 0.07)
    datos_df.loc[filas_elegidas, "sector"] = datos_df.loc[filas_elegidas, "sector"].map(escribir_mal)

    # Contacto: 8% en None (nulos).

    filas_elegidas = generar_muestra(datos_df, 0.08)
    datos_df.loc[filas_elegidas, "contacto"] = None

    # Correo: 6% sin la arroba (correo invalido).

    filas_elegidas = generar_muestra(datos_df, 0.06)
    datos_df.loc[filas_elegidas, "correo"] = datos_df.loc[filas_elegidas, "correo"].str.replace("@", "", regex = False)

    # Telefono: tres formatos mezclados: '3001234567', '300 123 4567', '+57 300-123-4567'.

    def formatear_telefono(telefono):
        return random.choice([
        telefono,
        f"{telefono[:3]} {telefono[3:6]} {telefono[6:]}",
        f"+57 {telefono[:3]}-{telefono[3:6]}-{telefono[6:]}"
    ])

    filas_elegidas = generar_muestra(datos_df, 0.30)
    datos_df.loc[filas_elegidas, "telefono"] = datos_df.loc[filas_elegidas, "telefono"].map(formatear_telefono)

    # Activa: a veces como texto: 'SI', 'No', '1', '0'.

    filas_elegidas = generar_muestra (datos_df, 0.3)
    datos_df["activa"] = datos_df["activa"].astype(object)
    datos_df.loc[filas_elegidas, "activa"] = datos_df.loc[filas_elegidas, "activa"].map(convertir_booleano_texto)

    # 5% de las filas repetidas tal cual (duplicados exactos).

    filas_elegidas = generar_muestra(datos_df, 0.05)
    datos_df = pd.concat([
        datos_df, 
        datos_df.loc[filas_elegidas]
    ])

    # 3% de los `nit` repetidos entre empresas distintas (el NIT deberia ser unico).

    filas_elegidas = generar_muestra(datos_df, 0.03)
    nit_repetido = datos_df.loc[filas_elegidas[0], "nit"]
    datos_df.loc[filas_elegidas, "nit"] = nit_repetido

    # Retornar datos ensuciados

    return datos_df

if __name__ == "__main__":

    tabla_empresas = ensuciar(tabla_empresas)

    print("Primeras filas:")
    print(tabla_empresas.head())

    print("\nDimensiones:")
    print(tabla_empresas.shape)

    print("\nValores nulos:")
    print(tabla_empresas.isna().sum())

    tabla_empresas.to_csv("empresas_sucias.csv", index=False)