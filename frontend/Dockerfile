# Usamos la imagen oficial de Nginx basada en Alpine (súper ligera)
FROM nginx:alpine

# Copiamos nuestros archivos del frontend a la carpeta donde Nginx sirve la web
COPY ./index.html /usr/share/nginx/html/index.html
COPY ./app.js /usr/share/nginx/html/app.js

# Exponemos el puerto 80 estándar de servidores web
EXPOSE 80