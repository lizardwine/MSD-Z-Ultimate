import os
import time


# Method to list and recopile new scripts
def script_list():
	path = os.getcwd()+"/scripts"
	current_script = os.listdir(path)
	
	count = 0
	for plugin in current_script:
		print(f"[{count}] {plugin}")
		count +=1

	try: 
		select_script = int(input("Script: "))

		exec(open(f"{path}/{current_script[select_script]}").read(), globals())
		
		time.sleep(5)

	except:
		print("unexpected error (no file,error script)")