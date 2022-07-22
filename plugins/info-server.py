import json

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
		
	Jar-Name: {contents["name"]}
	Version: {contents["version"]}
	Ram: {contents["ram"]}

	Y88-888-888-888-888-888-888-888-88Y-88Y 

	""")

except:
	print("Download and install the server to be able to use this utility")