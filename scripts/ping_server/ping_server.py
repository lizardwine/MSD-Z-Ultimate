#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Create by M20191
# Error file log --

from mcstatus import MinecraftServer
import re
from datetime import datetime

def ping_server(filename=''):
    try:
        serverNamePing = input("Nombre del Servidor: [0 For exit]: ")
        if serverNamePing != "0":
            server = MinecraftServer.lookup(serverNamePing)
            response = server.status()
            response.description = re.sub('§[\da-zA-Z]', '', response.description)
            data = f"Request: {datetime.now()}\nJugadores: {response.players.online}/{response.players.max}\nDisponibilidad: { response.players.max - response.players.online}\nLatencia: {response.latency}ms\nVersion/Bunge: {response.version.name[0:15]} {response.version.name[-6:]}\nDescripcion: {response.description}\nEstado: Activo"
            print(data)

        else:
            print("Cancelado con exito.\n")
        
        if filename:
            print("Guardando...")
            with open(filename,"a",encoding="UTF-8") as fp:
                fp.write(data)
    except:
        print("Servidor cerrado o en mantenimiento")

# Main
while True:
    option = int(input("[1]Ping server\n[2]Ping server with output\n[0 To exit]\n: "))
    if option == 1:
        ping_server()
    elif option == 2:
        log = input("File log: ")
        ping_server(log)
    else:
        break
