# Usar una imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt en el directorio de trabajo
COPY requirements.txt requirements.txt

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el contenido de la aplicación en el directorio de trabajo
COPY . .

# Exponer el puerto que la aplicación usará (si es necesario)
EXPOSE 5678

# Comando por defecto para ejecutar la aplicación
CMD ["python", "app.py"]
