import os
import time


# Method to list and recopile new plugins
def plugins_list():
	path = os.getcwd()+"/plugins"
	current_plugins = os.listdir(path)
	
	count = 0
	for plugin in current_plugins:
		print(f"[{count}] {plugin}")
		count +=1

	try: 
		select_plugin = int(input("Plugin: "))

		exec(open(f"{path}/{current_plugins[select_plugin]}").read(), globals())
		
		time.sleep(5)

	except:
		print("unexpected error (no file,error plugin)")