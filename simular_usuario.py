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
#estado (texto)
#id_empresa (texto (UUID))
#id_categoria (texto (UUID))
#id_prioridad (texto (UUID))

#4. Identifico los datos que sean un selector
ESTADO=[]