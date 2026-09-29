import random
from pandas import pd
import uuid
from faker import Faker

#1. Configurar el faker a la region que necesito
fake = Faker("es_CO")

#2. Sembrar semilla para tener coherencia en los datos generados
#simulados
Faker.seed(42)
random.seed(42)

#3. Identifico los datos que debo simular
# id (texto (UUID)) 
# nombre (texto)
# correo (texto)
# contrasena_hash (texto) 
# rol (texto) elementos a seleccionar de una lista de roles
# activa (booleano)
# fecha_registro (fecha y hora)

#4. Identificos los datos o el dato que sea un selector de una lista de opciones.
ROLES = ["ADMIN", "EMPRESA", "PARTICIPANTE"]

#5. Defino mi DATASET de 400 filas simuladas
FILAS = 400

#6. Construyo una funcion que genere los n datos pedidos (LIMPIOS).
def generar_datos_limpios(numero_datos = FILAS):
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

variabes_noche =pd.DataFrame( generar_datos_limpios() )

#Ensuciar los datos