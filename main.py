"""
Ver ram del servidor
"""

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Created by M20191
import requests
import time
import subprocess
import json

from plugins.default import plugins_list

class Main:

	def __init__(self):
		option = int(input("[1]Download server\n[2]Change RAM\n[3]Start server\n[4]Entry server\n[5]Close server\n[6]Server info\n[7]Plugins\n..."))
		
		if option == 1:
			self.install_jars()
		
		elif option == 2:
			self.ram_eula()
		
		elif option == 3:
			self.start_server()
		
		elif option == 4: 
			self.entry_server()
		
		elif option == 5:
			self.close_server()
		
		elif option == 6:
			self.server_info()

		elif option == 7:
			self.plugins()


		else:
			return False


	# Download and Install jars/forks
	def install_jars(self):
		# Diccionary of jars/forks available
		jars = {1:"paper",2:"purpur",3:"spigot"}

		for _id,name in jars.items():
			print(f"[{_id}] {name}")

		# Input of jar/fork and version 
		jar = int(input("Jar: "))
		version = input("Version (example 1.19.1): ")

		# Download with url resp requests
		try:
			url = f"https://api-msd-z.matiasing.repl.co/{jars[jar]}/{version}"
			resp = requests.get(url)
			subprocess.call(f"wget -t 100 -O {jars[jar]}.jar {resp.json()['link']} ",shell=True)
			

			dic = {"name":f"{jars[jar]}","version":f"{version}"}
			json.dump(dic, open("msd.json","w"))
			

			self.ram_eula()
			
		except:
			print("Error 404 or 500, check the jar and version")


	# Ram and eula configurations
	def ram_eula(self):
		ram = int(input(f"GB of RAM in your server: "))
		eula = input("You accept MC EULA [Y/N]: ").upper()

		if eula == "Y":
			with open("eula.txt","w") as w:
				w.write("eula=true")
			try:
				with open('msd.json',"r") as file:
					contents = json.load(file)
					contents["ram"] = ram
					json.dump(contents, open("msd.json","w"))

				with open("iniciar.sh","w") as w:
					w.write(f"java -Xmx{ram}G -Xms{ram}G -jar {contents['name']}.jar")

			except:
				print("Download and install the server to be able to use this utility")

		else:
			return False


	# Start your server in a linux screen
	def start_server(self):
		print(f"Start server")
		subprocess.call("screen -S server sh iniciar.sh", shell=True)

	# Look your server console
	def entry_server(self):
		subprocess.call("screen -r server",shell=True)

	# Close your server, isn´t correct form
	def close_server(self):
		print(f"This option is valid only for servers with errors or impossible to close with a bug, \nusing it can cause damage, enter the server console and type the 'stop' command your.\nCTRL+C To cancel")
		time.sleep(5)
		subprocess.call("screen -S -X server quit",shell=True)


	# Plugins for script
	def plugins(self):
		plugins_list()


if __name__ == "__main__":
	while True:
		msd = Main()
