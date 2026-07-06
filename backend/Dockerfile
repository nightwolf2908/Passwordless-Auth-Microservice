# Usamos una versión ligera de Python
FROM python:3.11-slim

# Definimos la carpeta de trabajo dentro del contenedor
WORKDIR /code

# Copiamos la lista de librerías e instalamos todo
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiamos todo el código de nuestra app
COPY ./app /code/app

# Comando para arrancar el servidor de Python
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]