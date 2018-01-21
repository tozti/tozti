import os, sys, shutil

def empty_extensions_list():
    for f in os.listdir("extensions/"):
        if f != ".gitkeep":
            shutil.rmtree(os.path.join("extensions", f))
