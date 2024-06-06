# Sistema de Seguimiento de Clases en el Aula

## Descripción del Proyecto

Este proyecto tiene como objetivo la creación de un asistente en clase que atienda a órdenes indicadas por el profesor durante el desarrollo de las clases. El sistema se implementará sobre una Raspberry Pi, conectada a una cámara con dos ejes de movimiento, y utilizando contenedores Docker para su estructura. A continuación se detallan las características principales del proyecto:

1. **Raspberry Pi y Cámara**:
    - Conectar una cámara con dos ejes de movimiento a una Raspberry Pi.
    - Crear toda la estructura a través de contenedores Docker.

2. **Control de Voz Offline**:
    - Instalar un sistema de control de voz offline para recibir órdenes.

3. **Integración con ChatGPT y Gemini**:
    - Preparar llamadas a ChatGPT y Gemini en caso de que la orden no sea reconocida por el sistema de control de voz.

4. **Detección de Pizarras y Superficies de Proyección**:
    - Implementar un sistema para que la cámara sea capaz de buscar pizarras o superficies de proyección en el aula.

5. **Lectura de Texto en Pizarras**:
    - Configurar la cámara para que sea capaz de leer texto de las pizarras.

6. **Órdenes a través de Scripts**:
    - Preparar scripts que permitan las siguientes acciones:
        - Al iniciar una clase se podrán realizar grabaciones, fotografías, etc., todo deberá quedar registrado con su sello de tiempo.
        - Cuando termine la clase, los alumnos podrán acceder a través de un servidor web a la clase completa.

### Ejemplo de Secuencia de Eventos
1. **8:15** - Inicio de clase.
2. **8:35** - Fotografía.
3. **8:36** - Texto de fotografía.
4. **10:15** - Video.
5. **10:25** - Fin de video.
6. **10:30** - Fotografía.
7. **10:40** - Fin de clase.

7. **Control a través de Módulos en Contenedores**:
    - Preparar el dispositivo para que pueda ser controlado a través de módulos instalados en diferentes contenedores.

8. **Sistemas de Autenticación**:
    - Implementar los sistemas de autenticación necesarios.

9. **Registro de Logs**:
    - Mantener un registro de logs para todas las actividades realizadas.

## Introducción

El asistente atenderá las siguientes órdenes:

- Tomar fotos de la pizarra.
- Iniciar y detener la grabación de video.
- La cámara se girará, pudiendo apuntar a varios objetivos.
- Los recursos generados estarán en un recurso compartido accesible al alumno.
- Extraer texto de una fotografía.

Para ello, nos serviremos de un sistema de reconocimiento por voz que tendrá una palabra de activación para poder despertar y así recibir una orden.

## Autores

- Álvaro Pérez Campos
- Carlos Melero Hurtado
- Antonio Jesús Martín Rodríguez
