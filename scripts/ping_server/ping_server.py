#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by M20191

# Import modules
from mcstatus import MinecraftServer
from datetime import datetime
from typing import Any
import re

def server(server_name: str) -> dict[str, Any]:
	"""
	Returns a object in which we can extract information from server pinged.\n
	Args:\n
		* server_name (str): minecraft server IP/DNS

	Returns:\n
		* response (object): returns a object to which information is extracted
	"""
	# Ping function return 0 if server don´t response
	try:
		server_ping = MinecraftServer.lookup(server_name)
		return server_ping.status()

	except:return 0
		
def information_server():
	"""
	Main function printing server information
	"""
	# Get name of server
	server_name = input("Server name: ")
	info_server = server(server_name)

	# server error
	if info_server==0:print("Error server ping");exit()

	# Information of server
	information_server = {
		"Time to ping":datetime.now(),
		"Ip":server_name,
		"Players":info_server.players.online,
		"Max/Players":info_server.players.max,
		"Availability":info_server.players.max - info_server.players.online,
		"Latency":str(info_server.latency).split(".")[0],
		"Version/Bunge":info_server.version.name[0:15]+" "+info_server.version.name[-6:],
		"Description":re.sub('§[\da-zA-Z]', '', info_server.description),
		"Status":"Active"
	}

	# items of information_server
	for i,x in information_server.items():
		print(f'{i}: {x}')

# Core
if __name__ == '__main__':
	while True:
		option = int(input("""
		[1]Ping server
		... 
		"""))
		# Main
		if option == 1:information_server()
		else:exit()