#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import subprocess
import time
import os

# Acepta EULA y configura la RAM
def eula_ram_sh():
    ram = int(input("Ram: "))
    eula = input("Aceptas el EULAMC [Y/N]:").upper()

    if eula == "Y":
        eula = "True"
        open("eula.txt","w").write("eula=true")

        # Extraemos informacion del information.json para realizar la instalacion
        with open("information.json","r") as read:
            information = json.load(read)
            information["ram"] = ram
            information["eula"] = eula
            json.dump(information,open("information.json","w"))

        open("iniciar.sh","w").write(f"java -Xmx{ram}G -Xms{ram}G -jar {information['jar']}.jar")




# Descargar servidor
def download_server():
    versions_get = requests.get("http://localhost:5000/versions")
    # Seleciona tu fork/jar para descargar
    print("Selecciona tu version a descargar")
    for jars_forks in versions_get.json().keys():
        print(f"- {jars_forks}")

    jar_fork = input("Jar/Fork: ")

    # Recursividad para verificar nombre
    if jar_fork in versions_get.json().keys():
        for versions_jar in versions_get.json()[jar_fork]:
            print(versions_jar,end=" | ")
        

        version_jar_fork = input("\nVersion: ")
        
        url = requests.get(f"http://localhost:5000/{jar_fork}/{version_jar_fork}")
        subprocess.call(f"wget -t 100 -O {jar_fork}.jar {url.json()['link']}",shell=True)

        # Sube un archivo log para extraer informacion posteriormente
        log = {"jar":jar_fork,"version":version_jar_fork}
        json.dump(log,open("information.json","w"))
        
    else:
        print("Version erronea")
        download_server()



# Importa configuraciones del json para crear un nuevo server
def import_server():
    json_name = input("Nombre del JSON para importar (sin .json): ")
    print(f"JSON: {json_name}.json")

    with open(f"{json_name}.json","r") as read:
        json_file = json.load(read)
        
        jar = json_file["jar"]
        version = json_file["version"]

    resp = requests.get(f"http://localhost:5000/{jar}/{version}")
    url = resp.json()["link"]
    subprocess.call(f"wget -t 100 -O {jar}.jar {url}",shell=True)


# Inicia tu servidor mientante el jar
def start_server():
	print("Iniciando server")
	subprocess.call("screen -S server sh iniciar.sh", shell=True)

# Entra en tu servidor
def entry_server():
	subprocess.call("screen -r server",shell=True)

# Cierra tu servidor de una manera forzada
def close_server():
	print("Cerrar el servidor bruscamente, esto puede generar problemas... CTRL+C para salir")
	time.sleep(5)
	subprocess.call("screen -S -X server quit",shell=True)



# - - - - - - 
"""
BETA
def script():
    # Obtiene la carpeta de los scripts (Los envuelve en una lista)
    path_scripts = f"{os.getcwd()}/scripts"
    # Recorre la lista de directorios
    for script in os.listdir(path_scripts):
        print(f"[{os.listdir(path_scripts).index(script)}] {script}")
    
    # Seleccionas el script
    script_to_run = int(input("Script: "))
    # Se ejecuta el script
    exec(open(f"{path_scripts}/{os.listdir(path_scripts)[script_to_run]}").read(), globals())
    
"""






