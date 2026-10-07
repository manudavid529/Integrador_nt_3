import random
import pandas as pd
import uuid
from faker import Faker
from datetime import timedelta

# 1. Configuración de semillas para reproducibilidad
fake = Faker("es_CO")
Faker.seed(42)
random.seed(42)

# 2. Declaración de Constantes (Listas fijas de foráneas)
ESTADOS = ["En curso", "Cerrado", "Abierto", "Cancelado"]
IDS_EMPRESA = [str(uuid.uuid4()) for _ in range(10)]
IDS_CATEGORIA = [str(uuid.uuid4()) for _ in range(5)]
IDS_PRIORIDAD = [str(uuid.uuid4()) for _ in range(3)]

def generar_muestra(datos, porcentaje):
    """Devuelve los índices de una muestra aleatoria del DataFrame"""
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index

def ensuciar_estado(estado):
    """Genera variantes sucias para la columna estado"""
    variantes = [
        estado.lower(),                  # minúsculas
        estado.upper(),                  # MAYÚSCULAS
        f" {estado} ",                   # espacios sobrantes
        estado.lower().replace(" ", "_") # formato con guion bajo
    ]
    return random.choice(variantes)

def generar_retos(n=500):
    filas = []
    
    # ==========================================
    # 1. Generación de datos limpios
    # ==========================================
    for _ in range(n):
        f_inicio = fake.date_between(start_date="-1y", end_date="+3m")
        f_fin = f_inicio + timedelta(days=random.randint(15, 180))
        
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.sentence(nb_words=6).rstrip("."),
            "descripcion": fake.sentence(nb_words=12),
            "fecha_inicio": f_inicio,
            "fecha_fin": f_fin,
            "estado": random.choice(ESTADOS),
            "id_empresa": random.choice(IDS_EMPRESA),
            "id_categoria": random.choice(IDS_CATEGORIA),
            "id_prioridad": random.choice(IDS_PRIORIDAD)
        })

    df = pd.DataFrame(filas)

    # ==========================================
    # 2. Ensuciar los datos (Errores a propósito)
    # ==========================================
    
    # a. Nombre: 10% con espacios sobrantes
    idx = generar_muestra(df, 0.10)
    df.loc[idx, "nombre"] = "  " + df.loc[idx, "nombre"] + "  "

    # b. Descripción: 12% en None (nulos)
    idx = generar_muestra(df, 0.12)
    df.loc[idx, "descripcion"] = None

    # c. Fecha_inicio: dos formatos mezclados (2026-03-02 y 02/03/2026)
    # Primero las convertimos a datetime por seguridad, luego extraemos strings mixtos
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"])
    iso = df["fecha_inicio"].dt.strftime("%Y-%m-%d")
    latino = df["fecha_inicio"].dt.strftime("%d/%m/%Y")
    
    df["fecha_inicio"] = iso  # Base estándar
    idx_latino = generar_muestra(df, 0.40) # 40% en formato latino
    df.loc[idx_latino, "fecha_inicio"] = latino.loc[idx_latino]

    # d. Fecha_fin: 8% en None y 5% ANTERIOR a fecha_inicio (Error lógico)
    # Aseguramos formato datetime para poder hacer la resta lógica
    df["fecha_fin"] = pd.to_datetime(df["fecha_fin"])
    
    # 5% Anterior a la fecha de inicio
    idx_anterior = generar_muestra(df, 0.05)
    # Convertimos la fecha inicio temporalmente para calcular el error
    f_inicio_temp = pd.to_datetime(df.loc[idx_anterior, "fecha_inicio"], format="mixed", dayfirst=True)
    # Le restamos un random de días
    df.loc[idx_anterior, "fecha_fin"] = f_inicio_temp - pd.Timedelta(days=random.randint(10, 30))
    
    # Convertimos fecha_fin a texto para que reciba correctamente el None sin volverlo NaT
    df["fecha_fin"] = df["fecha_fin"].dt.strftime("%Y-%m-%d")
    
    # 8% nulos
    idx_none = generar_muestra(df, 0.08)
    df.loc[idx_none, "fecha_fin"] = None

    # e. Estado: variantes de escritura ('en_curso', 'EN CURSO', ' Cerrado ')
    idx_estado = generar_muestra(df, 0.30) # Ensuciamos un 30% de los estados
    df.loc[idx_estado, "estado"] = df.loc[idx_estado, "estado"].apply(ensuciar_estado)

    # f. 5% de las filas repetidas tal cual (duplicados exactos)
    idx_duplicados = generar_muestra(df, 0.05)
    duplicados = df.loc[idx_duplicados].copy()
    # Se añade al dataframe (creando 25 filas extras, quedando 525 en total)
    df = pd.concat([df, duplicados], ignore_index=True)

    # Revolvemos los datos (shuffle) para que los duplicados y errores no queden juntos
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    return df

if __name__ == "__main__":
    df_retos = generar_retos(500)
    
    print(f"Dimensiones del dataset: {df_retos.shape}\n")
    print("Primeras 5 filas:")
    print(df_retos.head(), "\n")
    print("Conteo de nulos por columna:")
    print(df_retos.isna().sum())