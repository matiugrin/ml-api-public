# -*- coding: utf-8 -*-
import redis
# import settings
import json
from uuid import uuid4
import time

########################################################################
# COMPLETAR AQUI: Crear conexion a redis y asignarla a la variable "db".
########################################################################
db = redis.Redis(host='redis', port=6379, db=0)
########################################################################


def model_predict(text_data):
    """
    Esta función recibe sentencias para analizar desde nuestra API,
    las encola en Redis y luego queda esperando hasta recibir los
    resultados, qué son entonces devueltos a la API.

    Attributes
    ----------
    text_data : str
        Sentencia para analizar.

    Returns
    -------
    prediction : str
        Sentimiento de la oración. Puede ser uno de: "Positivo",
        "Neutral" o "Negativo".
    score : float
        Valor entre 0 y 1 que especifica el grado de positividad
        de la oración.
    """
    prediction = None
    score = None

    #################################################################
    # COMPLETAR AQUI: Crearemos una tarea para enviar a procesar.
    # Una tarea esta definida como un diccionario con dos entradas:
    #     - "id": será un hash aleatorio generado con uuid4 o
    #       similar, deberá ser de tipo string.
    #     - "text": texto que se quiere procesar, deberá ser de tipo
    #       string.
    # Luego utilice rpush de Redis para encolar la tarea.
    #################################################################
    
    job_id = str(uuid4())

    # paquete a enviar a traves de la cola de mensajes
    job_data = {
        'id': job_id,
        'text': text_data
    }

    #################################################################

    # lo mandamos a redis
    db.rpush('service_queue', json.dumps(job_data))

    # Iterar hasta recibir el resultado (del modelo)
    while True:
        #################################################################
        # COMPLETAR AQUI: En cada iteración tenemos que:
        #     1. Intentar obtener resultados desde Redis utilizando
        #        como key nuestro "job_id".
        #     2. Si no obtuvimos respuesta, dormir el proceso algunos
        #        milisegundos.
        #     3. Si obtuvimos respuesta, extraiga la predicción y el
        #        score para ser devueltos como salida de esta función.
        #################################################################
        
        response = db.get(job_id)
        if response is not None:
            
            response = json.loads(response.decode('utf-8'))
            prediction = response['prediction']
            score = response['score']

            db.delete(job_id)
            break

        time.sleep(1)

        #################################################################

    print(json.dumps({
        "text":text_data,
        "prediction": prediction,
        "score": score
    }))

    return prediction, score
