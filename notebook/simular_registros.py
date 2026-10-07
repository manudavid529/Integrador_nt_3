import random
import uuid
import pandas as pd
from faker import Faker

fake = Faker("es_CO")
Faker.seed(42)
random.seed(42)

# ---------- Constantes ----------
ESTADOS = ["INSCRITO", "EN PROCESO", "FINALIZADO"]

# UUID generados con la semilla fija, para que los ids de usuario/reto sean reproducibles
IDS_USUARIO = [str(uuid.UUID(int=random.getrandbits(128), version=4)) for _ in range(50)]
IDS_RETO = [str(uuid.UUID(int=random.getrandbits(128), version=4)) for _ in range(20)]

FILAS = 800


# ---------- Datos limpios ----------
def generar_datos_limpios(n):
    filas = []
    for _ in range(n):
        filas.append({
            "id": str(uuid.uuid4()),
            "fecha_registro": fake.date_time_between(start_date="-1y", end_date="now"),
            "observacion": fake.sentence(nb_words=10),
            "estado": random.choice(ESTADOS),
            "id_usuario": random.choice(IDS_USUARIO),
            "id_reto": random.choice(IDS_RETO),
        })
    return filas


# ---------- Utilidades para ensuciar ----------
def generar_muestra(datos, porcentaje):
    """Devuelve los índices de una muestra aleatoria (reproducible por la semilla)."""
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 999)).index


def escribir_mal(texto):
    variantes = [texto.lower(), f" {texto.title()} ", texto.upper()]
    return random.choice(variantes)


def formatear_fecha_mezclada(fecha):
    if random.random() < 0.5:
        return fecha.strftime("%Y-%m-%d %H:%M:%S")   # 2026-03-15 14:30:00
    return fecha.strftime("%d/%m/%Y %H:%M")          # 15/03/2026 14:30


# ---------- Función principal ----------
def generar_registros(n=FILAS):
    df = pd.DataFrame(generar_datos_limpios(n))

    # 1) 10% con el par id_usuario + id_reto repetido (copiado de otra fila)
    idx_repetidos = generar_muestra(df, 0.10)
    candidatos = df.index.difference(idx_repetidos)
    for i in idx_repetidos:
        origen = random.choice(list(candidatos))
        df.loc[i, "id_usuario"] = df.loc[origen, "id_usuario"]
        df.loc[i, "id_reto"] = df.loc[origen, "id_reto"]

    # 2) observacion: 20% nulos
    df["observacion"] = df["observacion"].astype(object)
    df.loc[generar_muestra(df, 0.20), "observacion"] = None

    # 3) estado: variantes sucias ('inscrito', 'EN PROCESO', ' Finalizado ')
    idx_estado = generar_muestra(df, 0.30)
    df.loc[idx_estado, "estado"] = df.loc[idx_estado, "estado"].apply(escribir_mal)

    # 4) fecha_registro: dos formatos mezclados
    df["fecha_registro"] = df["fecha_registro"].apply(formatear_fecha_mezclada)

    # 5) 5% de filas duplicadas tal cual (se hace al final para que sean copias exactas)
    duplicados = df.loc[generar_muestra(df, 0.05)]
    df = pd.concat([df, duplicados], ignore_index=True)

    return df


if __name__ == "__main__":
    df = generar_registros()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())