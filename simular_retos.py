#El elemento central: la necesidad que publica la empresa. Crea el script `src/simular_retos.py`. Con la libreria **Faker** genera 500 filas falsas de la tabla `retos`, con las MISMAS columnas que usa Backend II. Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

#Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.

import random
import uuid
from faker import Faker

#1. configirar el Faker a la region que necesito
fake=Faker("es_CO")

#2. Sembrar semillas para tener coherencia en los datos simulados
Faker.seed(42)
random.seed(42)

#3. Identifico los datos que debo simular

#id (texto (UUID))
#nombre (texto)
#descripcion (texto)
#fecha_inicio (fecha)
#fecha_fin (fecha)
#estado (texto*SELECTOR)
#id_empresa (texto (UUID))
#id_categoria (texto (UUID))
#id_prioridad (texto (UUID))

#4. Identifico los datos que sean un selector
ESTADO=["ACTIVO","INACTIVO"]

#5.Defino mi DATASET
FILAS=500

#6. Construyo una funcion para generar los N datos pedidos (LIMPIOS)
def generar_datos_limpios(numero_datos=FILAS):
    filas=[]
    for _ in range(numero_datos):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.sentence(nb_words=4),
            "descripcion": fake.text(),
            "fecha_inicio": fake.date_this_month(),
            "estado": random.choice(ESTADO),
            "id_empresa": str(uuid.uuid4()),
            "id_categoria": str(uuid.uuid4()),
            "id_prioridad": str(uuid.uuid4())
        })
    return filas