#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Create by M20191

import requests
import json

# Crea un JSON con ids de plugins
def create_json_plugins():
    with open("plugins.json","r") as read:
        plugins = json.load(read)
        
        while True:
            name = input("Nombre Plugin (0 Para salir): ")
            if name == "0":
                break
            else:
                plugin_id = int(input("ID Plugin: "))
                plugins[name]= plugin_id

        json.dump(plugins,open("plugins.json","w"))


# Ejecuta el JSON y descarga el plugin
def execute_json_plugins():
    with open("plugins.json","r") as read:
        plugins = json.load(read)
    for name,_id in plugins.items():
        # Descarga contenido del plugin
        download = requests.get(f"https://api.spiget.org/v2/resources/{_id}/download")
        open(f"plugins/{name}.jar","wb").write(download.content)


def remove_json_plugins():
    open("plugins.json","w").write("")

# Main
select = int(input("""
    [1] Create JSON Plugins File
    [2] Execute JSON Plugins File
    [3] Remove JSON Plugins File
    
    """))

if select == 1:
    create_json_plugins()

elif select == 2:
    execute_json_plugins()

elif select == 3:
    remove_json_plugins()