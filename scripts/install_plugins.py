"""
Install plugins
M20191
"""

import requests


plugins = {1:["",""]}

resp = requests.get("https://www.spigotmc.org/resources/gsit-modern-sit-seat-and-chair-lay-and-crawl-plugin-1-13-x-1-19-x.62325/download?version=459159")

open('plugins/', 'wb').write(resp.content)