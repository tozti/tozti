import subprocess
from requests import get, post, put, patch, delete
import requests
from pymongo import MongoClient
import os, sys, shutil
import pytest

def empty_extensions_list():
    """Remove all extensions
    """
    for f in os.listdir("extensions/"):
        if f != ".gitkeep":
            shutil.rmtree(os.path.join("extensions", f))

def stop_tozti(tozti_proc):
    """Stop a given tozti_proc
    """
    if tozti_still_running(tozti_proc):
        tozti_proc.terminate()

def launch_tozti():
    """Start a tozti server and either:
        - return None if the server couldn't be launched
        - return a Popen object representing tozti's process
    """
    tozti_proc = subprocess.Popen(["python", "-m", "tozti", "dev"], 
                                  stdout = subprocess.PIPE)
    # parse stdout to know when the server is launched
    for line in iter(tozti_proc.stdout.readline, b''):
        if b'ERROR' in line \
           or b'CRITICAL' in line:
            stop_tozti(tozti_proc)
            return None
        if b'Finished boot sequence' in line:
            break
    return tozti_proc


def install_extension(ext):
    """Install the extension `ext` (found in `tests/extension`)
    as a Tozti extension
    """
    extension_folder = "tests/extensions/"
    ext_test = os.path.join(extension_folder, ext)
    if os.path.isdir(ext_test):
        shutil.copytree(ext_test,
                        os.path.join("extensions/", ext))


def tozti_still_running(tozti):
    """Check if the instance of tozti ran in the process passed
    as argument is still running

    Params:
        tozti: tozti's process
    """
    return tozti is not None and tozti.poll() is None


API = 'http://127.0.0.1:8080/api'

def make_call(meth, path, json=None):
    """make a call to the storage API

    Params:
        meth: the method use by the call. ex: PATCH, PUT, GET, POST, DELETE
        path: the relative path to the api
        json: the json that must be send with the request

    Returns:
        a `requests` object
    """
    return requests.request(meth, API + path, json=json)

def db_contains_object(db, obj):
    """Check if the database only contains object obj

    Params:
        db: a `pymongo` object which allow us to operate on the db
        obj: the obj we want to find in the db

    Returns:
        True if the object is in the db, False otherwize
    """
    for o in db.find():
        if o["body"] == obj["body"] :
            return True
    return False

def add_object_get_id(obj):
    """Insert the object defined by `obj` into the database
    And returns the associated id
    """
    ret_val = make_call("POST", '/store/resources', json={"data": obj}).json()
    return ret_val['data']['id']

