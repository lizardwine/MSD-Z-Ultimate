#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import subprocess
import time


# Extraccion de datos del information.json
def extract_json(file):
	with open(f"{file}","r") as read:
		json_file = json.load(read)
		return json_file

# Acepta EULA y configura la RAM
def eula_ram_sh():
	ram = int(input("Ram: "))
	eula = input("Aceptas el EULAMC [Y/N]:").upper()

	if eula == "Y":
		eula = "true"
		open("eula.txt","w").write("eula=true")

		# Extraemos informacion del information.json para realizar la instalacion
		information = extract_json("information.json")
		information["ram"] = ram
		information["eula"] = eula
		
		json.dump(information,open("information.json","w"))

		open("iniciar.sh","w").write(f"java -Xmx{ram}G -Xms{ram}G -jar {information['jar']}.jar")


# Descargar servidor
def download_server():
	versions_get = requests.get("https://api-msd-z.matiasing.repl.co/versions")
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
		
		url = requests.get(f"https://api-msd-z.matiasing.repl.co/{jar_fork}/{version_jar_fork}")
		subprocess.call(f"wget -t 100 -O {jar_fork}.jar {url.json()['link']}",shell=True)

		# Nombre del servidor, identificarlo para ADM-SHELL
		name = input("Asignar nombre al servidor (sin espacios): ")
		# Sube un archivo log para extraer informacion posteriormente
		log = {"name":name,"jar":jar_fork,"version":version_jar_fork}
		json.dump(log,open("information.json","w"))
		
		eula_ram_sh()


	else:
		print("Version erronea")
		download_server()



# Importa configuraciones del json para crear un nuevo server
def import_server():
	json_name = input("Nombre del JSON para importar (sin .json): ")
	print(f"JSON: {json_name}.json")

	information = extract_json("information.json")
	jar = information["jar"]
	version = information["version"]
	ram = information["ram"]

	resp = requests.get(f"https://api-msd-z.matiasing.repl.co/{jar}/{version}")
	url = resp.json()["link"]
	subprocess.call(f"wget -t 100 -O {jar}.jar {url}",shell=True)
	
	# Eula true
	open("eula.txt","w").write("eula=true")

	# Escribe el sh para iniciar el servidor
	open("iniciar.sh","w").write(f"java -Xmx{ram}G -Xms{ram}G -jar {jar['jar']}.jar")

# Inicia tu servidor mientante el jar
def start_server():
	print("Iniciando server")
	information = extract_json("information.json")
	name = information["name"]

	subprocess.call(f"screen -S {name} sh iniciar.sh", shell=True)

# Entra en tu servidor
def entry_server():
	information = extract_json("information.json")
	name = information["name"]

	subprocess.call(f"screen -r {name}",shell=True)

# Cierra tu servidor como corresponde
def close_server():
	print("Cerrando el servidor...")
	time.sleep(5)
	information = extract_json("information.json")
	name = information["name"]
	
	subprocess.call(f'screen -S {name} p 0 -X stuff "stop^M"',shell=True)
	print("Servidor cerrado con exito")


# Cierra tu servidor de forma brusca
def brute_close_server():
	print("No se recomienda cerrarlo de esta forma podria causar problemas... CTRL+C Para salir")
	time.sleep(5)
	information = extract_json("information.json")
	name = information["name"]	
	subprocess.call(f"screen -S {name} -X quit",shell=True)

# Desinstala servidor
def delete_server():
	print("Estas por borrar todos los archivos del servidor CTRL+C Para salir")
	time.sleep(5)
	subprocess.call("ls | grep -v *.py | xargs rm -fr",shell=True)
	print("Servidor borrado con exito")

if __name__ == "__main__":
	while True:
		option = int(input("""
		[1] Descargar Servidor
		[2] Iniciar Servidor
		[3]	Importar Servidor
		[4] Detener Servidor
		[5] Forzar Detencion
		[6] Modificar RAM
		[7] Borrar Server
		... 
		"""))
		if option == 1:
			download_server()
		elif option == 2:
			start_server()
		elif option == 3:
			import_server()
		elif option == 4:
			close_server()
		elif option == 5:
			brute_close_server()
		elif option == 6:
			eula_ram_sh()
		elif option == 7:
			delete_server()



