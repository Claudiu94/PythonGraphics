import os as os

def createDirectories(dirs):
	for d in dirs:
		if not os.path.exists(d):
			os.makedirs(d)