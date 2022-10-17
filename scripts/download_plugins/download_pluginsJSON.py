#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by M20191

# Import modules
import requests
import json

def create_json_plugins():
    """
	Creates a JSON plugins file to automate plugins downloads with name and id
	"""
    # Open-read plugins JSON file
    with open("plugins.json","r") as read:
        plugins = json.load(read)
        
        while True:
            # Gets name of plugin
            name = input("Nombre Plugin (0 Para salir): ")
            if name == "0":break
            
            # Write name and id into JSON plugins file
            plugin_id = int(input("ID Plugin: "))
            plugins[name]= plugin_id

        json.dump(plugins,open("plugins.json","w"))


def execute_json_plugins():
    """
    Load the information from the JSON file and download plugins inside /plugins folder
    """
    # Open-read plugins
    with open("plugins.json","r") as read:
        plugins = json.load(read)
    
    # Download plugins from JSON file inside /plugins folder
    for name,_id in plugins.items():
        download = requests.get(f"https://api.spiget.org/v2/resources/{_id}/download")
        open(f"plugins/{name}.jar","wb").write(download.content)

def remove_json_plugins():
    """
    Delete JSON plugin file
    """
    # Remove JSON plugins file
    open("plugins.json","w").write("")

# Core
if __name__ == '__main__':
    while True:
        select = int(input("""
            [1] Create JSON Plugins File
            [2] Execute JSON Plugins File
            [3] Remove JSON Plugins File
            ...
            """))
        # Main
        if select == 1:create_json_plugins()
        elif select == 2:execute_json_plugins()
        elif select == 3:remove_json_plugins()