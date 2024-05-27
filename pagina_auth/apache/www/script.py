import docker

client = docker.from_env()

def create_directory_on_host():
    # Ejecutar 'mkdir -p /host/new_directory' en la máquina host
    result = client.containers.run(
        "alpine",
        "touch /host/home/usuario/hola2",
        volumes={
            '/': {'bind': '/host', 'mode': 'rw'}
        },
        remove=True
    )
    return "Fichero creado"

if __name__ == "__main__":
    print(create_directory_on_host())
