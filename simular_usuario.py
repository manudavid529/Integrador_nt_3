import random
import pandas as pd
import uuid
from faker import Faker

# 1. Configurar Faker a la región requerida
fake = Faker("es_CO")

# 2. Sembrar semillas para coherencia en los datos simulados
Faker.seed(42)
random.seed(42)

# 3. Datos a simular
# id (texto UUID)
# nombre (texto)
# correo (texto)
# contrasena_hash (texto)
# rol (texto) -> selector
# activo (booleano)
# fecha_registro (fecha y hora)

# 4. Definir opciones válidas
ROLES = ["ADMIN", "EMPRESA", "PARTICIPANTE"]

# 5. Definir tamaño del dataset
FILAS = 400

# 6. Generar datos limpios

def generar_datos_limpios(numero_datos=FILAS):
    filas = []
    for _ in range(numero_datos):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.name(),
            "correo": fake.email(),
            "contrasena_hash": fake.sha256(),
            "rol": random.choice(ROLES),
            "activo": random.choice([True, False]),
            "fecha_registro": fake.date_time_between(start_date='-2y', end_date='now').strftime("%Y-%m-%d %H:%M:%S")
        })
    return filas

variables_noche = pd.DataFrame(generar_datos_limpios())

# 7. Función para definir muestra aleatoria de filas

def generar_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index

# 8. Función para escribir mal un texto

def escribir_mal(texto):
    variantes = [texto.lower(), f" {texto.title()} ", texto.upper(), texto.capitalize()]
    return random.choice(variantes)

# 9. Función para convertir booleanos en textos

def convertir_booleano_a_texto(valor):
    if valor:
        return random.choice(["SI", "1"])
    return random.choice(["NO", "0"])

# 10. Función para ensuciar datos

def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # Asegurar tipo datetime para fechas
    datos_df["fecha_registro"] = pd.to_datetime(datos_df["fecha_registro"])

    # nombre: 10% con espacios sobrantes, 8% mayúsculas
    filas_elegidas = generar_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "nombre"] = " " + datos_df.loc[filas_elegidas, "nombre"] + " "

    filas_elegidas = generar_muestra(datos_df, 0.08)
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.loc[filas_elegidas, "nombre"].str.upper()

    # correo: 12% en mayúsculas, 5% sin @, 4% nulos
    filas_elegidas = generar_muestra(datos_df, 0.12)
    datos_df.loc[filas_elegidas, "correo"] = datos_df.loc[filas_elegidas, "correo"].str.upper()

    filas_elegidas = generar_muestra(datos_df, 0.05)
    datos_df.loc[filas_elegidas, "correo"] = datos_df.loc[filas_elegidas, "correo"].str.replace("@", "", regex=False)

    filas_elegidas = generar_muestra(datos_df, 0.04)
    datos_df.loc[filas_elegidas, "correo"] = None

    # rol: variantes de escritura
    filas_elegidas = generar_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "rol"] = datos_df.loc[filas_elegidas, "rol"].map(escribir_mal)

    # fecha: dos formatos mezclados
    iso = datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    latino = datos_df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")
    datos_df["fecha_registro"] = iso

    filas_elegidas = generar_muestra(datos_df, 0.40)
    datos_df.loc[filas_elegidas, "fecha_registro"] = latino.loc[filas_elegidas]

    # activo: a veces llega como SI, NO, 0, 1
    filas_elegidas = generar_muestra(datos_df, 0.27)
    datos_df.loc[filas_elegidas, "activo"] = datos_df.loc[filas_elegidas, "activo"].map(convertir_booleano_a_texto)

    # duplicados exactos
    idx_duplicados = generar_muestra(datos_df, 0.05)
    duplicados = datos_df.loc[idx_duplicados].copy()
    datos_df = pd.concat([datos_df, duplicados], ignore_index=True)
    datos_df = datos_df.sample(frac=1, random_state=42).reset_index(drop=True)

    return datos_df

# Ejecución

datos_sucios = ensuciar(variables_noche)

# Verificación rápida
print(f"Total de filas: {len(datos_sucios)}")
print(f"Total de duplicados exactos: {datos_sucios.duplicated().sum()}")