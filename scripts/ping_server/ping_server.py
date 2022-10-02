#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Create by M20191

from mcstatus import MinecraftServer
import re

def ping_server():
    try:
        serverNamePing = input("Nombre del Servidor: [0 For exit]: ")
        if serverNamePing != "0":
            server = MinecraftServer.lookup(serverNamePing)
            response = server.status()
            response.description = re.sub('§[\da-zA-Z]', '', response.description)
            print(f"""
            Jugadores: {response.players.online}/{response.players.max}
            Disponibilidad: { response.players.max - response.players.online}
            Latencia: {response.latency}ms
            Version/Bunge: {response.version.name[0:15]} {response.version.name[-6:]}
            Descripcion: {response.description}
            Estado: Activo
            """)
        else:
            print("Cancelado con exito.\n")
    except:
        print("Servidor cerrado o en mantenimiento")
ping_server()