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

class Main:

	def __init__(self):
		option = int(input("[1]Download server\n[2]Change RAM\n[3]Start server\n[4]Entry server\n[5]Close server\n[6]Server info\n..."))
		
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

			with open('msd.json',"r") as file:
				contents = json.load(file)
				contents["ram"] = ram
				json.dump(contents, open("msd.json","w"))

			with open("iniciar.sh","w") as w:
				w.write(f"java -Xmx{ram}G -Xms{ram}G -jar {contents['name']}.jar")

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




	# Optional lite version don't include

	def server_info(self):
		try:
			with open('msd.json',"r") as file:
				contents = json.load(file)

			import platform
			import datetime
			time = datetime.date.today()
			sistema = platform.system()
			version = platform.version()
			print(
			f"""
			888b     d888  .d8888b.  8888888b.   Y88-888-888-888-888-888-888-888-88Y
			8888b   d8888 d88P  Y88b 888  "Y88b  By: M20191
			88888b.d88888 Y88b.      888    888  Date: {time} 
			888Y88888P888  "Y888b.   888    888  OS: {sistema}
			888 Y888P 888     "Y88b. 888    888  OSversion: {version}  
			888  Y8P  888       "888 888    888  Python: > 3.8
			888   "   888 Y88b  d88P 888  .d88P  Minecraft Server Downloader ZUV
			888       888  "Y8888P"  8888888P"   Y88-888-888-888-888-888-888-888-88Y 
			
			Y88-888-888-SERVER-INFO-888-888-888-88Y 
			
			Name/Jar/Fork: {contents["name"]}
			Version: {contents["version"]}
			Ram: {contents["ram"]}

			Y88-888-888-888-888-888-888-888-88Y-88Y 

			""")
		except:
			print("Download and install the server to util that option")

while True:
	msd = Main()
