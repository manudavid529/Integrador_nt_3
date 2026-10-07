'''
Define el nivel de atencion del reto. Crea el script `src/simular_prioridades.py`. Con la libreria **Faker** 
genera 200 filas falsas de la tabla `prioridades`, con las MISMAS columnas que usa Backend II. Despues **ensucia
los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. 
Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea 
SIEMPRE el mismo y tu compañero pueda reproducirlo.

OJO: `dias_max_respuesta` NO esta en el modelo de Backend II: es una columna EXTRA solo para este ejercicio 
de analisis. Dejala anotada como tal en el script.

'''

import random
import uuid
from faker import Faker
import pandas as pd

#1. Configurar el faker a la region que necesite
fake=Faker("es_CO")

#2. Sembrar semillas para tener coherencia en los datos simulados y garantizar que tengamos resultados exactamente
Faker.seed(42)
random.seed(42)

#3. Identifico los datos que debo simular
#id (texto (UUID))
#nombre (texto)
#nivel (entero)
#dias_max_respuesta (entero)

#4 Identifico los datos o el dato que sea un selector y escribo las opciones
NIVELES=["ALTO", "MEDIO", "BAJO"]

#5. Defino mi DATASET
FILAS=200

#6. Construyo una funcion para generar los N datos pedidos (LIMPIOS)
def generar_datos_limpios(numero_datos=FILAS):
    filas=[]
    for _ in range(numero_datos):
        filas.append({
            "id":str(uuid.uuid4()), 
            "nombre":fake.name(),
            "nivel":random.choice(NIVELES),
            "dias_max_respuesta":random.randint(1-15)
        })
    return filas

prioridades= pd.DataFrame(generar_datos_limpios())

#Ensuciar los datos 

#1. Crear una función para definir porcentajes de error
def generar_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0,999)).index

#2. Crear una función para escribir mal un texto
def escribir_mal(texto):
    variantes=[texto.lowe(), f" {texto.title()} ", texto.capitalize()]
    return random.choice(variantes)

#3. Convertir boolenps en textos
def convertir_booleano_texto(valor):
    if valor:
        return random.choice(["SI", "1"])
    return random.choice(["NO", "0"])

#4. Funcion para ensuciaer los datos
def ensuciar(datos_df):
    datos_df=datos_df.copy()

    #nivel: a veces cono TEXTO(´3´), a veces palabra ('tres'), 7% en None
    filas_elegidas=generar_muestra(datos_df,0.1)
    datos_df.loc[filas_elegidas, "activo"]=datos_df.loc[filas_elegidas, "activo"].map(convertir_booleano_texto)=datos_df.loc[filas_elegidas, "activo"].map(convertir_booleano_texto)

    filas_elegidas=generar_muestra(datos_df,0.07)
    datos_df.loc[filas_elegidas, "nivel"]=None

    
    #Se ensucia `dias_max_respuesta`: 5% en None y 3% con un valor absurdo (999)
    
    filas_elegidas=generar_muestra(datos_df,0.05)
    datos_df.loc[filas_elegidas, "dias_max_respuesta"]=None

    filas_elegidas=generar_muestra(datos_df,0.03)
    datos_df.loc[filas_elegidas, "dias_max_respuesta"]=999

    # Historia: 8% de duplicados exactos y formatos de datos inconsistentes.
def generar_prioridades(n=200):
    datos = generar_datos_limpios(n)
    df = pd.DataFrame(datos)

    # Agregar el 8% de filas como duplicados exactos.
    cantidad_duplicados = round(len(df) * 0.08)
    duplicados = df.sample(
        n=cantidad_duplicados,
        random_state=random.randint(0, 999999)
    )
    df = pd.concat([df, duplicados], ignore_index=True)

    # Agregar nulos en nivel y en la columna extra.
    filas_nulas = generar_muestra(df, 0.07)
    df.loc[filas_nulas, "nivel"] = None

    filas_nulas = generar_muestra(df, 0.05)
    df.loc[filas_nulas, "dias_max_respuesta"] = None

    # Agregar espacios sobrantes y mayúsculas mezcladas en los textos.
    filas_nivel = generar_muestra(df, 0.15)
    df.loc[filas_nivel, "nivel"] = df.loc[filas_nivel, "nivel"].apply(
        lambda valor: escribir_mal(valor) if pd.notna(valor) else valor
    )

    filas_nombre = generar_muestra(df, 0.10)
    df.loc[filas_nombre, "nombre"] = df.loc[filas_nombre, "nombre"].apply(
        escribir_mal
    )

    # Agregar formatos distintos y un valor absurdo en la columna extra.
    filas_formato = generar_muestra(df, 0.05)
    df.loc[filas_formato, "dias_max_respuesta"] = "15 días"

    filas_absurdas = generar_muestra(df, 0.03)
    df.loc[filas_absurdas, "dias_max_respuesta"] = 999

    return df


if __name__ == "__main__":
    df = generar_prioridades(n=200)
    print(df.shape)
    print(df.head())
    print(df.isna().sum())