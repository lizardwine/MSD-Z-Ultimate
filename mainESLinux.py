#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import subprocess
import time

def extract_json(file : str) -> object:
	"""
	Returns a JSON object in which we can extract information from the downloaded server.\n
	Args:\n
		* file (str): JSON file

	Returns:\n
		* json_file: returns a JSON object to which information is extracted 
	"""

	with open(f"{file}","r") as read:
		json_file = json.load(read)
		return json_file

def eula_ram_sh():
	"""
	* Requests RAM value
	* Accepts the EULAMC
	* Generate the start.sh
	"""

	ram = int(input("Ram: "))
	eula = input("Aceptas el EULAMC [Y/N]:").upper()

	if eula == "Y":
		eula = "true"
		open("eula.txt","w").write("eula=true")

		information = extract_json("information.json")
		information["ram"] = ram
		information["eula"] = eula
		
		json.dump(information,open("information.json","w"))

		open("iniciar.sh","w").write(f"java -Xmx{ram}G -Xms{ram}G -jar {information['jar']}.jar")

def download_server():
	"""
	Download and install the jar/fork
	* List jars/forks/versions with the API (https://api-msd-z.matiasing.repl.co/versions)
	* Download the jar/fork
	* Store relevant information in information.json
		* Name (Name of server)
		* Jar (Jar installed)
		* Version (Version installed)
	"""

	# List of available API versions
	versions_get = requests.get("https://api-msd-z.matiasing.repl.co/versions")
	print("Selecciona tu version a descargar")
	for jars_forks in versions_get.json().keys():
		print(f"- {jars_forks}")

	jar_fork = input("Jar/Fork: ")

	# Validates if the selected version exists, otherwise re-executes the function
	if jar_fork in versions_get.json().keys():
		
		# List available versions of the selected jar/fork 
		for versions_jar in versions_get.json()[jar_fork]:
			print(versions_jar,end=" | ")
		
		version_jar_fork = input("\nVersion: ")
		
		# Using the API extracts the link to the selected version/fork/jar, then proceeds to install it using a wget
		url = requests.get(f"https://api-msd-z.matiasing.repl.co/{jar_fork}/{version_jar_fork}")
		subprocess.call(f"wget -t 100 -O {jar_fork}.jar {url.json()['link']}",shell=True)

		name = input("Asignar nombre al servidor (sin espacios): ")
		
		# Dump log to information.json
		log = {"name":name,"jar":jar_fork,"version":version_jar_fork}
		json.dump(log,open("information.json","w"))
		
		eula_ram_sh()
	
	# re-execute
	else:print("Version erronea");download_server()

def import_server():
	"""
	Extract information from a JSON setup file to automate the entire download and installation of the server.
	"""

	json_name = input("Nombre del JSON para importar (sin .json): ")
	print(f"JSON: {json_name}.json")

	# Extrac information
	information = extract_json(f"{json_name}.json")
	jar = information["jar"]
	version = information["version"]
	ram = information["ram"]
	
	# Get link and download
	resp = requests.get(f"https://api-msd-z.matiasing.repl.co/{jar}/{version}")
	url = resp.json()["link"]
	subprocess.call(f"wget -t 100 -O {jar}.jar {url}",shell=True)
	
	# Accepts the EULAMC
	open("eula.txt","w").write("eula=true")

	# Write start.sh file to setup server
	open("iniciar.sh","w").write(f"java -Xmx{ram}G -Xms{ram}G -jar {jar['jar']}.jar")

def create_setup_server():
	"""
	Creates a setup file to automate downloads and server installations
	"""
	
	# Request data
	name_setup = input("Nombre archivo [sin espacios]: ")
	name_server = input("Nombre del servidor [sin espacios]: ")
	jar_fork = input("Jar/Fork: ")
	version = input("Versions: ")
	ram = int(input("Ram del servidor: "))

	# Save the data in JSON setup file
	log = {"name":name_server,"jar":jar_fork,"version":version,"ram":ram,"eula":"true"}
	json.dump(log,open(f"{name_setup}","w"))

def start_server():
	"""
	Start server from start.sh with the server name (line 77)\n
	`screen -S {name} sh iniciar.sh
	"""

	print("Iniciando server")
	information = extract_json("information.json")
	name = information["name"]
	subprocess.call(f"screen -S {name} sh iniciar.sh", shell=True)

def entry_server():
	"""
	Entry server with the server name (line 77)
	"""
	information = extract_json("information.json")
	name = information["name"]
	subprocess.call(f"screen -r {name}",shell=True)

def close_server():
	"""
	Close the server with the own name\n
	`screen -S {name} p 0 -X stuff "stop^M
	"""
	print("Cerrando el servidor...")
	time.sleep(5)

	information = extract_json("information.json")
	name = information["name"]
	subprocess.call(f'screen -S {name} p 0 -X stuff "stop^M"',shell=True)
	print("Servidor cerrado con exito")

def brute_close_server():
	"""
	Close your server using brute forse\n
	`screen -S {name} -X quit
	"""
	print("No se recomienda cerrarlo de esta forma podria causar problemas... CTRL+C Para salir")
	time.sleep(5)
	
	information = extract_json("information.json")
	name = information["name"]
	subprocess.call(f"screen -S {name} -X quit",shell=True)

def delete_server():
	"""
	Remove all files from your path server\n
	`ls | grep -v *.py | xargs rm -fr
	"""
	print("Estas por borrar todos los archivos del servidor CTRL+C Para salir")
	time.sleep(5)
	
	subprocess.call("ls | grep -v *.py | xargs rm -fr",shell=True)
	print("Servidor borrado con exito")

# Core
if __name__ == "__main__":
	while True:
		option = int(input("""
		[1] Descargar Servidor
		[2] Iniciar Servidor
		[3]	Importar Servidor
		[4] Crear setup
		[5] Detener Servidor
		[6] Forzar Detencion
		[7] Modificar RAM
		[8] Borrar Server
		... 
		"""))

		# Main
		if option == 1:download_server()
		elif option == 2:start_server()
		elif option == 3:import_server()
		elif option == 4:create_setup_server()
		elif option == 5:close_server()
		elif option == 6:brute_close_server()
		elif option == 7:eula_ram_sh()
		elif option == 9:delete_server()
		else:print("Exit")